from typing import TypeVar, Union, overload

from typing_extensions import Protocol, runtime_checkable

from protocol_lib.iterable import IIterable, IIterator

__all__ = [
    "ISequence",
    "IMutableSequence",
]


T = TypeVar("T")


@runtime_checkable
class ISequence(Protocol[T]):
    def __contains__(self, item: T) -> bool:
        ...

    def __iter__(self) -> IIterator[T]:
        ...

    def __reversed__(self) -> IIterator[T]:
        ...

    def __len__(self) -> int:
        ...

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> "ISequence[T]":
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[T, "ISequence[T]"]:
        ...

    def index(self, value: T, start: int = ..., stop: int = ...) -> int:
        ...

    def count(self, value: T) -> int:
        ...


@runtime_checkable
class IMutableSequence(Protocol[T]):
    def __contains__(self, item: T) -> bool:
        ...

    def __iter__(self) -> IIterator[T]:
        ...

    def __reversed__(self) -> IIterator[T]:
        ...

    def __len__(self) -> int:
        ...

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> "IMutableSequence[T]":
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[T, "IMutableSequence[T]"]:
        ...

    def index(self, value: T, start: int = ..., stop: int = ...) -> int:
        ...

    def count(self, value: T) -> int:
        ...

    def __setitem__(self, index: int, value: T) -> None:
        ...

    def __delitem__(self, index: int) -> None:
        ...

    def insert(self, index: int, value: T) -> None:
        ...

    def append(self, value: T) -> None:
        ...

    def clear(self) -> None:
        ...

    def reverse(self) -> None:
        ...

    def extend(self, values: ISequence[T]) -> None:
        ...

    def pop(self, index: int = ...) -> T:
        ...

    def remove(self, value: T) -> None:
        ...

    def __iadd__(self, values: IIterable[T]) -> "IMutableSequence[T]":
        ...
