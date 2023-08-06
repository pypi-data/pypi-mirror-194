import inspect
from contextlib import AsyncExitStack
from typing import Any, Callable, Optional, Type, TypeVar

from .binding import Binding, BindingMap
from .dependant import Dependant, DependantMap
from .errors import ImplicitBindingError
from .implicit import is_implicitbinding
from .instance import InstanceMap
from .util import determine_return_type, invoke_callable

T = TypeVar("T")
Func = TypeVar("Func", bound=Callable[..., Any])


class FlexState:
    def __init__(self) -> None:
        self._stack: AsyncExitStack = AsyncExitStack()
        self.opened = False
        self._bindings = BindingMap()
        self._dependants = DependantMap()
        self._instances = InstanceMap()

    def chain(self) -> "FlexState":
        state = FlexState()
        state._bindings = self._bindings.chain()
        state._dependants = self._dependants.chain()
        state._instances = self._instances.chain()
        return state

    async def open(self) -> "FlexState":
        if not self.opened:
            self.opened = True
            try:
                initial_bindings = [binding for _, binding in self._bindings.items()]
                for binding in initial_bindings:
                    self.dependant(binding)
                for binding in initial_bindings:
                    if binding.eager:
                        dependant = self._dependants[binding.target]
                        await self.instance(dependant)
            except:  # noqa: E722
                await self.close()
                raise
        return self

    async def close(self) -> None:
        self._instances.clear()
        self._dependants.clear()
        try:
            await self._stack.aclose()
        finally:
            self.opened = False

    async def resolve(self, func: Any) -> Any:
        return await self.instance(self.dependant(self.binding(func)))

    def binding(
        self,
        func: Callable[..., Any],
        *,
        target: Optional[Type[Any]] = None,
        eager: bool = False,
        allow_implicit: bool = True,
        use_cached: bool = True,
        update_cached: bool = True,
    ) -> Binding:
        target = target or determine_return_type(func)

        if use_cached and target in self._bindings:
            return self._bindings[target]

        if not (allow_implicit or is_implicitbinding(target)):
            raise ImplicitBindingError(
                f"Requested a binding for {func} that was not explicitly "
                "marked for binding."
            )

        binding = Binding(
            target=target,
            func=func,
            eager=eager,
        )

        if update_cached:
            self._bindings[target] = binding

            # If we're updating the cached binding to replace it, then we should
            # remove any of the resolved dependant trees and instances.
            if binding.target in self._dependants:
                del self._dependants[binding.target]
            if binding.target in self._instances:
                del self._instances[binding.target]
            if binding.func in self._instances:
                del self._instances[binding.func]

        return binding

    def dependant(
        self,
        binding: Binding,
        *,
        use_cached: bool = True,
        update_cached: bool = True,
    ) -> Dependant:
        if use_cached and binding.target in self._dependants:
            return self._dependants[binding.target]

        with self._dependants.cycle_guard(binding.target):
            signature = inspect.signature(binding.func)
            dependant = Dependant(
                target=binding.target,
                func=binding.func,
                args={
                    name: self.dependant(
                        self.binding(
                            param.annotation,
                            target=param.annotation,
                            eager=binding.eager,
                            allow_implicit=False,
                        )
                    )
                    for name, param in signature.parameters.items()
                },
            )

        if update_cached:
            self._dependants[binding.target] = dependant

        return dependant

    async def instance(
        self,
        dependant: Dependant,
        *,
        use_cached: bool = True,
        update_cached: bool = True,
    ) -> Any:
        if use_cached and dependant.target in self._instances:
            return self._instances[dependant.target]
        if use_cached and dependant.func in self._instances:
            return self._instances[dependant.func]

        instance = await invoke_callable(
            stack=self._stack,
            func=dependant.func,
            args={
                name: await self.instance(subdep)
                for name, subdep in dependant.args.items()
            },
        )

        if update_cached:
            self._instances[dependant.target] = instance
            self._instances[dependant.func] = instance

        return instance
