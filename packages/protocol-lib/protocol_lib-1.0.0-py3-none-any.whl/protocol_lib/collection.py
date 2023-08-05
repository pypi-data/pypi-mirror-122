from typing import TypeVar

from typing_extensions import Protocol, runtime_checkable

from protocol_lib.iterable import IIterator

__all__ = [
    "ICollection",
]


T = TypeVar("T")


@runtime_checkable
class ICollection(Protocol[T]):
    def __contains__(self, item: T) -> bool:
        ...

    def __iter__(self) -> IIterator[T]:
        ...

    def __len__(self) -> int:
        ...
