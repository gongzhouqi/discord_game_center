from abc import ABC, abstractmethod

import core.Room
import core.Games.Library


class Game(ABC):
    def __init__(self, name, lower, higher):
        self.room: core.Room.Room or None = None
        self.name: str = name
        self.lower: int = lower
        self.higher: int = higher
        self.total_players: int = 0
        self.historical_players = []
        self.players = []
        self.command_senders = []
        self.commands = []

    def start(self):
        self.on_start()

    def join(self, player):
        self.historical_players.append(player)
        self.players.append(player)

    def leave(self, player):
        self.players.remove(player)
        self.on_leave(player)

    def end(self):
        self.room.game_ends()

    def command(self, player, *args):
        self.command_senders.append(player)
        self.commands.append(args)
        self.on_command(player, args)

    def get_name_of(self, player):
        return self.room.get_player_name(player)

    def send_to_room(self, msg, file=None):
        self.room.broadcast(msg, file)

    def send_to_player(self, player, msg, file=None):
        self.room.send_to_player(player, msg, file)

    @abstractmethod
    def on_leave(self, player):
        pass

    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_command(self, player, *args):
        pass


def game_from_id(game_id):
    return core.Games.Library.game_classes[game_id]()
