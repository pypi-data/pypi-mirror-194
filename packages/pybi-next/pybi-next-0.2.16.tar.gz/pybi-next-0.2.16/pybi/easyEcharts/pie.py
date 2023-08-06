from __future__ import annotations
from .base import BaseChart
import pybi as pbi
import pybi.utils.sql as sqlUtils

from typing import TYPE_CHECKING, Optional
from pybi.core.components.reactiveComponent import EChartDatasetInfo

if TYPE_CHECKING:
    from pybi.core.dataSource import DataSourceTable


class PieChart(BaseChart):
    def __init__(
        self,
        data: DataSourceTable,
        name: str,
        value: str,
        agg="round(avg(${}),2)",
    ):
        super().__init__()
        self.data = data
        self.name = name
        self.value = value
        self.agg = agg
        self._series_configs = {}

    def radius(self, value=["40%", "70%"]):
        """
        设置圆环图颜色。
        参考资料:https://echarts.apache.org/zh/option.html#series-pie.radius
        """
        self._series_configs["radius"] = value
        self._series_configs["avoidLabelOverlap"] = False
        self._series_configs["label"] = {"show": False, "position": "center"}
        self._series_configs["labelLine"] = {"show": False}
        self._series_configs["emphasis"] = {
            "label": {"show": True, "fontSize": "2em", "fontWeight": "bold"}
        }

        return self

    def get_options_infos(self):
        opts = super().get_options()

        agg_field = sqlUtils.apply_agg(self.agg, self.value)
        opt_data = pbi.set_dataView(
            f"select `{self.name}`,{agg_field} from {self.data} group by `{self.name}`"
        )

        series_config = {
            "type": "pie",
            "radius": "50%",
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": "rgba(0, 0, 0, 0.5)",
                }
            },
        }

        series_config.update(self._series_configs)

        ds_info = EChartDatasetInfo(series_config, "dataset[0]", opt_data.source_name)

        opts["xAxis"] = None

        opts["yAxis"] = None

        opts["tooltip"] = {"trigger": "item"}

        return opts, [ds_info]
