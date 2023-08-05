from dataclasses import dataclass
from functools import partial
from operator import methodcaller
from types import MappingProxyType
from typing import Any, Callable, Mapping, cast

from sqlalchemy import Column, String, cast as sql_cast, not_
from sqlalchemy.sql.elements import BinaryExpression, ColumnClause

from rest_collection.typing import ApiOperatorType
from ...abc import AbstractApiSimpleOperator

__all__ = [
    'ApiStartsWithOperator',
    'ApiNotStartsWithOperator',
    'ApiIStartsWithOperator',
    'ApiNotIStartsWithOperator',
    'ApiEndsWithOperator',
    'ApiNotEndsWithOperator',
    'ApiIEndsWithOperator',
    'ApiNotIEndsWithOperator',
    'ApiContainsOperator',
    'ApiNotContainsOperator',
    'ApiIContainsOperator',
    'ApiNotIContainsOperator',
]


@dataclass(frozen=True)
class _LikeRule:
    method: str
    value_getter: Callable[[str], str]


_LIKE_RULE_MAP: Mapping[
    str, _LikeRule,
] = MappingProxyType({
    'startswith': _LikeRule('like', lambda x: f'{x}%'),
    'istartswith': _LikeRule('ilike', lambda x: f'{x}%'),
    'endswith': _LikeRule('like', lambda x: f'%{x}'),
    'iendswith': _LikeRule('ilike', lambda x: f'%{x}'),
    'contains': _LikeRule('like', lambda x: f'%{x}%'),
    'icontains': _LikeRule('ilike', lambda x: f'%{x}%'),
})


def _make_like_expression(
    like_rule_label: str,
    column: Column,
    value: Any,
) -> BinaryExpression:
    """
    Making filter like or ilike expression.

    :param like_rule_label: Key of ``_LIKE_RULE_MAP``.
    :param column: Sqlalchemy column.
    :param value: Value of filter.
    """
    like_rule = _LIKE_RULE_MAP[like_rule_label]

    if column.type.python_type is not str:
        column = sql_cast(column, String)

    return cast(
        BinaryExpression,
        methodcaller(
            like_rule.method,
            like_rule.value_getter(str(value)),
        )(column),
    )


_startswith = partial(
    _make_like_expression, 'startswith',
)  # type: ApiOperatorType


class ApiStartsWithOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return _startswith


class ApiNotStartsWithOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return cast(
            Callable[[ColumnClause, Any], BinaryExpression],
            lambda a, b: not_(  # type: ignore[no-untyped-call]
                _startswith(a, b)
            ),
        )


_istartswith = partial(
    _make_like_expression, 'istartswith',
)  # type: ApiOperatorType


class ApiIStartsWithOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return _istartswith


class ApiNotIStartsWithOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return cast(
            Callable[[ColumnClause, Any], BinaryExpression],
            lambda a, b: not_(  # type: ignore[no-untyped-call]
                _istartswith(a, b),
            ),
        )


_endswith = partial(
    _make_like_expression, 'endswith',
)  # type: ApiOperatorType


class ApiEndsWithOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return _endswith


class ApiNotEndsWithOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return cast(
            Callable[[ColumnClause, Any], BinaryExpression],
            lambda a, b: not_(  # type: ignore[no-untyped-call]
                _endswith(a, b),
            ),
        )


_iendswith = partial(
    _make_like_expression, 'iendswith',
)  # type: ApiOperatorType


class ApiIEndsWithOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return _iendswith


class ApiNotIEndsWithOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return cast(
            Callable[[ColumnClause, Any], BinaryExpression],
            lambda a, b: not_(  # type: ignore[no-untyped-call]
                _iendswith(a, b),
            ),
        )


_contains = partial(
    _make_like_expression, 'contains',
)  # type: ApiOperatorType


class ApiContainsOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return _contains


class ApiNotContainsOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return cast(
            Callable[[ColumnClause, Any], BinaryExpression],
            lambda a, b: not_(  # type: ignore[no-untyped-call]
                _contains(a, b),
            ),
        )


_icontains = partial(
    _make_like_expression, 'icontains',
)  # type: ApiOperatorType


class ApiIContainsOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return _icontains


class ApiNotIContainsOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return cast(
            Callable[[ColumnClause, Any], BinaryExpression],
            lambda a, b: not_(  # type: ignore[no-untyped-call]
                _icontains(a, b),
            ),
        )
