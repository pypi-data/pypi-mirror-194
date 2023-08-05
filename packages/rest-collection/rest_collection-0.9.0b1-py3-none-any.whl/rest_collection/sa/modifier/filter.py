from typing import Any

from sqlalchemy.sql import Select

from rest_collection.api import AbstractApiFilterRequestContext
from .abc import AbstractSaQueryModifier

__all__ = [
    'SaQueryFilterModifier',
]


class SaQueryFilterModifier(
    AbstractSaQueryModifier[AbstractApiFilterRequestContext],
):
    __slots__ = ()

    def fill_join_map(self) -> None:
        if not self:
            return

        pointers = self.data.pointers

        if pointers is None:
            return

        for api_pointer in pointers:
            self.join_map.add_pointer(api_pointer)

    def modify(self, sa_query: Select, *args: Any, **kwargs: Any) -> Select:
        if not self:
            return sa_query

        return sa_query.where(
            self.data.compile(self.join_map.aliased_table_map),
        )
