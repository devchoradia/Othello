from enum import IntEnum
from model.observer import Observable
from abc import abstractmethod
from view.game_view import GameView
from model.player.player import Player, GamePlayer

'''
Local player class.
The player uses the BoardView to retrieve a move
'''
class LocalPlayer(GamePlayer):
    def __init__(self, view: GameView, player_color=Player.BLACK):
        super().__init__(player_color)
        self.board_view = view.board_view
        self.player_color = player_color

    def get_requested_move(self) -> (int, int):
        row, col = self.board_view.get_requested_move()
        self.board_view.remove_move_handler()
        return (row, col)
    
    def request_move(self):
        self.board_view.set_move_handler(self.notify_observers)