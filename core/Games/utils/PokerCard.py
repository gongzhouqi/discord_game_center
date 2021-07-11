from typing import List

from core.util.recourse_util import GCRecourse


card_images = GCRecourse("card_image")


class Card:
    SPADE = 0
    HEART = 1
    CLUB = 2
    DIAMOND = 3
    NORMAL_COLORS = {SPADE, HEART, CLUB, DIAMOND}
    JOKER = 4

    ACE = 0
    KING = 1
    QUEEN = 2
    JACK = 3
    TEN = 4
    NINE = 5
    EIGHT = 6
    SEVEN = 7
    SIX = 8
    FIVE = 9
    FOUR = 10
    THREE = 11
    TWO = 12
    NORMAL_NUMBERS = {ACE, KING, QUEEN, JACK, TEN, NINE, EIGHT, SEVEN, SIX, FIVE, FOUR, THREE, TWO}
    NUMBER_CARDS = {TEN, NINE, EIGHT, SEVEN, SIX, FIVE, FOUR, THREE, TWO}
    FACE_CARDS = {KING, QUEEN, JACK}
    LARGE = 13
    SMALL = 14

    colors_short = ["S", "H", "C", "D", "J"]
    colors_full = ["Spade", "Heart", "Club", "Diamond", "JOKER"]
    colors_emoji = [":spades:", ":hearts:", ":clubs:", ":diamonds:", ":black_joker:"]
    numbers_short = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2", "R", "B"]
    numbers_full = ["Ace", "King", "Queen", "Jack", "10", "9", "8", "7", "6", "5", "4", "3", "2", "Red", "Black"]
    numbers_emoji = ["A", "K", "Q", "J",
                     ":keycap_ten:", ":nine:", ":eight:", ":seven:", ":six:", ":five:", ":four:", ":three:", ":two:",
                     ":red_square:", ":black_large_square:"]

    def __init__(self, color, number):
        assert (color in Card.NORMAL_COLORS and number in Card.NORMAL_NUMBERS) or\
               (color == Card.JOKER and (number == Card.SMALL or number == Card.LARGE))
        self.color = color
        self.number = number

    def get_image(self):
        return generate_cards_image([self])

    def is_red(self):
        return self.color == Card.HEART or self.color == Card.DIAMOND

    def is_black(self):
        return self.color == Card.SPADE or self.color == Card.CLUB

    def is_face(self):
        return self.number in Card.FACE_CARDS

    def is_number(self):
        return self.number in Card.NUMBER_CARDS

    def is_ACE(self):
        return self.number == Card.ACE

    def get_emoji(self):
        return Card.colors_emoji[self.color] + Card.numbers_emoji[self.number]

    def get_color_short(self):
        return Card.colors_short[self.color]

    def get_color_full(self):
        return Card.colors_full[self.color]

    def get_number_short(self):
        return Card.numbers_short[self.number]

    def get_number_full(self):
        return Card.numbers_full[self.number]

    def __hash__(self):
        return self.color * 53 + self.number

    def __eq__(self, other):
        if type(self) == type(other):
            return self.color == other.color and self.number == other.number
        return False

    def __str__(self):
        color = self.get_color_short()
        number = self.get_number_short()
        return color + number


def generate_cards_image(cards: List[Card]):
    # TODO: important
    if len(cards) == 1:
        c = cards[0]
        color = c.get_color_short()
        number = c.get_number_short()
        image_name = "{}{}.png".format(number, color)
        image_path = card_images.get_resource(image_name)
        return image_path
    pass
