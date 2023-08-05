from typing import Iterator, Sequence, Tuple, TypeVar

from sqlalchemy import Column

from rest_collection.typing import TableLikeType

__all__ = [
    'ItemGetter',
    'TableIndices',
]

_ItemType = TypeVar('_ItemType')


class ItemGetter:  # pylint: disable=too-few-public-methods
    """Реализация operator.itemgetter, возвращающая только кортежи."""
    def __init__(self, *items: int) -> None:
        self._items = items

    def __call__(self, data: Sequence[_ItemType]) -> Tuple[_ItemType, ...]:
        return tuple(map(lambda item: data[item], self._items))


class TableIndices:
    """Определяющий индексы колонок таблиц контейнер."""
    __slots__ = ('_table',)

    def __init__(self, sa_table: TableLikeType) -> None:
        self._table = sa_table

    def _iter_columns(self, offset: int) -> Iterator[Tuple[int, Column]]:
        return enumerate(self._table.columns, start=offset)

    def get_indices(self, offset: int = 0) -> Tuple[int, ...]:
        return tuple(i for i, _ in self._iter_columns(offset=offset))

    def get_primary_indices(self, offset: int = 0) -> Tuple[int, ...]:
        return tuple(
            i for i, column in self._iter_columns(offset=offset)
            if column.primary_key is True
        )

    def primary_getter(self, offset: int = 0) -> ItemGetter:
        return ItemGetter(*self.get_primary_indices(offset=offset))

    def getter(self, offset: int = 0) -> ItemGetter:
        return ItemGetter(*self.get_indices(offset=offset))
