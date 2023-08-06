import pathlib

from loxt_models.panel import PanelModel


class DeckModel:
    NAME: str
    ICON: pathlib.Path = None
    CONTEXT: str = 'any, any, visible ;'

    title: str = ''

    def __init__(self):
        self.panels: list[PanelModel] = list()

    def add_panel(self, panel):
        panel.order_index = len(self.panels) * 100 + 100
        self.panels.append(panel)
