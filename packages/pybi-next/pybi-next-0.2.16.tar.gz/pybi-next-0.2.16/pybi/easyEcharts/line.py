from __future__ import annotations
from .base import BaseChart
import pybi as pbi
import pybi.utils.sql as sqlUtils

from typing import TYPE_CHECKING, Optional
from pybi.core.components.reactiveComponent import EChartDatasetInfo

if TYPE_CHECKING:
    from pybi.core.dataSource import DataSourceTable


class LineChart(BaseChart):
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

    def stack(self):
        self._series_configs["stack"] = "Total"
        return self

    def area(self):
        """
        线以下区域填充颜色,使其成为区域图
        """
        self._series_configs["areaStyle"] = {}
        return self

    def get_options_infos(self):
        opts = super().get_options()

        opt_data = None
        if self.color:
            opt_data = self.data.to_pivot(
                row=self.x, column=self.color, cell=self.y, agg=self.agg
            )
        else:
            agg_field = sqlUtils.apply_agg(self.agg, self.y)
            opt_data = pbi.set_dataView(
                f"select `{self.x}`,{agg_field} from {self.data} group by `{self.x}`"
            )

        series_config = {"type": "line"}
        series_config.update(self._series_configs)

        ds_info = EChartDatasetInfo(series_config, "dataset[0]", opt_data.source_name)

        opts["xAxis"] = [
            {
                "type": "category",
                "boundaryGap": False,
            }
        ]

        opts["yAxis"] = [{"type": "value"}]

        opts["tooltip"] = {
            "trigger": "axis",
            "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}},
        }

        return opts, [ds_info]
