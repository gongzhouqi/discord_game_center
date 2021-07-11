from core.Exception import *
import core.Game
import core.Games.Library
import core.Room


class Hall:
    def __init__(self):
        self.channel_room_map = {}
        self.people_room_map = {}

    def create_room(self, user, channel, game_name):
        if game_name not in core.Games.Library.games:
            raise NoSuchGameException()
        if channel in self.channel_room_map:
            raise ChannelOccupiedException()
        if user in self.people_room_map:
            raise PlayerOccupiedException()
        game_id = core.Games.Library.games[game_name]
        game = core.Game.game_from_id(game_id)
        room = core.Room.Room(self, channel, user, game)
        self.channel_room_map[channel] = room
        self.people_room_map[user] = room

    def join_room(self, user, channel):
        if channel not in self.channel_room_map:
            raise NoSuchRoomException()
        if user in self.people_room_map:
            raise PlayerOccupiedException()
        room = self.channel_room_map[channel]
        try:
            room.join(user)
            self.people_room_map[user] = room
        except Exception as e:
            raise e

    def leave_room(self, user, channel):
        if channel not in self.channel_room_map:
            raise NoSuchRoomException()
        if user not in self.people_room_map:
            raise PlayerNotInRoomException()
        room = self.channel_room_map[channel]
        if self.people_room_map[user] != room:
            raise PlayerNotInRoomException()
        try:
            room.leave(user)
            self.people_room_map.pop(user)
        except Exception as e:
            raise e

    def close_room(self, user, channel):
        if channel not in self.channel_room_map:
            raise NoSuchRoomException()
        room = self.channel_room_map[channel]
        if user != room.owner:
            raise NotOwnerException(room.owner)
        try:
            people_in_room = room.close()
            self.channel_room_map.pop(channel)
            for person in people_in_room:
                self.people_room_map.pop(person)
        except Exception as e:
            raise e

    def start_room_game(self, user, channel):
        if channel not in self.channel_room_map:
            raise NoSuchRoomException()
        room = self.channel_room_map[channel]
        if user != room.owner:
            raise NotOwnerException(room.owner)
        try:
            room.start_game()
        except Exception as e:
            raise e

    def pass_instruction_to_game(self, user, channel, *args):
        if channel not in self.channel_room_map:
            raise NoSuchRoomException()
        room = self.channel_room_map[channel]
        try:
            room.instruction(user, args)
        except Exception as e:
            raise e
