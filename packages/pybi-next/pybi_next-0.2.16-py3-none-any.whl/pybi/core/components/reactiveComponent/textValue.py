from __future__ import annotations
from typing import TYPE_CHECKING, List, Union


from pybi.core.components import ComponentTag
from pybi.core.sql import Sql
from .base import ReactiveComponent
import re


if TYPE_CHECKING:
    pass

m_sql_from_text_pat = re.compile(r"(?:sql:\[_\s)(.+?)(?:\s_])", re.I)


class TextValue(ReactiveComponent):
    def __init__(self, contexts: List[Union[str, Sql]]) -> None:
        super().__init__(ComponentTag.TextValue)
        self.contexts = contexts

    @staticmethod
    def extract_sql_from_text(text: str):
        """
        >>> input = '总销售额:sql:[_ select sum(销售额) from data _]'
        >>> extract_sql_from_text(input)
        >>> ['总销售额:',Sql('select sum(销售额) from data')]
        """
        start_idx = 0

        for match in re.finditer(m_sql_from_text_pat, text):

            span = match.span()

            if span[0] > start_idx:
                # 前面有普通文本
                yield text[start_idx : span[0]]

            yield Sql(match.group(1))
            start_idx = span[1]

        end_idx = len(text) - 1

        if start_idx < end_idx:
            yield text[start_idx : len(text)]
