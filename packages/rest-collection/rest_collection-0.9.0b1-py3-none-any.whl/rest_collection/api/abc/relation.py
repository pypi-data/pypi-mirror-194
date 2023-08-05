from abc import abstractmethod
from typing import Any, Dict
from weakref import WeakKeyDictionary

from .request import AbstractApiRequest, AbstractApiRequestContext
from ..pointer import ApiPointer

__all__ = [
    'AbstractApiRelationRequestContext',
]


class AbstractApiRelationRequestContext(AbstractApiRequestContext):

    __slots__ = ('_relation_pointers',)

    def __init__(self, request: AbstractApiRequest) -> None:
        self._relation_pointers: WeakKeyDictionary[
            ApiPointer, Any,
        ] = WeakKeyDictionary()
        super().__init__(request)

    @abstractmethod
    def _initialize(self) -> None: ...

    @property
    def relation_pointers(self) -> Dict[ApiPointer, bool]:
        return dict(self._relation_pointers)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} ({self.relation_pointers!r})'

    def __len__(self) -> int:
        return len(self._relation_pointers)

    def __bool__(self) -> bool:
        return len(self._relation_pointers) > 0
