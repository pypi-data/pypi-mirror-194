from __future__ import annotations
from .base import BaseChart
import pybi as pbi

from typing import TYPE_CHECKING, Optional
from pybi.core.components.reactiveComponent import EChartDatasetInfo

if TYPE_CHECKING:
    from pybi.core.dataSource import DataSourceTable


class ScatterChart(BaseChart):
    def __init__(
        self,
        data: DataSourceTable,
        x: str,
        y: str,
        color: Optional[str] = None,
        agg="round(avg(${}),2)",
    ):
        super().__init__()
        self.data = data
        self.x = x
        self.y = y
        self.color = color
        self.agg = agg
        self._series_configs = {}

    def get_options_infos(self):
        opts = super().get_options()

        opt_data = None
        if self.color:
            opt_data = pbi.set_dataView(
                f"select `{self.color}`,`{self.x}`,`{self.y}` from {self.data}"
            )
        else:
            opt_data = pbi.set_dataView(
                f"select 1,`{self.x}`,`{self.y}` from {self.data}"
            )

        series_config = {
            "type": "scatter",
        }

        series_config.update(self._series_configs)

        ds_info = EChartDatasetInfo(series_config, "dataset[0]", opt_data.source_name)

        opts["xAxis"] = [{}]

        opts["yAxis"] = [{}]

        opts["tooltip"] = {"trigger": "item"}

        return opts, [ds_info]
