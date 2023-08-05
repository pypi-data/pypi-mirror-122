from typing_extensions import Protocol, runtime_checkable

__all__ = [
    "ISized",
]


@runtime_checkable
class ISized(Protocol):
    def __len__(self) -> int:
        ...
