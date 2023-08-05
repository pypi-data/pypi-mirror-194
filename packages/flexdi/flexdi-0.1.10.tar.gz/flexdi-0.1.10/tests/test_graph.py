from dataclasses import dataclass
from typing import Any, AsyncIterator, Iterator

import pytest
from pydantic import BaseModel

# Import of Annotated not available from typing until 3.9
# Import of assert_type not available from typing until 3.11
from typing_extensions import Annotated, assert_type

from flexdi import CycleError, FlexGraph


@pytest.mark.asyncio
async def test_dependant_simple() -> None:
    """
    For a simple class with no arguments, we should be able to easily determine
    the dependency tree.
    """

    class Foo:
        pass

    async with FlexGraph() as graph:
        res = await graph.resolve(Foo)
        assert isinstance(res, Foo)


@pytest.mark.asyncio
async def test_dependant_chained() -> None:
    """
    When arguments are specified, follow the tree to construct them.
    """

    class Foo:
        pass

    class Bar:
        def __init__(self, dep1: Foo) -> None:
            self.dep1 = dep1

    async with FlexGraph() as graph:
        res = await graph.resolve(Bar)
        assert isinstance(res, Bar)
        assert isinstance(res.dep1, Foo)


@pytest.mark.asyncio
async def test_dependant_chained_dataclasses() -> None:
    """
    Now lets try it with dataclasses.
    """

    @dataclass
    class Foo:
        pass

    @dataclass
    class Bar:
        dep1: Foo

    async with FlexGraph() as graph:
        res = await graph.resolve(Bar)
        assert isinstance(res, Bar)
        assert isinstance(res.dep1, Foo)


@pytest.mark.asyncio
async def test_dependant_chained_pydantic() -> None:
    """
    Now lets try it with pydantic models used.
    """

    class Foo(BaseModel):
        pass

    class Bar(BaseModel):
        dep1: Foo

    async with FlexGraph() as graph:
        res = await graph.resolve(Bar)
        assert isinstance(res, Bar)
        assert isinstance(res.dep1, Foo)


@pytest.mark.asyncio
async def test_cycle_detection() -> None:
    """
    This is a bit of a contrived case, but if there are cycles present in the
    dependency tree, we should fail as there would be no way to construct the
    object required.
    """

    class Foo:
        pass

    class Bar:
        pass

    def foo_init(self: Foo, dep1: Bar) -> None:
        self.dep1 = dep1  # type: ignore

    def bar_init(self: Bar, dep1: Foo) -> None:
        self.dep1 = dep1  # type: ignore

    Foo.__init__ = foo_init  # type: ignore
    Bar.__init__ = bar_init  # type: ignore

    async with FlexGraph() as graph:
        with pytest.raises(CycleError):
            await graph.resolve(Foo)
        with pytest.raises(CycleError):
            await graph.resolve(Bar)


@pytest.mark.asyncio
async def test_provider() -> None:
    @dataclass
    class Foo:
        value: int

    @dataclass
    class Bar:
        dep1: Foo

    graph = FlexGraph()

    @graph.bind
    def foo_provider() -> Foo:
        return Foo(2)

    async with graph:
        res = await graph.resolve(Bar)
        assert isinstance(res, Bar)
        assert isinstance(res.dep1, Foo)
        assert res.dep1.value == 2


@pytest.mark.asyncio
async def test_provider_no_decorator() -> None:
    @dataclass
    class Foo:
        value: int

    @dataclass
    class Bar:
        dep1: Foo

    def foo_provider() -> Foo:
        return Foo(2)

    graph = FlexGraph()
    graph.bind(foo_provider)

    async with graph:
        res = await graph.resolve(Bar)
        assert isinstance(res, Bar)
        assert isinstance(res.dep1, Foo)
        assert res.dep1.value == 2


@pytest.mark.asyncio
async def test_provider_lambda() -> None:
    @dataclass
    class Foo:
        value: int

    @dataclass
    class Bar:
        dep1: Foo

    graph = FlexGraph()
    graph.bind(lambda: Foo(2), resolves=Foo)

    async with graph:
        res = await graph.resolve(Bar)
        assert isinstance(res, Bar)
        assert isinstance(res.dep1, Foo)
        assert res.dep1.value == 2


@pytest.mark.asyncio
async def test_provider_interface_map() -> None:
    @dataclass
    class Foo:
        pass

    @dataclass
    class FooChild(Foo):
        pass

    @dataclass
    class Bar:
        dep1: Foo

    graph = FlexGraph()
    graph.bind(FooChild, resolves=Foo)

    async with graph:
        res = await graph.resolve(Bar)
        assert isinstance(res, Bar)
        assert isinstance(res.dep1, FooChild)


@pytest.mark.asyncio
async def test_provider_lower_level() -> None:
    @dataclass
    class Foo:
        value: int

    @dataclass
    class Bar:
        dep1: Foo

    graph = FlexGraph()

    @graph.bind
    def value_provider() -> int:
        return 2

    async with graph:
        res = await graph.resolve(Bar)
        assert isinstance(res, Bar)
        assert isinstance(res.dep1, Foo)
        assert res.dep1.value == 2


@pytest.mark.asyncio
async def test_provider_clazz_mapping() -> None:
    @dataclass
    class Foo:
        value: int

    graph = FlexGraph()

    @graph.bind(resolves=int)
    def value_provider() -> Any:
        return 3

    async with graph:
        res = await graph.resolve(Foo)
        assert isinstance(res, Foo)
        assert res.value == 3


@pytest.mark.asyncio
async def test_provider_annotated() -> None:
    @dataclass
    class Foo:
        value1: Annotated[int, "value1"]
        value2: Annotated[int, "value2"]

    graph = FlexGraph()

    @graph.bind
    def value1_provider() -> Annotated[int, "value1"]:
        return 123

    @graph.bind
    def value2_provider() -> Annotated[int, "value2"]:
        return 456

    async with graph:
        res = await graph.resolve(Foo)
        assert isinstance(res, Foo)
        assert res.value1 == 123
        assert res.value2 == 456


@pytest.mark.asyncio
async def test_provider_annotated_mapping() -> None:
    @dataclass
    class Foo:
        value1: Annotated[int, "value1"]
        value2: Annotated[int, "value2"]

    graph = FlexGraph()

    @graph.bind(resolves=Annotated[int, "value1"])
    def value1_provider() -> int:
        return 123

    @graph.bind(resolves=Annotated[int, "value2"])
    def value2_provider() -> int:
        return 456

    async with graph:
        res = await graph.resolve(Foo)
        assert isinstance(res, Foo)
        assert res.value1 == 123
        assert res.value2 == 456


@pytest.mark.asyncio
async def test_provider_annotated_chained() -> None:
    @dataclass
    class Foo:
        value1: Annotated[int, "value1"]
        value2: Annotated[int, "value2"]

    graph = FlexGraph()

    @graph.bind
    def value1_provider() -> Annotated[int, "value1"]:
        return 123

    @graph.bind(resolves=Annotated[int, "value2"])
    def value2_provider(value1: Annotated[int, "value1"]) -> int:
        return value1 + 111

    async with graph:
        res = await graph.resolve(Foo)
        assert isinstance(res, Foo)
        assert res.value1 == 123
        assert res.value2 == 234


@pytest.mark.asyncio
async def test_singleton() -> None:
    @dataclass
    class Foo:
        value1: int
        value2: str

    graph = FlexGraph()

    called_value1_provider = 0
    called_value2_provider = 0

    @graph.bind(eager=True)
    def value1_provider() -> int:
        nonlocal called_value1_provider
        called_value1_provider += 1
        return 1

    @graph.bind
    def value2_provider() -> str:
        nonlocal called_value2_provider
        called_value2_provider += 1
        return "2"

    async with graph:
        async with graph.chain() as sub_injector:
            await sub_injector.resolve(Foo)
        async with graph.chain() as sub_injector:
            await sub_injector.resolve(Foo)

    assert called_value1_provider == 1
    assert called_value2_provider == 2

    async with graph:
        async with graph.chain() as sub_injector:
            await sub_injector.resolve(Foo)
        async with graph.chain() as sub_injector:
            await sub_injector.resolve(Foo)

    assert called_value1_provider == 2
    assert called_value2_provider == 4


@pytest.mark.asyncio
async def test_sync_dep_provider() -> None:
    @dataclass
    class Foo:
        value: int

    graph = FlexGraph()

    provider_events = []

    @graph.bind
    def provider() -> int:
        provider_events.append("entered")
        return 1

    async with graph:
        provider_events = []

        res = await graph.resolve(Foo)
        assert isinstance(res, Foo)
        assert res.value == 1

        provider_events = ["entered"]

    provider_events = ["entered"]


@pytest.mark.asyncio
async def test_async_dep_provider() -> None:
    @dataclass
    class Foo:
        value: int

    graph = FlexGraph()

    provider_events = []

    @graph.bind
    async def provider() -> int:
        provider_events.append("entered")
        return 1

    async with graph:
        provider_events = []

        res = await graph.resolve(Foo)
        assert isinstance(res, Foo)
        assert res.value == 1

        provider_events = ["entered"]

    provider_events = ["entered"]


@pytest.mark.asyncio
async def test_sync_gen_provider() -> None:
    @dataclass
    class Foo:
        value: int

    graph = FlexGraph()

    provider_events = []

    @graph.bind
    def provider() -> Iterator[int]:
        provider_events.append("entered")
        try:
            yield 1
        finally:
            provider_events.append("exited")

    async with graph:
        provider_events = []

        res = await graph.resolve(Foo)
        assert isinstance(res, Foo)
        assert res.value == 1

        provider_events = ["entered"]

    provider_events = ["entered", "exited"]


@pytest.mark.asyncio
async def test_async_gen_provider() -> None:
    @dataclass
    class Foo:
        value: int

    graph = FlexGraph()

    provider_events = []

    @graph.bind
    async def provider() -> AsyncIterator[int]:
        provider_events.append("entered")
        try:
            yield 1
        finally:
            provider_events.append("exited")

    async with graph:
        provider_events = []

        res = await graph.resolve(Foo)
        assert isinstance(res, Foo)
        assert res.value == 1

        provider_events = ["entered"]

    provider_events = ["entered", "exited"]


@pytest.mark.asyncio
async def test_all_providers() -> None:
    @dataclass
    class Foo:
        val1: Annotated[int, "value1"]
        val2: Annotated[int, "value2"]
        val3: Annotated[int, "value3"]
        val4: Annotated[int, "value4"]

    graph = FlexGraph()

    @graph.bind(resolves=Annotated[int, "value1"])
    def value1() -> int:
        return 1

    @graph.bind(resolves=Annotated[int, "value2"])
    async def value2() -> int:
        return 2

    @graph.bind(resolves=Annotated[int, "value3"])
    def value3() -> Iterator[int]:
        yield 3

    @graph.bind(resolves=Annotated[int, "value4"])
    async def value4() -> AsyncIterator[int]:
        yield 4

    async with graph:
        res = await graph.resolve(Foo)
        assert isinstance(res, Foo)
        assert res.val1 == 1
        assert res.val2 == 2
        assert res.val3 == 3
        assert res.val4 == 4


@pytest.mark.asyncio
async def test_supports_all_func_invocations() -> None:
    class Foo:
        pass

    def func1(foo: Foo) -> Foo:
        return foo

    async def func2(foo: Foo) -> Foo:
        return foo

    def func3(foo: Foo) -> Iterator[Foo]:
        yield foo

    async def func4(foo: Foo) -> AsyncIterator[Foo]:
        yield foo

    async with FlexGraph() as graph:
        res1 = await graph.resolve(func1)
        res2 = await graph.resolve(func2)
        res3 = await graph.resolve(func3)
        res4 = await graph.resolve(func4)
        assert_type(res1, Foo)
        assert_type(res2, Foo)
        assert_type(res3, Foo)
        assert_type(res4, Foo)
        assert isinstance(res1, Foo)
        assert isinstance(res2, Foo)
        assert isinstance(res3, Foo)
        assert isinstance(res4, Foo)


@pytest.mark.asyncio
async def test_gen_shutdown_order_loop() -> None:
    """
    Assert that when running asynchronous dependencies from a synchronous
    function that the cleanup is performed in the expected order.
    """

    graph = FlexGraph()

    class Foo:
        pass

    class Bar:
        pass

    events = []

    @graph.bind
    async def func1() -> AsyncIterator[Foo]:
        events.append(1)
        yield Foo()
        events.append(5)

    @graph.bind
    async def func2(foo: Foo) -> AsyncIterator[Bar]:
        events.append(2)
        yield Bar()
        events.append(4)

    @graph.bind
    async def func3(bar: Bar) -> None:
        events.append(3)

    async with graph:
        await graph.resolve(func3)

    assert events == [1, 2, 3, 4, 5]


@pytest.mark.asyncio
async def test_bindings_out_of_order() -> None:
    """
    If we get dependencies in a different order than their dependency resolution
    order, we should be able to construct the correct graph regardless.

    In this case we have a dependency chain (Buzz -> Fizz -> Foo) and we bind Bar
    to be the resolver of Foo after we have already made a binding to resolve Fizz.

    If we determine the dependencies too early, then the Fizz will think that Foo
    should be its own resolver, because at the time of binding that would make sense.
    Only once we enter the with statement should we evaluate the full dependency
    tree, because at that point we can reference all bindings made no matter what
    order they are made in.
    """

    graph = FlexGraph()

    class Foo:
        pass

    class Bar(Foo):
        pass

    @dataclass
    class Fizz:
        foo: Foo

    @dataclass
    class Buzz:
        fizz: Fizz

    graph.bind(Buzz)
    graph.bind(Bar, resolves=Foo)

    async with graph:
        buzz = await graph.resolve(Buzz)
        assert isinstance(buzz, Buzz)
        assert isinstance(buzz.fizz, Fizz)
        assert isinstance(buzz.fizz.foo, Bar)


def test_entrypoints() -> None:
    graph = FlexGraph()

    class Foo:
        pass

    @graph.entrypoint
    def main1(foo: Foo) -> Foo:
        return foo

    @graph.entrypoint
    async def main2(foo: Foo) -> Foo:
        return foo

    @graph.entrypoint()
    def main3(foo: Foo) -> Foo:
        return foo

    @graph.entrypoint()
    async def main4(foo: Foo) -> Foo:
        return foo

    res1 = main1()
    res2 = main2()
    res3 = main3()
    res4 = main4()
    assert_type(res1, Foo)
    assert_type(res2, Foo)
    assert_type(res3, Foo)
    assert_type(res4, Foo)
    assert isinstance(res1, Foo)
    assert isinstance(res2, Foo)
    assert isinstance(res3, Foo)
    assert isinstance(res4, Foo)


@pytest.mark.asyncio
async def test_one_instance_multiple_targets() -> None:
    """
    Foo and Bar are normal classes.
    A class Fizz exists which can satisfy either Foo or Bar.

    We should be able to find the definition of Fizz to both Foo and Bar,
    and there should only be one instance created from doing so.
    """

    graph = FlexGraph()

    @dataclass
    class Foo:
        pass

    @dataclass
    class Bar:
        pass

    @dataclass
    class Fizz(Foo, Bar):
        pass

    @dataclass
    class Buzz:
        foo: Foo
        bar: Bar

    graph.bind(Fizz, resolves=Foo)
    graph.bind(Fizz, resolves=Bar)

    async with graph:
        buzz = await graph.resolve(Buzz)
        assert isinstance(buzz.foo, Fizz)
        assert isinstance(buzz.bar, Fizz)
        assert id(buzz.foo) == id(buzz.bar)
