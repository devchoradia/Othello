from model.player import Player
import numpy as np

class Game:
    def __init__(self, board_size):
        self.board_size = board_size
        self.curr_player = Player.X
        self.board = np.zeros((board_size, board_size), dtype=np.int)
        self.init_board()

    def init_board(self):
        center = int(self.board_size / 2)
        self.board[center, center] = int(Player.O)
        self.board[center, center - 1] = int(Player.X)
        self.board[center - 1, center] = int(Player.X)
        self.board[center - 1, center - 1] = int(Player.O) 

    def make_move(self, row, col):
        self.board[row, col] = int(self.curr_player)
    
    def switch_player_turn(self):
        self.curr_player = Player(len(Player) + 1 - self.curr_player)

    def is_legal_move(self, row, col):
        # TODO
        if row < 0 or row >= self.board_size:
            return False
        if col < 0 or col >= self.board_size:
            return False
        if self.board[row, col] != 0:
            return False
        return True

    def is_game_terminated(self):
        return self.has_player_won() or self.is_board_full()

    def has_player_won(self):
        # TODO
        return False

    def get_winner(self):
        if self.has_player_won():
            return self.curr_player
        else:
            return 0

    def is_board_full(self):
        return not np.any(self.board == 0)
        # for row in self.board:
        #     for tile in row:
        #         if tile != Player.NONE:
        #             return False
        # return true
    
    