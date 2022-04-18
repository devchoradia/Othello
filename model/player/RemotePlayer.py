from enum import IntEnum
from model.observer import Observable
from abc import abstractmethod
from client.client import Client
from model.player.player import Player, GamePlayer

'''
Stub class for RemotePlayer class (TODO)
'''
class RemotePlayer(GamePlayer):
    def __init__(self, player_color=Player.WHITE, game=None):
        super().__init__(player_color)
        self.game = game
        self.client = Client()
        self.client.set_observer(self)

    def get_requested_move(self) -> (int, int):
        return (0, 0)
    
    def request_move(self):
        pass

    def update(self):
        pass