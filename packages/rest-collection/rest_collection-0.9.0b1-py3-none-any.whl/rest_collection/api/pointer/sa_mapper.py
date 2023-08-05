from operator import attrgetter
from typing import Any, Iterator, Mapping
from weakref import WeakKeyDictionary

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Mapper

__all__ = [
    'SaMapperRegistry',
]


class SaMapperRegistry(Mapping[DeclarativeMeta, Mapper]):
    """
    Sqlalchemy model mappers registry.
    """
    __slots__ = '_data', '__weakref__'

    def __init__(self) -> None:
        self._data: WeakKeyDictionary[
            DeclarativeMeta,
            Mapper,
        ] = WeakKeyDictionary()

    def __getitem__(self, key: DeclarativeMeta) -> Mapper:
        if key not in self._data:
            self._data[key] = inspect(key)
        return self._data[key]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[DeclarativeMeta]:
        return iter(self._data)

    def __repr__(self) -> str:
        keys = ', '.join(
            sorted(
                map(
                    attrgetter('__tablename__'), self._data.keys(),
                ),
            ),
        )
        return f'<{self.__class__.__name__} keys={keys}>'

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError(
                f'Comparison only with {self.__class__.__name__!r} '
                f'objects is allowed.',
            )
        return frozenset(other) == frozenset(self)
