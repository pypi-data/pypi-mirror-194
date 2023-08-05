from contextlib import closing
from typing import Any, List, Optional

from sqlalchemy import func, select
from sqlalchemy.engine import Engine
from sqlalchemy.engine.row import Row

from .abc import AbstractSqlalchemySelector
from .mixin import SqlalchemySelectorMixin

__all__ = [
    'SqlalchemySelector',
]


class SqlalchemySelector(
    SqlalchemySelectorMixin,
    AbstractSqlalchemySelector[Engine],
):
    """Sync selector."""
    __slots__ = ()

    def select(self, *args: Any, **kwargs: Any) -> List[Row]:
        sa_query = self.get_query()

        with closing(self._sa_engine.connect()) as conn:
            return conn.execute(sa_query).fetchall()

    def count(self, *args: Any, **kwargs: Any) -> Optional[int]:
        sa_query = self.get_query(for_counting=True)
        sa_query = select(func.count()).select_from(sa_query.alias())

        with closing(self._sa_engine.connect()) as conn:
            return conn.execute(sa_query).scalar()
