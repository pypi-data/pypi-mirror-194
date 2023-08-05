from contextlib import suppress
from typing import Any, List, Optional, cast

from sqlalchemy import func, select

from .abc import AbstractAsyncSqlalchemySelector
from .mixin import SqlalchemySelectorMixin

__all__ = [

]

# mypy: disable-error-code=no-untyped-call


with suppress(ImportError):
    # We don`t know was aiopg installed or not.
    # So, we suppress ImportError if not.
    from aiopg.sa import Engine
    from aiopg.sa.result import ResultProxy, RowProxy

    __all__.append('AiopgSqlalchemySelector')


    class AiopgSqlalchemySelector(
        SqlalchemySelectorMixin,
        AbstractAsyncSqlalchemySelector[Engine],
    ):
        """Async aiopg-based selector."""
        __slots__ = ()

        async def select(self, *args: Any, **kwargs: Any) -> List[RowProxy]:
            sa_query = self.get_query()

            async with self._sa_engine.acquire() as conn:
                result_proxy: ResultProxy = await conn.execute(sa_query)
                return cast(
                    List[RowProxy],
                    await result_proxy.fetchall(),
                )

        async def count(self, *args: Any, **kwargs: Any) -> Optional[int]:
            sa_query = self.get_query(for_counting=True)
            sa_query = select(func.count()).select_from(sa_query.alias())

            async with self._sa_engine.acquire() as conn:
                result_proxy: ResultProxy = await conn.execute(sa_query)
                return cast(
                    Optional[int],
                    await result_proxy.scalar(),
                )
