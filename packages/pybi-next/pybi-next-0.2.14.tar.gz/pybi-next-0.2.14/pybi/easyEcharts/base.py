from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Tuple, List, Sequence


if TYPE_CHECKING:
    from pybi.core.components.reactiveComponent import EChartDatasetInfo


m_merge_keys = set(["tooltip", "legend", "title", "grid"])


class BaseChart:
    def __init__(self) -> None:
        self.__base_opt = {
            "tooltip": {},
            "legend": {},
            "series": [],
            "title": {},
            "grid": {"containLabel": True},
        }
        self.__merge_opt = {}

    def merge(self, options: Dict):
        self.__merge_opt = options
        return self

    def get_options(self):
        return {
            **self.__base_opt,
            **{k: v for k, v in self.__merge_opt.items() if k in m_merge_keys},
        }

    def set_title(self, text: str):
        opt_title: Dict = self.__base_opt["title"]
        opt_title["text"] = text

        return self

    def get_options_infos(self) -> Tuple[Dict, Sequence[EChartDatasetInfo]]:
        raise NotImplementedError
