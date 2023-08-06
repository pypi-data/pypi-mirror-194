from __future__ import annotations
from typing import TYPE_CHECKING, List, Union


from pybi.core.components import ComponentTag
from pybi.core.sql import Sql
from .base import SingleReactiveComponent


if TYPE_CHECKING:
    pass


class Table(SingleReactiveComponent):
    def __init__(
        self,
        sql: Sql,
    ) -> None:
        super().__init__(ComponentTag.Table, sql)
