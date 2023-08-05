from typing import Iterable, Iterator, Tuple, TypeVar, Union

__all__ = [
    'ApiParam',
]


_ValueType = TypeVar('_ValueType')


class ApiParam(Iterable[_ValueType]):
    """Representation of API param."""
    __slots__ = 'name', 'value'

    def __init__(self, name: str, value: _ValueType) -> None:
        self.name = name.lower().strip()
        self.value = value

    @property
    def key(self) -> str:
        return self.name

    @key.setter
    def key(self, value: str) -> None:
        self.name = value

    def __iter__(self) -> Iterator[  # type: ignore[override]
        Union[str, _ValueType]
    ]:
        yield self.name
        yield self.value

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__} '
            f'name={self.name!r} '
            f'value={self.value!r}>'
        )

    @classmethod
    def from_tuple(
        cls,
        tuple_: Tuple[str, _ValueType],
    ) -> 'ApiParam[_ValueType]':
        return cls(*tuple_)
