from loxt_models.deck import DeckModel


class SidebarModel:

    def __init__(self):
        self.decks: list[DeckModel] = list()

    def add_deck(self, deck: DeckModel):
        self.decks.append(deck)
