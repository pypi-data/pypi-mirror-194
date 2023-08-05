from abc import ABCMeta
from typing import Any, FrozenSet, Optional, Set, Tuple, overload
from weakref import ReferenceType, WeakSet, ref

from sqlalchemy import Column
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import RelationshipProperty

from .identity import ApiIdentity
from ..exc import ApiTypeError

__all__ = [
    'ApiPointer',
]


@overload
def _make_ref_or_none(value: None) -> None: ...


@overload
def _make_ref_or_none(value: 'ApiPointer') -> ReferenceType['ApiPointer']: ...


def _make_ref_or_none(value):  # type: ignore[no-untyped-def]
    if value is None:
        return
    return ref(value)

@overload
def _resolve_ref_or_none(ref_: None) -> None: ...


@overload
def _resolve_ref_or_none(ref_: ReferenceType['ApiPointer']) -> 'ApiPointer': ...


def _resolve_ref_or_none(ref_):  # type: ignore[no-untyped-def]
    if ref_ is None:
        return
    return ref_()


class ApiPointer(metaclass=ABCMeta):
    """
    API pointer container, that associates string identity of ORM model and
    ORM model itself.
    """
    __slots__ = (
        '_identity',
        '_sa_column',
        '_sa_relationship',
        '_sa_cls',
        '_parent_ref',
        '_childs_refs',
        '__weakref__',
    )

    def __init__(  # pylint: disable=too-many-arguments
        self,
        identity: ApiIdentity,
        sa_cls: DeclarativeMeta,
        sa_column: Optional[Column],
        sa_relationship: Optional[RelationshipProperty],
        parent: Optional['ApiPointer'] = None,
        childs: Optional[Set['ApiPointer']] = None,
    ) -> None:
        self._identity = identity
        self._sa_column = sa_column
        self._sa_relationship = sa_relationship
        self._sa_cls = sa_cls
        self._parent_ref = _make_ref_or_none(parent)
        self._childs_refs: WeakSet['ApiPointer'] = WeakSet(childs)

    def __repr__(self) -> str:
        return f'<ApiPointer (identity={self._identity})>'

    @property
    def identity(self) -> ApiIdentity:
        return self._identity

    @property
    def sa_column(self) -> Optional[Column]:
        return self._sa_column

    @property
    def sa_relationship(self) -> Optional[RelationshipProperty]:
        return self._sa_relationship

    @property
    def sa_cls(self) -> DeclarativeMeta:
        return self._sa_cls

    @property
    def parents(self) -> Tuple['ApiPointer', ...]:
        """Parent pointers chain (ordered from top parents to self parent)."""
        parent = self.parent

        if parent is None:
            return ()

        return parent.parents + (parent,)

    @property
    def parent(self) -> Optional['ApiPointer']:
        """Parent pointer."""
        return _resolve_ref_or_none(self._parent_ref)

    @property
    def childs(self) -> FrozenSet['ApiPointer']:
        """Child pointers."""
        return frozenset(self._childs_refs)

    def add_child(self, api_pointer: 'ApiPointer') -> None:
        self._childs_refs.add(api_pointer)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            raise ApiTypeError(
                f'Comparison with object of {self.__class__.__name__!r} '
                f'allowed.',
            )
        return self._identity == other.identity

    def __hash__(self) -> int:
        return hash(self._identity)
