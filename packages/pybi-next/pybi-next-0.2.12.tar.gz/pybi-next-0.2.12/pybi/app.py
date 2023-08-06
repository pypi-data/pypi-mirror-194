from __future__ import annotations
from pathlib import Path

from pybi.core import DataSource
import pandas as pd

from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Union, Any
import os

from pybi.core.components import (
    ContainerComponent,
    ColBoxComponent,
    ComponentTag,
    BoxComponent,
    FlowBoxComponent,
    TextComponent,
    UploadComponent,
    GridBoxComponent,
    TabsComponent,
)
from pybi.core.components.reactiveComponent import EChart, Slicer, Table, TextValue
from pybi.core.dataSource import (
    DataSourceField,
    DataSourceTable,
    DataView,
    DataViewBase,
    PivotDataView,
)
from pybi.utils.dataSourceUtils import ds2sqlite_file_base64, ds2sqlite
from pybi.utils.data_gen import (
    json_dumps_fn,
    random_ds_name,
    random_dv_name,
    get_project_root,
)
from pybi.core.sql import Sql
import pybi.utils.sql as sqlUtils
from pybi.easyEcharts.base import BaseChart

if TYPE_CHECKING:
    pass
    # from pybi.core.components import ReactiveComponent


class AppMeta:
    def __init__(self, app: App) -> None:
        self.__app = app

    def set_dbLocalStorage(self, on: bool):
        """
        是否开启数据库本地缓存
        """
        self.__app.dbLocalStorage = on
        return self

    def set_echarts_renderer(self, renderer="canvas"):
        """
        echarts renderer type: 'canvas' or 'svg'
        'canvas' is default
        """
        self.__app.echartsRenderer = renderer
        return self


class App(ContainerComponent):
    def __init__(self) -> None:
        super().__init__(ComponentTag.App)
        self.dataSources: List[DataSource] = []
        self.dataViews: List[DataViewBase] = []
        self.__dataSetNames = set()
        self._with_temp_host_stack: List[ContainerComponent] = []
        self._clear_data = False
        self.dbLocalStorage = False
        self.echartsRenderer = "canvas"
        self.__meta = AppMeta(self)

    def __record_and_check_dataset_name(self, name: str):
        if name in self.__dataSetNames:
            raise Exception(f"dataset name '{name}' is duplicate")
        self.__dataSetNames.add(name)

    @property
    def meta(self):
        return self.__meta

    def clear_all_data(self):
        self._clear_data = True

    def _get_temp_host(self):
        if self._with_temp_host_stack:
            return self._with_temp_host_stack[len(self._with_temp_host_stack) - 1]
        return None

    def set_source(self, data: pd.DataFrame, *, name: Optional[str] = None):
        name = name or random_ds_name()
        self.__record_and_check_dataset_name(name)

        ds = DataSource(name, data)
        self.dataSources.append(ds)
        return DataSourceTable(ds.name, data.columns.tolist(), host=self)

    def set_dataView(
        self,
        sql: str,
        exclude_source: Optional[List[DataSourceTable]] = None,
        *,
        name: Optional[str] = None,
    ):
        exclude_source = exclude_source or []
        name = name or random_dv_name()
        self.__record_and_check_dataset_name(name)
        dv = DataView(name, Sql(sql))

        for es in exclude_source:
            dv.exclude_source(es.source_name)

        self.dataViews.append(dv)
        return DataSourceTable(
            dv.name, sqlUtils.extract_fields_head_select(sql), host=self
        )

    def set_pivot_dataView(
        self,
        source: str,
        row: str,
        column: str,
        cell: str,
        agg="min",
        exclude_source: Optional[List[DataSourceTable]] = None,
        excludeRowFields=False,
        *,
        name: Optional[str] = None,
    ):
        exclude_source = exclude_source or []
        name = name or random_dv_name()
        self.__record_and_check_dataset_name(name)
        pdv = PivotDataView(name, source, row, column, cell, agg, excludeRowFields)

        for es in exclude_source:
            pdv.exclude_source(es.source_name)

        self.dataViews.append(pdv)
        return DataSourceTable(pdv.name, [], host=self)

    def add_upload(
        self,
        *,
        host: Optional[ContainerComponent] = None,
    ):

        cp = UploadComponent()

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        return cp

    def add_text(
        self,
        text: str,
        *,
        host: Optional[ContainerComponent] = None,
    ):

        contexts = list(TextValue.extract_sql_from_text(text))

        cp = TextValue(contexts)

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        return cp

    def add_slicer(
        self,
        field: Union[DataSourceField, DataSourceTable],
        *,
        host: Optional[ContainerComponent] = None,
    ):
        if isinstance(field, DataSourceTable):
            field = field[field.columns[0]]

        assert isinstance(field, DataSourceField)
        sql = f"select distinct {field._get_sql_field_name()} from {field.source_name}"
        cp = Slicer(Sql(sql))
        cp.title = field.name
        cp.add_updateInfo(field.source_name, field._get_sql_field_name())

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        return cp

    def add_table(
        self,
        dataSourceTable: DataSourceTable,
        *,
        host: Optional[ContainerComponent] = None,
    ):

        sql = f"select {dataSourceTable.get_sql_fields()} from {dataSourceTable.source_name}"
        cp = Table(Sql(sql))

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        return cp

    def add_echart(
        self,
        options: Union[Dict, BaseChart],
        *,
        host: Optional[ContainerComponent] = None,
    ):
        cp = None

        if isinstance(options, BaseChart):
            opts, infos = options.get_options_infos()
            cp = EChart(opts)

            for info in infos:
                cp.add_sql_path(info)
        else:
            cp = EChart(options)

            for info in EChart._extract_dataset_infos_from_option_(options):
                cp.add_sql_path(info)

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        return cp

    def flowBox(
        self,
        *,
        host: Optional[ContainerComponent] = None,
    ):
        cp = FlowBoxComponent(self)

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        return cp

    def gridBox(
        self,
        areas: Union[List[List[str]], str],
        *,
        host: Optional[ContainerComponent] = None,
    ):
        if isinstance(areas, str):
            areas = GridBoxComponent.areas_str2array(areas)

        cp = GridBoxComponent(areas, self)

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        return cp

    def colBox(
        self,
        spec: List[int] | None = None,
        *,
        host: Optional[ContainerComponent] = None,
    ):
        cp = ColBoxComponent(spec, self)

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        return cp

    def box(
        self,
        *,
        host: Optional[ContainerComponent] = None,
    ):
        cp = BoxComponent(self)
        host = host or self._get_temp_host() or self
        host._add_children(cp)
        return cp

    def add_tabs(
        self,
        names: List[str],
        mode="narrowing",
        *,
        host: Optional[ContainerComponent] = None,
    ):
        """
        mode: 'fullWidth' | 'narrowing'
            fullWidth:全宽度;页签栏会横向撑满屏幕宽度
            narrowing(默认值):收窄;页签栏向左靠拢
        """
        cp = TabsComponent(names, mode, appHost=self)
        host = host or self._get_temp_host() or self
        host._add_children(cp)
        return cp

    def save_zip_db(self, path: str):
        with open(path, mode="w", encoding="utf8") as f:
            f.write(ds2sqlite_file_base64(self.dataSources))

    def save_db(self, path: str):
        if Path(path).exists():
            os.remove(path)
        ds2sqlite(path, self.dataSources)

    def _to_json_dict(self):
        data = super()._to_json_dict()

        data["dbFile"] = ds2sqlite_file_base64(
            self.dataSources, clear_data=self._clear_data
        )
        return data

    def __reset_data(self):
        """support for run on ipython env"""
        self.children = []
        self.dataSources = []
        self.dataViews = []

    def to_json(self):
        return json_dumps_fn(self, indent=2, ensure_ascii=False)

    def to_raw_html(self):
        try:
            symbol = '"__{{__config_data__}}___"'

            config = json_dumps_fn(self, ensure_ascii=False)

            with open(
                get_project_root() / "template/index.html", mode="r", encoding="utf8"
            ) as html:
                res = html.read().replace(symbol, config)
                return res
        except Exception as e:
            raise e
        else:
            self.__reset_data()

    def to_html(self, file):
        try:
            file = Path(file)
            raw = self.to_raw_html()
            Path(file).write_text(raw, "utf8")

            print(f"to html:{file.absolute()}")
        except Exception as e:
            raise e
        else:
            self.__reset_data()
