from typing import Any, Dict, Iterator, Set

__all__ = [
    'Aliases',
]


class Aliases(Set[str]):
    """Представление алиасов одной сущности с выделением основного."""
    __slots__ = '_alt', '_main'

    def __init__(self, main: str, *alt: str) -> None:
        super().__init__()
        self._main = main
        self._alt = frozenset(alt)

    def __iter__(self) -> Iterator[str]:
        yield self._main
        yield from self._alt

    def __contains__(self, value: Any) -> bool:
        return str(value) == self._main or str(value) in self._alt

    def __len__(self) -> int:
        return len(self._alt) + 1

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} ' \
               f'main={self._main!r} ' \
               f'alt={self._alt!r}>'

    @property
    def main(self) -> str:
        return self._main

    @property
    def map(self) -> Dict[str, str]:
        return {
            alias: self._main for alias in self._alt
        }
