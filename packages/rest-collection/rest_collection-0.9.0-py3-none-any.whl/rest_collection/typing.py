from typing import Callable, TypeVar, Union

from sqlalchemy import Column, Table
from sqlalchemy.sql import Alias
from sqlalchemy.sql.elements import BinaryExpression, Label

__all__ = [
    'ApiOperatorType',
    'TableLikeType',
    'ColumnLikeType',
    'SelectableElementType',
    'SaEngineType',
    'ApiContextType',
]

ApiOperatorType = Callable[..., BinaryExpression]

TableLikeType = Union[Table, Alias]
ColumnLikeType = Union[Column, Label]
SelectableElementType = Union[TableLikeType, ColumnLikeType]

SaEngineType = TypeVar('SaEngineType')
ApiContextType = TypeVar('ApiContextType')
