from pybi.core.components.component import Component
from .componentTag import ComponentTag


class TextComponent(Component):
    def __init__(self, content: str) -> None:
        super().__init__(ComponentTag.Text)
        self.content = content


class UploadComponent(Component):
    def __init__(self) -> None:
        super().__init__(ComponentTag.Upload)
