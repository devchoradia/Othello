from enum import IntEnum
from model.observer import Observable
from abc import abstractmethod
from model.player.player import Player, GamePlayer
from model.ai.abstract_minimax_ai import AbstractMinimaxAI
from view.game_view import GameView

'''
AI player class.
The player uses the minimax ai to retrieve a move
'''
class AIPlayer(GamePlayer):
    def __init__(self, ai: AbstractMinimaxAI, view: GameView, player_color=Player.WHITE):
        super().__init__(player_color)
        self.ai = ai
        self.board_view = view.board_view

    def get_requested_move(self) -> (int, int):
        return self.ai.decision(self.board_view.board)

    def request_move(self):
        self.board_view.root.after(1000, self.notify_observers)