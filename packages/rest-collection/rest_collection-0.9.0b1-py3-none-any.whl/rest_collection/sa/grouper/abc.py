from abc import ABCMeta, abstractmethod
from collections import OrderedDict, defaultdict
from typing import Any, DefaultDict, Dict, Hashable, Mapping, MutableMapping, \
    Sequence, \
    Tuple

__all__ = [
    'AbstractGrouper',
]


class AbstractGrouper(metaclass=ABCMeta):
    __slots__ = ()

    def group(
        self,
        data: Sequence[Sequence[Any]],
    ) -> Dict[str, Tuple[Dict[str, Any], ...]]:
        grouped: DefaultDict[
            str,
            OrderedDict[Tuple[Hashable, ...], Dict[str, Any]],
        ] = defaultdict(
            OrderedDict,
        )

        for row in data:
            self.group_row(row, grouped)

        return {
            k: tuple(v.values()) for k, v in grouped.items()
        }

    __call__ = group

    @abstractmethod
    def group_row(
        self,
        row: Sequence[Any],
        grouped: Mapping[
            str,
            MutableMapping[Tuple[Hashable, ...], Dict[str, Any]]
        ],
    ) -> None: ...
