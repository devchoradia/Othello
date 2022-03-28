from model.player import Player, AI_PLAYER, HUMAN_PLAYER
from model.game import Game
from model.ai.abstract_minimax_ai import AbstractMinimaxAI
import numpy as np

class MinimaxAI(AbstractMinimaxAI):
    def __init__(self,):
        super().__init__(6)

    def is_uncapturable(self, board, player, row, col, direction):
        '''
        Determines whether the location on the given board is uncapturable
        '''
        board_size = len(board)
        corner_tiles = [(0, 0), (0, board_size - 1), (board_size - 1, 0), (board_size - 1, board_size - 1)]
        border_indices = [board_size - 1, 0]
        if (row, col) in corner_tiles:
            return True
        elif col == board_size - 1 or col == 0:
            if direction == 0 or direction == -1:
                if board[row - 1, col] == int(player):
                    is_uncapturable = self.is_uncapturable(board, int(player), row - 1, col, -1)
                    if is_uncapturable == True:
                        return is_uncapturable
            if direction == 0 or direction == 1:
                if board[row + 1, col] == int(player):
                    return self.is_uncapturable(board, int(player), row + 1, col, 1)
        elif row == board_size - 1 or row == 0:
            if direction == 0 or direction == -1:
                if board[row, col - 1] == int(player):
                    is_uncapturable = self.is_uncapturable(board, int(player), row, col - 1, -1)
                    if is_uncapturable == True:
                        return is_uncapturable
            if direction == 0 or direction == 1:
                if board[row, col + 1] == int(player):
                    return self.is_uncapturable(board, int(player), row, col + 1, 0)
        return False

    def heuristic(self, state):
        '''
        Estimates the utility value of the state of the board
        '''
        computer_score = 0
        opponent_score = 0
        for row_idx, row in enumerate(state):
            for col_idx, tile in enumerate(row):
                if tile == int(AI_PLAYER): # Our tile
                    computer_score += 1
                    if self.is_uncapturable(state, AI_PLAYER, row_idx, col_idx, 0):
                        computer_score += 999
                elif tile == int(HUMAN_PLAYER): # Opponent tile
                    opponent_score += 1
                    if self.is_uncapturable(state, HUMAN_PLAYER, row_idx, col_idx, 0):
                        opponent_score += 999
        return computer_score, opponent_score

    def get_utility_value(self, state):
        '''
        Returns the utility value of the given state
        '''
        computer_score, opponent_score, = self.heuristic(state)
        return computer_score - opponent_score
    