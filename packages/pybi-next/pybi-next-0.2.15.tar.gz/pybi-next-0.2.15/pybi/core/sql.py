import pybi.utils.sql as sqlUtils
from pybi.utils.data_gen import Jsonable


class Sql(Jsonable):
    def __init__(self, sql: str) -> None:
        self.sql = sql

    def get_table_names(self):
        return sqlUtils.extract_table_names(self.sql)

    def __str__(self) -> str:
        return f"sql:[_ {self.sql} _]"

    def _to_json_dict(self):
        data = super()._to_json_dict()
        return data
