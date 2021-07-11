from typing import List

import discord
from discord import TextChannel, Member

from core.Exception import InGamingException, NotInGamingException, GamePopulationException
import core.Game
import core.Hall


# Room status
WAITING = 0
GAMING = 1


class Room:
    def __init__(self, hall, channel, owner, game):
        self.hall: core.Hall.Hall = hall
        self.channel: TextChannel = channel
        self.owner: Member = owner
        self.people: List[Member] = [owner]
        self.players: List[int] = [0]
        self.total_players: int = 1
        self.curr_player_number: int = 1
        self.users_to_players = {owner: 0}
        self.players_to_users = {0: owner}
        self.game: core.Game.Game = game
        self.status: int = WAITING

    def start_game(self):
        if self.status == GAMING:
            raise InGamingException()
        if self.total_players < self.game.lower or self.total_players > self.game.higher:
            raise GamePopulationException(self.game.name, str(self.game.lower), str(self.game.higher))
        self.status = GAMING
        for player in self.players:
            self.game.join(player)
        self.game.start()

    def join(self, user):
        if self.status == GAMING:
            raise InGamingException()
        self.people.append(user)
        player_number = self.curr_player_number
        self.total_players += 1
        self.curr_player_number += 1
        self.users_to_players[user] = player_number
        self.players_to_users[player_number] = user
        self.players.append(player_number)

    def leave(self, user):
        if user == self.owner:
            self.close()
        else:
            self.people.remove(user)
            player_number = self.users_to_players.pop(user)
            self.players_to_users.pop(player_number)
            self.total_players -= 1
            self.players.remove(player_number)
            if self.status == GAMING:
                self.game.leave(player_number)

    def close(self):
        # TODO: Sort of important
        return self.people

    def instruction(self, user, *args):
        if self.status == WAITING:
            raise NotInGamingException()
        self.game.command(self.users_to_players[user], args)

    def game_ends(self):
        # TODO:
        self.status = WAITING

    async def broadcast(self, msg, file=None):
        await self.channel.send(msg, file=discord.File(file))

    async def send_to_player(self, player, msg, file=None):
        await self.players_to_users[player].send(msg, file=discord.File(file))

    def get_player_name(self, player):
        return self.players_to_users[player].name
