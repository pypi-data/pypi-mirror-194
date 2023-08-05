from abc import ABCMeta, abstractmethod
from typing import Any, Generic
from weakref import ref

from sqlalchemy.sql import Select

from rest_collection.exc import RestCollectionReferenceError
from rest_collection.typing import ApiContextType
from ..container import JoinMap

__all__ = [
    'AbstractSaQueryModifier',
]


class AbstractSaQueryModifier(Generic[ApiContextType], metaclass=ABCMeta):
    """
    Модификатор запроса
    """
    __slots__ = '_data_ref', '_join_map_ref'

    def __init__(
        self,
        api_context: ApiContextType,
        join_map: JoinMap,
    ) -> None:
        self._data_ref = ref(api_context)
        self._join_map_ref = ref(join_map)

    @property
    def data(self) -> ApiContextType:
        data = self._data_ref()
        if data is None:
            raise RestCollectionReferenceError()
        return data

    @property
    def join_map(self) -> JoinMap:
        join_map = self._join_map_ref()
        if join_map is None:
            raise RestCollectionReferenceError()
        return join_map

    @abstractmethod
    def fill_join_map(self) -> None: ...

    @abstractmethod
    def modify(self, sa_query: Select, *args: Any, **kwargs: Any) -> Select: ...

    def __call__(self, *args: Any, **kwargs: Any) -> Select:
        return self.modify(*args, **kwargs)

    def __bool__(self) -> bool:
        return bool(self.data)
