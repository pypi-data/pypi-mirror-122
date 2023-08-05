from typing_extensions import Protocol, runtime_checkable

__all__ = [
    "IHashable",
]


@runtime_checkable
class IHashable(Protocol):
    def __hash__(self) -> int:
        ...
