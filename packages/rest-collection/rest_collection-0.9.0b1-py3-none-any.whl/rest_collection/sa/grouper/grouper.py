from functools import partial
from operator import attrgetter, is_
from typing import Any, Dict, Hashable, List, Mapping, MutableMapping, Sequence, \
    Tuple, cast

from sqlalchemy.sql import Alias

from rest_collection.typing import TableLikeType
from .abc import AbstractGrouper
from ..container import ItemGetter, SelectCollection, SelectElement, \
    TableIndices

__all__ = [
    'SqlalchemyGrouper',
]

_is_none = partial(is_, None)


class SqlalchemyGrouper(AbstractGrouper):
    __slots__ = ('_group_info',)

    def __init__(self, *select_elements: SelectElement) -> None:
        assert all(map(lambda x: isinstance(x, SelectElement), select_elements))

        self._group_info: List[
            Tuple[
                str,
                Tuple[str, ...],
                ItemGetter,
                ItemGetter,
            ]
        ] = []
        next_index = 0

        for select_element in select_elements:

            if select_element.is_element:
                # На данный момент простые элементы выборки не обрабатываются
                #  группировщиком. Для верной их группировки, они должны
                # содержать отношение
                next_index += len(select_element)
                continue

            sa_table = cast(
                TableLikeType,
                select_element.sa_element,
            )
            sa_tablename = sa_table.original.name if isinstance(
                sa_table, Alias,
            ) else sa_table.name

            indexer = TableIndices(sa_table)

            self._group_info.append((
                sa_tablename,
                tuple(map(attrgetter('key'), sa_table.columns)),
                indexer.primary_getter(offset=next_index),
                indexer.getter(offset=next_index),
            ))

            next_index += len(select_element)

    def group_row(
        self,
        row: Sequence[Any],
        grouped: Mapping[
            str,
            MutableMapping[Tuple[Hashable, ...], Dict[str, Any]]
        ],
    ) -> None:
        for (
            data_label,
            row_labels,
            primary_getter,
            getter,
        ) in self._group_info:

            data = grouped[data_label]
            primary_key = primary_getter(row)

            if all(map(_is_none, primary_key)):
                # Данные с нулевыми основными ключами не выгружаем
                continue

            if primary_key in data:
                continue

            # Предполагается, что типы в основных ключах таблиц будут хэшируемы
            data[primary_key] = dict(zip(row_labels, getter(row)))

    @classmethod
    def from_select_collection(
        cls,
        select_collection: SelectCollection,
    ) -> 'SqlalchemyGrouper':
        return cls(*select_collection)
