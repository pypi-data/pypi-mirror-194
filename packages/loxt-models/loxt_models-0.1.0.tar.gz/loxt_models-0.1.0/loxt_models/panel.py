from typing import Optional

from loxt_models.deck import DeckModel


class PanelModel:
    NAME: str
    ORDER_INDEX: int
    CONTEXT: str = 'any, any, visible ;'

    title: str = ''
    default_menu_command: str = None
    wants_canvas: bool = False

    def __init__(self):
        self.FACTORY_NAME: str = f"{self.NAME}_factory"
        self.deck: Optional[DeckModel] = None
