from .card import Card


class Deck:
    def __init__(self):
        self.cards = []

    def add_card(self, question: str, answer: str):
        self.cards.append(Card(question, answer))
        return self

    def add_card_from_list(self, add: [str]):
        """:param add list of two strings formatted [question, answer]"""
        self.cards.append(Card(add[0], add[1]))
        return self

    def add_card_from_obj(self, add: Card):
        self.cards.append(add)
        return self

    def print(self):
        """Print each question: answer in the deck"""
        for card in self.cards:
            print(f"{card.question}: {card.answer}")
