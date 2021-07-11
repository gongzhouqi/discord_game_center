import itertools
import random

from core.Games.utils.PokerCard import Card


class Deck:
    STANDARD_52 = 0
    WILD_CARDS_54 = 1
    ALL_PRESETS = [STANDARD_52, WILD_CARDS_54]

    @staticmethod
    def generate_deck(contents):
        cards = []
        for preset_type in contents:
            assert preset_type in Deck.ALL_PRESETS
            sub_deck = Deck.get_52()
            for card in sub_deck:
                cards.append(card)
            if preset_type == Deck.WILD_CARDS_54:
                cards.append(Card(Card.JOKER, Card.LARGE))
                cards.append(Card(Card.JOKER, Card.SMALL))
        deck = Deck()
        deck.cards = cards
        return deck

    def __init__(self):
        self.cards = []

    @staticmethod
    def get_52():
        comb = list(itertools.product(Card.NORMAL_COLORS, Card.NORMAL_NUMBERS))
        all_cards = [Card(c, n) for c, n in comb]
        return all_cards

    def touch(self):
        card = self.cards.pop(0)
        return card

    def shuffle(self):
        random.shuffle(self.cards)

    def add_card(self, card: Card):
        assert type(card) == Card
        self.cards.append(card)
