from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional, Dict, Set, Any, Union

from pybi.utils.data_gen import Jsonable

from pybi.core.components import ComponentTag
from pybi.core.sql import Sql
from .base import ReactiveComponent
from pybi.core.dataSource import DataSourceView, DataSourceTable


if TYPE_CHECKING:
    from pybi.core.dataSource import DataSourceTable


class EChartSqlInfo(Jsonable):
    def __init__(self, seriesConfig: Dict, path: str, sql: Sql, chartType: str) -> None:
        self.path = path
        self._sql = sql
        self.chartType = chartType
        self.seriesConfig = seriesConfig

    def _to_json_dict(self):
        data = super()._to_json_dict()
        sql_data = self._sql._to_json_dict()

        data = {**data, **sql_data}
        return data


class EChartDatasetInfo(Jsonable):
    def __init__(self, seriesConfig: Dict, path: str, dataset: str) -> None:
        self.path = path
        self.dataset = dataset
        self.seriesConfig = seriesConfig


class EChartUpdateInfo(Jsonable):
    def __init__(
        self,
        action_type: str,
        value_type: str,
        table: str,
        field: str,
    ) -> None:
        """
        action_type : Literal["hover", "click"]
        value_type: Literal["x", "y", "value"]
        """
        super().__init__()
        self.actionType = action_type
        self.valueType = value_type
        self.table = table
        self.field = field


class EChart(ReactiveComponent):
    def __init__(self, options: Dict) -> None:

        super().__init__(ComponentTag.EChart)

        self._chart_mappings = {}
        self.options = options
        self._sqlInfos: List[EChartDatasetInfo] = []
        self._chartUpdateInfos: List[EChartUpdateInfo] = []
        self.height = "100%"

    def set_height(self, value: str):
        """
        15em:15字体大小
        300px:300像素
        """
        self.height = value
        return self

    def add_sql_path(self, info: EChartDatasetInfo):
        """
        add_sql_path('xAxis.data',"select distinct name from data")
        """
        self._sqlInfos.append(info)
        return self

    def hover_filter(
        self, value_type: str, table: Union[str, DataSourceTable], field: str
    ):
        """
        value_type: Literal["x", "y", "value"]
        """
        if isinstance(table, DataSourceTable):
            table = table.source_name

        self._chartUpdateInfos.append(
            EChartUpdateInfo("hover", value_type, table, field)
        )
        return self

    def _to_json_dict(self):
        self.options["series"] = []
        # EChart.remove_sql_from_option(self.options, self._sqlInfos)

        EChart.remove_legend_empty_data(self.options)
        EChart.remove_axis_empty_data(self.options)

        data = super()._to_json_dict()
        data["mapping"] = self._chart_mappings

        data["sqlInfos"] = self._sqlInfos
        data["updateInfos"] = self._chartUpdateInfos

        return data

    @staticmethod
    def remove_legend_empty_data(options: Dict):
        target = options
        if "legend" in target:
            target = options["legend"]
            if isinstance(target, list):
                target = target[0]
                if (
                    "data" in target
                    and isinstance(target["data"], list)
                    and len(target["data"]) == 0
                    or (not target["data"][0])
                ):
                    target["data"] = None

    @staticmethod
    def remove_axis_empty_data(options: Dict):
        def remove_fn(name: str):
            target = options
            if name not in target or target[name] is None:
                return

            if "data" in target[name][0]:
                axis = target[name][0]
                target = axis["data"]
                if (
                    isinstance(target, list)
                    and len(target) == 0
                    or (not target[0] == "")
                ):
                    axis["data"] = None
                    axis["type"] = "category"

        remove_fn("xAxis")
        remove_fn("yAxis")

    @staticmethod
    def extract_infos_from_option(opt: Dict):

        yield from EChart._extract_series_infos_from_option_(opt)
        return
        stack = [("", opt)]

        while len(stack) > 0:

            path, target = stack.pop()

            for key, value in target.items():
                if key != "series":
                    cur_path = f"{path}.{key}"

                    if isinstance(value, dict):
                        stack.append((cur_path, value))
                    elif isinstance(value, list):
                        for idx, v in enumerate(value):
                            if isinstance(v, dict):
                                stack.append((f"{cur_path}[{idx}]", v))
                    elif isinstance(value, (Sql, DataSourceView)):

                        if isinstance(value, DataSourceView):
                            value = Sql(value._to_sql())

                        yield EChartSqlInfo(cur_path[1:], value, "other")

    @staticmethod
    def _extract_series_infos_from_option_(opt: Dict):
        if "series" not in opt:
            return

        def extract_series(series: Dict, idx=-1):
            series_data = series["data"]
            if series["type"] in ["line", "pie", "bar"]:
                if isinstance(series_data, (Sql, DataSourceView)):
                    if isinstance(series_data, DataSourceView):
                        series_data = Sql(series_data._to_sql())

                    path = "series"
                    if idx > -1:
                        path = f"{path}[{idx}].data"

                    series["pybiFlag"] = None

                    yield EChartSqlInfo(series, path, series_data, series["type"])

        series = opt["series"]
        if isinstance(series, list):
            for idx, s in enumerate(series):
                yield from extract_series(s, idx)
        else:
            yield from extract_series(series)

    @staticmethod
    def _extract_dataset_infos_from_option_(opt: Dict):
        if "dataset" not in opt:
            return

        series = []
        if "series" in opt:
            series = opt["series"]

        def extract_ds(ds: Dict, series: List[Dict], idx=-1):
            if "source" not in ds:
                return

            source = ds["source"]

            if isinstance(source, (DataSourceTable)):

                path = "dataset"
                if idx > -1:
                    path = f"{path}[{idx}]"

                # series["pybiFlag"] = None

                if "data" in series[0]:
                    series[0]["data"] = None

                yield EChartDatasetInfo(series[0], path, source.source_name)

        dataset = opt["dataset"]
        assert isinstance(dataset, list)

        for idx, ds in enumerate(dataset):
            yield from extract_ds(ds, series, idx)

    @staticmethod
    def remove_sql_from_option(opt: Dict, infos: List[EChartDatasetInfo]):

        filterSeries = [series for series in opt["series"] if not "pybiFlag" in series]

        opt["series"] = filterSeries

        # for info in infos:
        #     paths = info.path.split(".")
        #     dictUtils.set_by_paths(paths, opt, None)
