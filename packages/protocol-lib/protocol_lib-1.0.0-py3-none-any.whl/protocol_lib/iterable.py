from typing import TypeVar

from typing_extensions import Protocol, runtime_checkable

__all__ = [
    "IIterable",
    "IIterator",
    "IReversible",
]


T_co = TypeVar("T_co", covariant=True)


@runtime_checkable
class IIterable(Protocol[T_co]):
    def __iter__(self) -> "IIterator[T_co]":
        ...


@runtime_checkable
class IIterator(Protocol[T_co]):
    def __iter__(self) -> "IIterator[T_co]":
        ...

    def __next__(self) -> T_co:
        ...


@runtime_checkable
class IReversible(Protocol[T_co]):
    def __iter__(self) -> "IIterator[T_co]":
        ...

    def __reversed__(self) -> "IIterator[T_co]":
        ...
