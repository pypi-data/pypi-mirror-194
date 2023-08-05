from itertools import zip_longest
from typing import Any, Generic, Iterator, Optional, Sequence, TYPE_CHECKING, \
    Tuple, TypeVar, overload

from rest_collection.container import Chunked
from .container import ApiParam
from .schema import ApiContextParamSchema

if TYPE_CHECKING:
    from ..abc import AbstractApiRequest


__all__ = [
    'ApiContextParams',
    'ApiContextParamBlocks',
]


_ApiContextParamsDataType = TypeVar(
    '_ApiContextParamsDataType', bound=Tuple[Any, ...],
)


class _BaseApiContextParams(  # pylint: disable=too-few-public-methods
    Generic[_ApiContextParamsDataType],
):
    __slots__ = '_data', '_schema'

    def __init__(
        self,
        request: 'AbstractApiRequest',
        url_param_schema: ApiContextParamSchema,
    ) -> None:
        # pylint: disable=import-outside-toplevel
        from ..abc import AbstractApiRequest
        assert isinstance(request, AbstractApiRequest)
        assert isinstance(url_param_schema, ApiContextParamSchema)

        self._schema = url_param_schema
        self._data = self._get_data(request)

    def _get_data(
        self,
        request: 'AbstractApiRequest',
    ) -> _ApiContextParamsDataType:
        url_params = tuple(
            filter(
                lambda x: x.name in self._schema, request.params,
            ),
        )

        for url_param in url_params:
            self._schema.normalize(url_param)

        return url_params  # type: ignore[return-value]


class ApiContextParams(
    _BaseApiContextParams[Tuple[ApiParam[Any], ...]],
    Sequence[ApiParam[Any]],
):
    """Representation of sequence of API params."""
    __slots__ = ()

    @overload
    def __getitem__(self, index: int) -> ApiParam[Any]: ...

    @overload
    def __getitem__(self, index: slice) -> Tuple[ApiParam[Any], ...]: ...

    def __getitem__(self, index):  # type: ignore[no-untyped-def]
        return self._data[index]

    def __len__(self) -> int:
        return len(self._data)

    def _filter(self, param_name: str) -> Iterator[ApiParam[Any]]:
        return filter(lambda x: x.name == param_name, self._data)

    def get_only(self, param_name: str) -> Tuple[ApiParam[Any], ...]:
        return tuple(self._filter(param_name))

    def get_first(self, param_name: str) -> Optional[ApiParam[Any]]:
        try:
            return next(self._filter(param_name))
        except StopIteration:
            pass


class ApiContextParamBlocks(
    _BaseApiContextParams[
        Tuple[Tuple[ApiParam[Any], ...], ...]
    ],
    Sequence[Tuple[ApiParam[Any], ...]],
):
    """Representation of block of API params."""
    __slots__ = ()

    def _get_data(
        self,
        request: 'AbstractApiRequest',
    ) -> Tuple[Tuple[ApiParam[Any], ...], ...]:
        url_params = super()._get_data(request)

        chunked_url_params = Chunked(
            lambda url_param: url_param.name == self._schema.first_node.name,
            url_params,
        )

        return tuple(
            tuple(
                ApiParam(
                    node.main, node.block_default,
                ) if url_param is None else url_param

                for url_param, node in zip_longest(
                    url_params_chunk, self._schema.nodes,
                )
            ) for url_params_chunk in chunked_url_params
        )

    @overload
    def __getitem__(self, index: int) -> Tuple[
        ApiParam[Any], ...
    ]: ...

    @overload
    def __getitem__(self, index: slice) -> Tuple[
        Tuple[ApiParam[Any], ...], ...
    ]: ...

    def __getitem__(self, index):  # type: ignore[no-untyped-def]
        return self._data[index]

    def __len__(self) -> int:
        return len(self._data)
