from typing import NamedTuple, Tuple, cast

from sqlalchemy import select
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import Label

from rest_collection.api import AbstractApiRequest
from ..container import JoinMap
from ..modifier import SaQueryFilterModifier, \
    SaQueryLimitModifier, SaQueryOrderByModifier, SaQueryRelationModifier

__all__ = [
    'SqlalchemySelectorMixin',
]


class _SqlalchemyModifiers(NamedTuple):
    filter: SaQueryFilterModifier
    order_by: SaQueryOrderByModifier
    relation: SaQueryRelationModifier
    limit: SaQueryLimitModifier


class SqlalchemySelectorMixin:  # pylint: disable=too-few-public-methods
    __slots__ = ()

    @staticmethod
    def _get_modifiers(
        join_map: JoinMap,
        api_request: AbstractApiRequest,
    ) -> _SqlalchemyModifiers:
        return _SqlalchemyModifiers(
            SaQueryFilterModifier(api_request.filter, join_map),
            SaQueryOrderByModifier(api_request.order_by, join_map),
            SaQueryRelationModifier(api_request.relation, join_map),
            SaQueryLimitModifier(api_request.limit, join_map),
        )

    def get_query(self, for_counting: bool = False) -> Select:
        selectable: Tuple[
            Label, ...
        ] = self._select_collection.selectable  # type: ignore[attr-defined]

        sa_query = select(*selectable)

        modifiers: _SqlalchemyModifiers
        modifiers = self._modifiers  # type: ignore[attr-defined]

        # Фильтрация
        sa_query = modifiers.filter.modify(sa_query)

        # Сортировка
        if not for_counting:
            sa_query = modifiers.order_by.modify(sa_query)

        # Стыковка отношений
        sa_query = modifiers.relation.modify(sa_query)

        # Ограничение выборки
        if not for_counting:
            sa_query = modifiers.limit.modify(sa_query)

        return cast(Select, sa_query)
