from abc import abstractmethod
from enum import IntEnum

from model.observer import Observable


class Player(IntEnum):
    BLACK = 1
    WHITE = 2


PLAYER_SYMBOL = {
    Player.BLACK: 'X',
    Player.WHITE: 'O',
    0: ' '
}

PLAYER_COLOR = {
    Player.BLACK: 'black',
    Player.WHITE: 'white',
    0: 'green'
}

AI_PLAYER = Player.WHITE
HUMAN_PLAYER = Player.BLACK

'''
Abstract player class.
The player notifies the GameController when a move is made, and has a method to retrieve this last move requested.
'''


class GamePlayer(Observable):
    def __init__(self, player_color: Player):
        super().__init__()
        self.player_color = player_color

    @abstractmethod
    def get_requested_move(self) -> (int, int):
        pass

    @abstractmethod
    def request_move(self):
        pass
