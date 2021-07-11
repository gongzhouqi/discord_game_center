from copy import deepcopy
from functools import cmp_to_key
from itertools import combinations
from typing import List

from core.Exception import UnexpectedErrorException
import core.Game
from core.Games.utils.PokerCard import Card, generate_cards_image
from core.Games.utils.PokerDeck import Deck


# User Instructions
U_CALL = "call"
U_RAISE = "raise"
U_FOLD = "fold"
U_ALL_IN = "all_in"
U_HELP = "help"

# Intermediate communication
M_SKIP = "m_skip"
M_DEALT_H = "m_dealt_h"
M_DEALT_T = "m_dealt_t"
M_END_CHARGE = "m_end_charge"

# Inner Instructions
I_BASE_CHARGE = "base_charge"
I_SKIP_CHARGE = "skip_charge"
I_CHARGE = "charge"
I_END_CHARGE = "end_charge"
I_DEAL_HANDS = "deal_hands"
I_DEAL_TABLE = "deal_table"
I_REPORT = "report"


class THFiveCards:
    ROYAL_FLUSH = 10
    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

    def __init__(self, cards):
        self.cards: List[Card] = cards
        self.reorder = None
        self.reordered = None
        self.straight = None
        self.flush = None
        self.four = None
        self.three = None
        self.pair1 = None
        self.pair2 = None
        self.score = -1

    def init(self):
        self.cards = sorted(self.cards, key=cmp_to_key(THFiveCards.compare_cards), reverse=True)
        self.init_straight()
        self.init_flush()
        self.init_four()
        self.init_three()
        self.init_pair1()
        self.init_pair2()
        self.init_score()

    @staticmethod
    def compare_cards(card1: Card, card2: Card):
        if card1.number < card2.number:
            return 1
        if card1.number > card2.number:
            return -1
        if card1.color < card2.color:
            return 1
        if card1.color > card2.color:
            return -1
        return 0

    def __eq__(self, other):
        if type(self) == type(other):
            for mc, oc in zip(self.cards, other.cards):
                if mc != oc:
                    return False
            return True
        return False

    def compare(self, other):
        if self.score > other.score:
            return 1
        if self.score < other.score:
            return -1
        for c1, c2 in zip(self.reordered, other.reordered):
            if c1.number < c2.number:
                return 1
            if c1.number > c2.number:
                return -1
        for c1, c2 in zip(self.reordered, other.reordered):
            if c1.color < c2.color:
                return 1
            if c1.color > c2.color:
                return -1
        return 0

    def init_straight(self):
        base_color = self.cards[0].color
        for cd in self.cards:
            if cd.color != base_color:
                self.straight = []
                return
        self.straight = [0, 1, 2, 3, 4]

    def init_flush(self):
        curr_number = self.cards[0].number
        for i in range(1, 5):
            cd = self.cards[i]
            if cd.number == curr_number+1:
                curr_number = cd.number
            else:
                self.flush = []
                return
        self.flush = [0, 1, 2, 3, 4]

    def init_four(self):
        mid_number = self.cards[1].number
        if self.cards[2].number == self.cards[3].number == mid_number:
            if self.cards[0] == mid_number:
                self.four = [0, 1, 2, 3]
            elif self.cards[4] == mid_number:
                self.four = [1, 2, 3, 4]
            else:
                self.four = []
        else:
            self.four = []

    def init_three(self):
        if self.has_four():
            self.three = []
        elif self.cards[0].number == self.cards[1].number == self.cards[2].number:
            self.three = [0, 1, 2]
        elif self.cards[1].number == self.cards[2].number == self.cards[3].number:
            self.three = [1, 2, 3]
        elif self.cards[2].number == self.cards[3].number == self.cards[4].number:
            self.three = [2, 3, 4]
        else:
            self.three = []

    def init_pair1(self):
        if self.has_four():
            self.pair1 = []
        elif self.has_three():
            if self.three == [0, 1, 2]:
                if self.cards[3].number == self.cards[4].number:
                    self.pair1 = [3, 4]
                else:
                    self.pair1 = []
            elif self.three == [2, 3, 4]:
                if self.cards[0].number == self.cards[1].number:
                    self.pair1 = [0, 1]
                else:
                    self.pair1 = []
            else:
                self.pair1 = []
        elif self.cards[0].number == self.cards[1].number:
            self.pair1 = [0, 1]
        elif self.cards[1].number == self.cards[2].number:
            self.pair1 = [1, 2]
        elif self.cards[2].number == self.cards[3].number:
            self.pair1 = [2, 3]
        elif self.cards[3].number == self.cards[4].number:
            self.pair1 = [3, 4]
        else:
            self.pair1 = []

    def init_pair2(self):
        if self.has_pair1():
            if self.has_three():
                self.pair2 = []
            elif self.pair1[1] == 1:
                if self.cards[2].number == self.cards[3].number:
                    self.pair2 = [2, 3]
                elif self.cards[3].number == self.cards[4].number:
                    self.pair2 = [3, 4]
                else:
                    self.pair2 = []
            elif self.pair1[1] == 2:
                if self.cards[3].number == self.cards[4].number:
                    self.pair2 = [3, 4]
                else:
                    self.pair2 = []
            else:
                self.pair2 = []
        else:
            self.pair2 = []

    def has_straight(self):
        return len(self.straight) != 0

    def has_flush(self):
        return len(self.flush) != 0

    def has_four(self):
        return len(self.four) != 0

    def has_three(self):
        return len(self.three) != 0

    def has_pair1(self):
        return len(self.pair1) != 0

    def has_pair2(self):
        return len(self.pair2) != 0

    def init_score(self):
        if self.has_straight() and self.has_flush():
            if self.cards[0].number == Card.ACE:
                self.score = THFiveCards.ROYAL_FLUSH
            else:
                self.score = THFiveCards.STRAIGHT_FLUSH
        elif self.has_four():
            self.score = THFiveCards.FOUR_OF_A_KIND
            if self.four == [1, 2, 3, 4]:
                self.reorder = [1, 2, 3, 4, 0]
        elif self.has_three() and self.has_pair1():
            self.score = THFiveCards.FULL_HOUSE
            if self.three == [2, 3, 4]:
                self.reorder = [2, 3, 4, 0, 1]
        elif self.has_flush():
            self.score = THFiveCards.FLUSH
        elif self.has_straight():
            self.score = THFiveCards.STRAIGHT
        elif self.has_three():
            self.score = THFiveCards.THREE_OF_A_KIND
            if self.three == [1, 2, 3]:
                self.reorder = [1, 2, 3, 0, 4]
            elif self.three == [2, 3, 4]:
                self.reorder = [2, 3, 4, 0, 1]
        elif self.has_pair1() and self.has_pair2():
            self.score = THFiveCards.TWO_PAIR
            if self.pair2 == [3, 4]:
                if self.pair1 == [0, 1]:
                    self.reorder = [0, 1, 3, 4, 2]
                elif self.pair1 == [1, 2]:
                    self.reorder = [1, 2, 3, 4, 0]
        elif self.has_pair1():
            self.score = THFiveCards.ONE_PAIR
            if self.pair1 == [1, 2]:
                self.reorder = [1, 2, 0, 3, 4]
            elif self.pair1 == [2, 3]:
                self.reorder = [2, 3, 0, 1, 4]
            elif self.pair1 == [3, 4]:
                self.reorder = [3, 4, 0, 1, 2]
        else:
            self.score = THFiveCards.HIGH_CARD
        if self.reorder is None:
            self.reorder = [0, 1, 2, 3, 4]
        self.reordered = []
        for order in self.reorder:
            self.reordered.append(self.cards[order])


def compare_two(cards1: THFiveCards, cards2: THFiveCards):
    return cards1.compare(cards2)


class SingleTH:
    # Status
    INITIALIZING = -1
    BASE_CHARGING = 0
    AFTER_BASE_CHARGING = 1
    DEALING_HANDS = 2
    AFTER_DEALING_HANDS = 3
    CHARGING = 4
    AFTER_CHARGING = 5
    END_CHARGING = 6
    DEALING_TABLE = 7
    AFTER_DEALING_TABLE = 8
    TERMINATING = 9

    # Rounds
    ROUND_1 = 1
    ROUND_2 = 2
    ROUND_3 = 3
    ROUND_4 = 4

    def _inform(self, target, instruction, *args):
        self.outer.call(target, instruction, args)
        return False

    def __init__(self, outer, players, owner, base=1, decks=2):
        assert owner == players[0]
        self.outer = outer
        self.players = players
        self.owner = owner
        self.base = base
        self.status = SingleTH.INITIALIZING
        self.status_info = []
        self.hands = {}
        self.bets = {}
        self.quited = {}
        self.remaining = -1
        self.all_in_ed = {}
        self.decks = decks
        self.deck = None
        self.first = None
        self.second = None
        self.third = None
        self.fourth = None
        self.fifth = None
        self.table = [None, None, None, None, None]
        self.highest_cards = {}
        self.init()

    def init(self):
        for player in self.players:
            self.hands[player] = []
            self.bets[player] = 0
            self.quited[player] = False
            self.all_in_ed[player] = False
        deck_content = [Deck.STANDARD_52 for _ in range(self.decks)]
        self.deck = Deck.generate_deck(deck_content)
        self.deck.shuffle()
        self.remaining = len(self.players)

    def start(self):
        self.process_game()

    def process_game(self):
        if self.status == SingleTH.INITIALIZING:
            self.status = SingleTH.BASE_CHARGING
            self.status_info = [0]
            self.process_game()
        elif self.status == SingleTH.BASE_CHARGING:
            self.base_charge()
        elif self.status == SingleTH.AFTER_BASE_CHARGING:
            if self.status_info[0]+1 == len(self.players):
                self.status = SingleTH.DEALING_HANDS
                self.status_info = [0]
            else:
                self.status = SingleTH.BASE_CHARGING
                self.status_info[0] += 1
            self.process_game()
        elif self.status == SingleTH.DEALING_HANDS:
            self.deal_hands()
        elif self.status == SingleTH.AFTER_DEALING_HANDS:
            if self.status_info[0]+1 == len(self.players):
                self.status = SingleTH.CHARGING
                self.status_info = [0, SingleTH.ROUND_1, [-1 for _ in self.players]]
            else:
                self.status = SingleTH.DEALING_HANDS
                self.status_info[0] += 1
            self.process_game()
        elif self.status == SingleTH.CHARGING:
            self.charge()
        elif self.status == SingleTH.AFTER_CHARGING:
            self.status = SingleTH.CHARGING
            self.status_info[0] += 1
            self.status_info[0] %= len(self.players)
            self.process_game()
        elif self.status == SingleTH.END_CHARGING:
            curr_round = self.status_info[1]
            if curr_round == SingleTH.ROUND_4:
                self.status = SingleTH.TERMINATING
            else:
                self.status = SingleTH.DEALING_TABLE
                self.status_info = [curr_round]
            self.process_game()
        elif self.status == SingleTH.DEALING_TABLE:
            self.deal_table()
        elif self.status == SingleTH.AFTER_DEALING_TABLE:
            self.status = SingleTH.CHARGING
            curr_round = self.status_info[0]
            self.status_info = [0, curr_round+1, [-1 for _ in self.players]]
            self.process_game()
        elif self.status == SingleTH.TERMINATING:
            self.get_highest_cards()
        else:
            raise UnexpectedErrorException()

    def base_charge(self):
        assert self.status == SingleTH.BASE_CHARGING
        to_charge = self.players[self.status_info[0]]
        self._inform(to_charge, "base_charge", self.base)

    def charge(self):
        assert self.status == SingleTH.CHARGING
        order = self.status_info[0]
        to_charge = self.players[order]
        if self.quited[to_charge]:
            self._inform(to_charge, "skip_charge")
        else:
            bets = self.status_info[2]
            prev_other_bet = max(bets)
            if prev_other_bet == -1:
                prev_other_bet = 0
            curr_bet = bets[order]
            if curr_bet == -1:
                self._inform(to_charge, "charge", prev_other_bet, True)
            else:
                if prev_other_bet == curr_bet:
                    self._inform(None, "end_charge")
                else:
                    self._inform(to_charge, "charge", prev_other_bet-curr_bet, False)

    def on_charged(self, player, action, info, all_in):
        assert self.status == SingleTH.CHARGING or self.status == SingleTH.BASE_CHARGING
        order = self.status_info[0]
        assert self.players[order] == player
        if self.status == SingleTH.BASE_CHARGING:
            if action == "fold":
                self.quit(player)
            else:
                self.bets[player] += info
                if all_in:
                    self.all_in_ed[player] = True
            self.status = SingleTH.AFTER_BASE_CHARGING
            self.process_game()
        else:
            if action == "fold":
                self.quit(player)
            else:
                bets = self.status_info[2]
                if bets[order] == -1:
                    bets[order] = info
                else:
                    bets[order] += info
                self.bets[player] += info
                if all_in:
                    self.all_in_ed[player] = True
            self.status = SingleTH.AFTER_CHARGING
            self.process_game()

    def on_end_charging(self):
        assert self.status == SingleTH.CHARGING
        self.status = SingleTH.END_CHARGING
        self.process_game()

    def on_skipped_charging(self):
        assert self.status == SingleTH.CHARGING
        self.status = SingleTH.AFTER_CHARGING
        self.process_game()

    def deal_hands(self):
        assert self.status == SingleTH.DEALING_HANDS
        to_deal = self.players[self.status_info[0]]
        c1 = self.deck.touch()
        c2 = self.deck.touch()
        self.hands[to_deal] = [c1, c2]
        self._inform(to_deal, "deal_hands", c1, c2)

    def on_dealt_hands(self):
        assert self.status == SingleTH.DEALING_HANDS
        self.status = SingleTH.AFTER_DEALING_HANDS
        self.process_game()

    def deal_table(self):
        assert self.status == SingleTH.DEALING_TABLE
        assert self.status_info[0] == SingleTH.ROUND_1 or\
               self.status_info[0] == SingleTH.ROUND_2 or\
               self.status_info[0] == SingleTH.ROUND_3

        if self.status_info[0] == SingleTH.ROUND_1:
            c1 = self.deck.touch()
            c2 = self.deck.touch()
            c3 = self.deck.touch()
            self.first = c1
            self.second = c2
            self.third = c3
            self.table[0] = c1
            self.table[1] = c2
            self.table[2] = c3
        elif self.status_info[0] == SingleTH.ROUND_2:
            c4 = self.deck.touch()
            self.fourth = c4
            self.table[3] = c4
        else:
            c5 = self.deck.touch()
            self.fourth = c5
            self.table[4] = c5
        self._inform(None, "deal_table", self.table)

    def on_dealt_table(self):
        assert self.status == SingleTH.DEALING_TABLE
        self.status = SingleTH.AFTER_DEALING_TABLE
        self.process_game()

    def quit(self, player):
        self.quited[player] = True
        self.remaining -= 1
        if self.remaining == 1:
            self.report_winning(None)

    def get_highest_cards(self):
        for player in self.players:
            if not self.quit(player):
                possibilities = []
                three_cards = combinations(self.table, 3)
                four_cards = combinations(self.table, 4)
                five_cards = combinations(self.table, 5)
                for cd3 in three_cards:
                    tmp = deepcopy(list(cd3))
                    tmp.append(self.hands[player][0])
                    tmp.append(self.hands[player][1])
                    possibilities.append(THFiveCards(tmp))
                for cd4 in four_cards:
                    tmp1 = deepcopy(list(cd4))
                    tmp2 = deepcopy(list(cd4))
                    tmp1.append(self.hands[player][0])
                    tmp2.append(self.hands[player][1])
                    possibilities.append(THFiveCards(tmp1))
                    possibilities.append(THFiveCards(tmp2))
                for cd5 in five_cards:
                    tmp = deepcopy(list(cd5))
                    possibilities.append(THFiveCards(tmp))
                sorted_possibilities = sorted(possibilities, key=cmp_to_key(compare_two), reverse=True)
                highest = sorted_possibilities[0]
                self.highest_cards[player] = highest
        winner_cards = sorted(list(self.highest_cards.values()), key=cmp_to_key(compare_two), reverse=True)[0]
        winners = []
        for player, cards in self.highest_cards:
            if cards == winner_cards:
                winners.append(player)
        self.report_winning(winners)

    def report_winning(self, winner):
        if winner is None:
            winner = []
            for player in self.players:
                if not self.quited[player]:
                    winner.append(player)
            assert len(winner) == 1
        self._inform(None, "report", winner)


class TexasHoldEm(core.Game.Game):
    def __init__(self):
        super().__init__("德州扑克", 2, 8)
        self.inner_single_game = None
        self.expecting_player = -1
        self.expecting_command = []
        self.tmp_info = None

    def on_leave(self, player):
        self.inner_single_game.quit(player)

    def on_start(self):
        self.inner_single_game = SingleTH(self, deepcopy(self.players), self.players[0])
        self.inner_single_game.start()

    def on_command(self, player, *args):
        command = args[0]
        is_valid = self.check_expectation(command, player, args)
        self.clear_expectation()
        if not is_valid:
            # TODO: Maybe do something?
            return
        if command == U_HELP:
            # TODO: give help
            pass
        elif command == U_CALL:
            self.inner_single_game.on_charged(player, "bet", self.tmp_info, False)
        elif command == U_RAISE:
            self.inner_single_game.on_charged(player, "bet", self.tmp_info+args[1], False)
        elif command == U_ALL_IN:
            # TODO: multi-game feature
            self.inner_single_game.on_charged(player, "bet", 999, True)
        elif command == U_FOLD:
            self.inner_single_game.on_charged(player, "fold", None, False)
        elif command == M_SKIP:
            self.inner_single_game.on_skipped_charging()
        elif command == M_DEALT_H:
            self.inner_single_game.on_dealt_hands()
        elif command == M_DEALT_T:
            self.inner_single_game.on_dealt_table()
        elif command == M_END_CHARGE:
            self.inner_single_game.on_end_charging()
        else:
            # TODO: Maybe do something?
            pass

    def call(self, target, instruction, *args):
        if instruction == I_BASE_CHARGE:
            self.set_expectation([U_CALL], target, info=args[0])
            self.send_to_room("请{}支付盲注{}枚。".format(self.get_name_of(target), str(args[0])))
        elif instruction == I_SKIP_CHARGE:
            self.set_expectation([M_SKIP], target)
            self.on_command(target, M_SKIP)
        elif instruction == I_CHARGE:
            if args[1]:
                self.set_expectation([U_CALL, U_FOLD, U_RAISE], target, info=args[0])
                self.send_to_room("请{}下注，至少{}枚，可以加注。".format(self.get_name_of(target), str(args[0])))
            else:
                self.set_expectation([U_CALL, U_FOLD], target, info=args[0])
                self.send_to_room("请{}再跟注{}枚。".format(self.get_name_of(target), str(args[0])))
        elif instruction == I_END_CHARGE:
            self.send_to_room("全部下注完毕！")
            self.set_expectation([M_END_CHARGE], None)
            self.on_command(None, M_END_CHARGE)
        elif instruction == I_DEAL_HANDS:
            # TODO: fix this
            self.send_to_player(target, None, generate_cards_image([args[0]]))
            self.send_to_player(target, None, generate_cards_image([args[1]]))
            self.set_expectation([M_DEALT_H], target)
            self.on_command(target, M_DEALT_H)
        elif instruction == I_DEAL_TABLE:
            # TODO: fix this
            for c in args[0]:
                if c is not None:
                    self.send_to_room(None, generate_cards_image([c]))
            self.set_expectation([M_DEALT_T], None)
            self.on_command(None, M_DEALT_T)
        elif instruction == I_REPORT:
            for win in args[0]:
                self.send_to_room("{} 获胜！".format(self.get_name_of(win)))
            self.end()
        else:
            # TODO: Maybe do something?
            pass

    def set_expectation(self, command, command_from, info=None):
        self.expecting_command = command
        self.expecting_player = command_from
        self.tmp_info = info

    def check_expectation(self, command, command_from, *args):
        if command == U_HELP:
            return True
        if command not in self.expecting_command:
            return False
        if self.expecting_player != command_from:
            return False
        if command == U_RAISE:
            return len(args) == 2
        else:
            return len(args) == 1

    def clear_expectation(self):
        self.expecting_player = -1
        self.tmp_info = None
        self.expecting_command = []
