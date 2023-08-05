from itertools import count
from operator import itemgetter
from typing import Hashable, Iterator, MutableMapping, TypeVar
from weakref import WeakKeyDictionary, WeakValueDictionary

__all__ = [
    'WeakKeyOrderedDict',
]


_KeyType = TypeVar('_KeyType', bound=Hashable)
_ValueType = TypeVar('_ValueType')


class WeakKeyOrderedDict(MutableMapping[_KeyType, _ValueType]):

    __slots__ = '_data', '_keys', '_key_count'

    def __init__(self) -> None:
        self._key_count = count()
        self._keys: WeakValueDictionary[int, _KeyType] = WeakValueDictionary()
        self._data: WeakKeyDictionary[
            _KeyType, _ValueType,
        ] = WeakKeyDictionary()

    def __getitem__(self, key: _KeyType) -> _ValueType:
        return self._data[key]

    def __setitem__(self, key: _KeyType, value: _ValueType) -> None:
        key_key = next(self._key_count)
        self._keys[key_key] = key
        self._data[key] = value

    def __delitem__(self, key: _KeyType) -> None:
        del self._data[key]

        key_key_to_delete = None

        for key_key, key_value in self._keys.items():
            if key_value == key:
                key_key_to_delete = key_key
                break

        if key_key_to_delete is not None:
            del self._keys[key_key_to_delete]

    def __iter__(self) -> Iterator[_KeyType]:
        return iter(
            map(itemgetter(1), sorted(self._keys.items(), key=itemgetter(0))),
        )

    def __len__(self) -> int:
        return len(self._data)
