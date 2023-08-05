from typing import TypeVar

from typing_extensions import Protocol, runtime_checkable

__all__ = [
    "IContainer",
]


T_contra = TypeVar("T_contra", contravariant=True)


@runtime_checkable
class IContainer(Protocol[T_contra]):
    def __contains__(self, item: T_contra) -> bool:
        ...
