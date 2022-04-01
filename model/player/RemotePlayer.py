from enum import IntEnum
from model.observer import Observable
from abc import abstractmethod
from model.player.player import Player, GamePlayer

'''
Stub class for RemotePlayer class (TODO)
'''
class RemotePlayer(GamePlayer):
    def __init__(self, player_color=Player.WHITE):
        super().__init__(player_color)

    def get_requested_move(self) -> (int, int):
        return (0, 0)
    
    def request_move(self):
        pass