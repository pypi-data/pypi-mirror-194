from __future__ import annotations
from typing import TYPE_CHECKING, List, Union


from pybi.core.components import ComponentTag
from pybi.core.sql import Sql
from .base import SingleReactiveComponent


if TYPE_CHECKING:
    pass


class Slicer(SingleReactiveComponent):
    def __init__(self, sql: Sql) -> None:
        super().__init__(ComponentTag.Slicer, sql)
        self.title = ""
        self.multiple = True

    def set_title(self, title: str):
        self.title = title
        return self

    def set_multiple(self, multiple: bool):
        self.multiple = multiple
        return self
