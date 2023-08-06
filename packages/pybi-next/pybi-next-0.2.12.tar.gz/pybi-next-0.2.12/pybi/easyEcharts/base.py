from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Tuple, List, Sequence


if TYPE_CHECKING:
    from pybi.core.components.reactiveComponent import EChartDatasetInfo


class BaseChart:
    def merge(self, options: Dict):
        pass

    def get_options(self):
        return {"tooltip": {}, "legend": {}, "series": []}

    def get_options_infos(self) -> Tuple[Dict, Sequence[EChartDatasetInfo]]:
        raise NotImplementedError
