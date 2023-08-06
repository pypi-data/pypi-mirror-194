from __future__ import annotations
from .line import LineChart
from .bar import BarChart
from .pie import PieChart
from .scatter import ScatterChart
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from pybi.core.dataSource import DataSourceTable


__all__ = ["easy_echarts"]


class EasyEChartsMeta:
    def make_line(
        self,
        data: DataSourceTable,
        x: str,
        y: str,
        color: Optional[str] = None,
        agg="round(avg(${}),2)",
    ):
        return LineChart(data, x, y, color, agg)

    def make_bar(
        self,
        data: DataSourceTable,
        *,
        x: str,
        y: str,
        color: Optional[str] = None,
        agg="round(avg(${}),2)",
    ):
        return BarChart(data, x, y, color, agg)

    def make_pie(
        self,
        data: DataSourceTable,
        *,
        name: str,
        value: str,
        agg="round(avg(${}),2)",
    ):
        return PieChart(data, name, value, agg)

    def make_scatter(
        self,
        data: DataSourceTable,
        *,
        x: str,
        y: str,
        color: Optional[str] = None,
        agg="round(avg(${}),2)",
    ):
        return ScatterChart(data, x, y, color, agg)


easy_echarts = EasyEChartsMeta()
