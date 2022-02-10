from abc import ABC, abstractmethod

class GameView(ABC):
    def __init__(self, board_view):
        self.board_view = board_view

    def display_board(self):
        self.board_view.display()

# abstract methods: $abstract_method
# get_move, #display_player, display_illegal_moves