from model.player.player import Player, AI_PLAYER, HUMAN_PLAYER
from model.game import Game
from model.ai.abstract_minimax_ai import AbstractMinimaxAI
import numpy as np

class MinimaxAI(AbstractMinimaxAI):
    def __init__(self,):
        super().__init__(4)

    def is_uncapturable(self, board, player, row, col, d):
        '''
        Determines whether the player's tile at the given location is uncapturable.
        A tile is "uncapturable" if it is either:
            - a corner tile
            - an edge tile where the remaining tiles along that edge, in at least one direction, are the same color.
        '''
        board_size = len(board)
        corner_tiles = [(0, 0), (0, board_size - 1), (board_size - 1, 0), (board_size - 1, board_size - 1)]
        border_indices = [board_size - 1, 0]
        if (row, col) in corner_tiles:
            return True
        elif col == board_size - 1 or col == 0:
            if d == 0 or d == -1:
                if board[row - 1, col] == int(player):
                    is_uncapturable = self.is_uncapturable(board, int(player), row - 1, col, -1)
                    if is_uncapturable:
                        return is_uncapturable
            if d == 0 or d == 1:
                if board[row + 1, col] == int(player):
                    return self.is_uncapturable(board, int(player), row + 1, col, 1)
        elif row == board_size - 1 or row == 0:
            if d == 0 or d == -1:
                if board[row, col - 1] == int(player):
                    is_uncapturable = self.is_uncapturable(board, int(player), row, col - 1, -1)
                    if is_uncapturable:
                        return is_uncapturable
            if d == 0 or d == 1:
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


class MinimaxAI2(AbstractMinimaxAI):
    def __init__(self,):
        super().__init__(4)
    
    def corner_closeness(self, board, player, row, col, d):
        '''
        Determines whether the player's tile at the given location is close to the corner squares.
        Squares adjacent to corners are a huge disadvantage as 
        it gives the opponent the opportunity to capture the corner. Therefore, we avoid capturing close corner squares.
        '''

        board_size = len(board)
        close_corner_tiles = [(0,1),(1,0),(1,1),(0, board_size - 2),(1, board_size - 2),(1, board_size - 1),
        (board_size - 2, 0),(board_size - 2, 1),(board_size - 1, 1), (board_size - 2, board_size - 2), 
        (board_size - 1, board_size - 2), (board_size - 2, board_size - 1)]
        if (row, col) in close_corner_tiles:
            return True


    def heuristic(self, state):
        '''
        Estimates the utility value of the state of the board for this AI level
        '''
        computer_score = 0
        opponent_score = 0
        for row_idx, row in enumerate(state):
            for col_idx, tile in enumerate(row):
                if tile == int(AI_PLAYER): # Our tile
                    computer_score += 1
                    if self.corner_closeness(state, AI_PLAYER, row_idx, col_idx, 0):
                        computer_score += 999
                elif tile == int(HUMAN_PLAYER): # Opponent tile
                    opponent_score += 1
                    if self.corner_closeness(state, HUMAN_PLAYER, row_idx, col_idx, 0):
                        opponent_score += 999
        return computer_score, opponent_score



    def get_utility_value(self, state):
        '''
        Returns the utility value of the given state
        '''
        computer_score, opponent_score, = self.heuristic(state)
        return computer_score - opponent_score
        
