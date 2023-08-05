from operator import methodcaller
from typing import Any, Callable, FrozenSet, Iterator, List, Optional, Sequence, \
    TYPE_CHECKING, Union, cast, overload
from weakref import ref

from sqlalchemy import Column, and_, or_
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList

from rest_collection.exc import RestCollectionReferenceError
from rest_collection.typing import ApiOperatorType
from ..alias import AliasedTableMap
from ..exc import ApiFilterExpressionError, ApiPointerError
from ..pointer import ApiPointer, ApiPointerRegistry

if TYPE_CHECKING:
    from ..abc import AbstractApiOperatorRegistry

__all__ = [
    'ApiFilterExpression',
    'ApiFilterExpressionGroup',
]


class ApiFilterExpression:
    """
    API filter expression.
    """
    __slots__ = '_pointer_ref', '_operator', '_value'

    def __init__(
        self,
        pointer: ApiPointer,
        operator: ApiOperatorType,
        value: Any,
    ):
        self._pointer_ref = ref(pointer)
        self._operator = operator
        self._value = value

    @property
    def pointer(self) -> ApiPointer:
        pointer = self._pointer_ref()
        if pointer is None:
            raise RestCollectionReferenceError()
        return pointer

    @property
    def sa_column(self) -> Optional[Column]:
        return self.pointer.sa_column

    @property
    def value(self) -> Any:
        return self._value

    @property
    def operator(self) -> ApiOperatorType:
        return self._operator

    def compile(self, aliased_table_map: AliasedTableMap) -> BinaryExpression:
        api_pointer = self.pointer

        if api_pointer is None:
            raise RestCollectionReferenceError()

        if api_pointer.parent is None:
            column = self.sa_column

        else:
            aliased_table = aliased_table_map[api_pointer]
            sa_column = cast(Column, self.sa_column)
            column = aliased_table.columns[sa_column.key]

        return self._operator(
            column,
            self.value,
        )

    __call__ = compile

    @classmethod
    def from_string(
        cls,
        expression_string: str,
        pointer_registry: ApiPointerRegistry,
        operator_registry: 'AbstractApiOperatorRegistry',
    ) -> 'ApiFilterExpression':
        expression_string = expression_string.strip('() ')
        return cls.from_list(
            expression_string.split(' ', 2),
            pointer_registry,
            operator_registry,
        )

    @classmethod
    def from_list(
        cls,
        expression_list: List[Any],
        pointer_registry: ApiPointerRegistry,
        operator_registry: 'AbstractApiOperatorRegistry',
    ) -> 'ApiFilterExpression':
        if not isinstance(expression_list, list) or len(expression_list) != 3:
            raise ApiFilterExpressionError(
                'Unable to parse expression list. '
                'It must contain column key, operator key and value itself.',
            )

        column_pointer_key, operator_key, value = expression_list

        try:
            column_pointer = pointer_registry[column_pointer_key]

        except ApiPointerError as err:
            raise ApiFilterExpressionError(
                f'There is no model pointer with key {column_pointer_key!r}.',
            ) from err

        if column_pointer.sa_column is None:
            raise ApiFilterExpressionError(
                f'In filter expression list it is allowed to declare only '
                f'column, but {column_pointer_key!r} is a relationship.',
            )

        try:
            operator = operator_registry[operator_key]

        except KeyError as err:
            raise ApiFilterExpressionError(
                f'There is not operator {operator_key!r} in operator registry '
                f'list.',
            ) from err

        return cls(column_pointer, operator, value)

    def __eq__(self, other: Any) -> bool:
        try:
            return bool(
                self.pointer == other.pointer and
                self._operator == other.operator and
                self._value == other.value
            )
        except AttributeError:
            return False

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} ' \
               f'pointer={self.pointer!r} ' \
               f'operator={self._operator!r} ' \
               f'value={self._value!r}>'


_ExpressionType = Union[
    ApiFilterExpression,
    'ApiFilterExpressionGroup',
]


class ApiFilterExpressionGroup(Sequence[_ExpressionType]):
    """
    Api filter expression group, that are concatenated logically.
    """
    __slots__ = '_expressions', '_conjunction'

    def __init__(
        self,
        *expressions: _ExpressionType,
        conjunction: bool = True,
    ) -> None:
        self._conjunction = bool(conjunction)

        # ApiFilterExpression is not hashable, so current attribute is list,
        # not set.
        self._expressions: List[_ExpressionType] = []
        self.join(*expressions)

    def __len__(self) -> int:
        return len(self._expressions)

    @overload
    def __getitem__(self, index: int) -> _ExpressionType: ...

    @overload
    def __getitem__(self, index: slice) -> List[_ExpressionType]: ...

    def __getitem__(self, index):  # type: ignore[no-untyped-def]
        return self._expressions[index]

    def join(self, *expressions: _ExpressionType) -> None:
        for expression in expressions:
            assert isinstance(
                expression, (
                    ApiFilterExpression, ApiFilterExpressionGroup,
                ),
            )

            if expression not in self._expressions:
                self._expressions.append(expression)

    @property
    def expressions(self) -> List[_ExpressionType]:
        return self._expressions

    @property
    def conjunction(self) -> bool:
        return self._conjunction

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} ' \
               f'conjunction={"and" if self._conjunction else "or"!r} ' \
               f'expressions={self._expressions!r}>'

    def __eq__(self, other: Any) -> bool:
        try:
            return bool(
                self._conjunction == other.conjunction and
                self._expressions == other.expressions
            )
        except AttributeError:
            return False

    @property
    def sa_operator(self) -> Callable[...,  BooleanClauseList]:
        return cast(
            Callable[..., BooleanClauseList],
            and_ if self._conjunction else or_,
        )

    def compile(self, aliased_table_map: 'AliasedTableMap') -> Union[
        BooleanClauseList, BinaryExpression, None,
    ]:
        expressions = self._expressions
        if len(expressions) == 0:
            return None

        if len(expressions) == 1:
            # It is senselessly to apply operator on single expression.
            return self._expressions[0].compile(aliased_table_map)

        return self.sa_operator(
            *map(
                methodcaller('compile', aliased_table_map), self._expressions,
            ),
        )

    __call__ = compile

    @property
    def pointers(self) -> FrozenSet[ApiPointer]:

        def get_pointers() -> Iterator[ApiPointer]:
            for expression in self._expressions:

                if isinstance(expression, ApiFilterExpressionGroup):
                    yield from expression.pointers
                    continue

                yield expression.pointer

        return frozenset(get_pointers())

    @classmethod
    def create_or_unwrap(
        cls,
        *expressions: _ExpressionType,
        conjunction: bool = True,
    ) -> 'ApiFilterExpressionGroup':
        """Creation or returning filter expression group, if it declares
        singly."""
        if len(expressions) == 1 and isinstance(expressions[0], cls):
            return expressions[0]
        return cls(*expressions, conjunction=conjunction)
