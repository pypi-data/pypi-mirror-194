from abc import abstractmethod
from typing import Any, FrozenSet, Optional, Union

from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList

from .request import AbstractApiRequest, AbstractApiRequestContext
from ..alias import AliasedTableMap
from ..filter import ApiFilterExpressionGroup, ApiFilterParser
from ..pointer import ApiPointer

__all__ = [
    'AbstractApiFilterRequestContext',
]


class AbstractApiFilterRequestContext(AbstractApiRequestContext):

    __slots__ = '_data', '_parser'

    def __init__(self, request: AbstractApiRequest) -> None:
        self._data: Optional[ApiFilterExpressionGroup] = None
        self._parser = ApiFilterParser(
            request.pointer_registry,
            request.operator_registry,
        )
        super().__init__(request)

    @property
    def data(self) -> Optional[ApiFilterExpressionGroup]:
        return self._data

    @property
    def pointers(self) -> Optional[FrozenSet[ApiPointer]]:
        data = self._data
        if data is not None:
            return data.pointers

    @abstractmethod
    def _initialize(self) -> None: ...

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} (data={self._data!r})'

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and other.data == self._data

    def __bool__(self) -> bool:
        return self._data is not None

    def compile(self, aliased_table_map: AliasedTableMap) -> Union[
        BooleanClauseList, BinaryExpression, None,
    ]:
        data = self._data
        if data is not None:
            return data.compile(aliased_table_map)
