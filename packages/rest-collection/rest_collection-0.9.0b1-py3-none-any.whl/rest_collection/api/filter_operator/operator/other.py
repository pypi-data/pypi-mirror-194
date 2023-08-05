from typing import Any, Callable, Iterable, Type, cast

from sqlalchemy.sql.elements import BinaryExpression, ColumnClause
from ujson import loads

from rest_collection.typing import ApiOperatorType
from ...abc import AbstractApiOperator, AbstractApiSetOperator, \
    AbstractApiSimpleOperator

__all__ = [
    'ApiInOperator',
    'ApiNotInOperator',
    'ApiIsOperator',
    'ApiNotIsOperator',
    'ApiBetweenOperator',
]


class ApiInOperator(AbstractApiSetOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return cast(
            Callable[[ColumnClause, Iterable[Any]], BinaryExpression],
            lambda a, b: a.in_(b),
        )


class ApiNotInOperator(AbstractApiSetOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return cast(
            Callable[[ColumnClause, Iterable[Any]], BinaryExpression],
            lambda a, b: a.notin_(b)
        )


class ApiIsOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return cast(
            Callable[[ColumnClause, Any], BinaryExpression],
            lambda a, b: a.is_(b)
        )


class ApiNotIsOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return cast(
            Callable[[ColumnClause, Any], BinaryExpression],
            lambda a, b: a.isnot(b)
        )


class ApiBetweenOperator(AbstractApiOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return cast(
            Callable[[ColumnClause, Any, Any], BinaryExpression],
            lambda a, b, c: a.between(b, c)
        )

    def _deserialize(
        self,
        column_type: Type[object],
        raw_value: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        right, left = loads(raw_value)
        deserializer = self.__class__.deserializer
        return self._get_deserialize_result(
            deserializer(column_type, right), deserializer(column_type, left),
        )
