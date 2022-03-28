from model.player import Player, AI_PLAYER, HUMAN_PLAYER
from abc import ABC, abstractmethod
from model.game import Game
import numpy as np

'''
Template method
AbstractMinimaxAI defines the skeleton of the minimax algorithm, but leaves the implementation of specific steps 
(e.g. the heuristic function, max depth, etc.) to the subclasses.

Different levels of the AI might implement different heuristics and calculate different depths of gameplay.
'''

class AbstractMinimaxAI(ABC):
    '''
    Abstract class a minimax ai player
    '''
    def __init__(self, max_depth):
        self.max_depth = max_depth

    def decision(self, state):
        '''
        Returns the best move (tuple) based on the minimax algorithm
        '''
        best_value, best_move = self.max_value(state, float('-inf'), float('inf'), self.max_depth)
        return best_move

    def max_value(self, state, alpha, beta, depth):
        '''
        Returns the max utility value (and its corresponding move) possible from this state
        '''
        best_move = None
        board_size = len(state)
        model = Game(board_size=board_size, board=state.copy(), curr_player=AI_PLAYER)
        if depth == 0:
            return self.get_utility_value(state), best_move
        best_value = float('-inf')
        moves = model.get_valid_moves(player=AI_PLAYER)
        for move in moves:
            model = Game(board_size=board_size, board=state.copy(), curr_player=AI_PLAYER)
            row, col = move
            new_state = model.make_move(row, col)
            a = self.min_value(model.board, alpha, beta, depth=depth-1)
            if a == max(best_value, a):
                best_move = (row, col)
            best_value = max(best_value, a)
            if best_value >= beta:
                return best_value, best_move
            alpha = max(alpha, best_value)
        if len(moves) == 0:
            return self.get_utility_value(state), best_move
        return best_value, best_move

    def min_value(self, state, alpha, beta, depth):
        '''
        Returns the min utility value possible from this state
        '''
        min_value = float('inf')
        board_size = len(state)
        min_move = None
        model = Game(board_size=board_size, board=state.copy(), curr_player=HUMAN_PLAYER)
        if depth == 0:
            return self.get_utility_value(state)
        moves = model.get_valid_moves(player=HUMAN_PLAYER)
        for move in moves:
            model = Game(board_size=board_size, board=state.copy(), curr_player=HUMAN_PLAYER)
            row, col = move
            new_state = model.make_move(row, col)
            max_value, max_move = self.max_value(model.board, alpha, beta, depth-1)
            if max_value == min(min_value, max_value):
                min_move = (row, col)
            min_value = max(min_value, max_value)
            if min_value <= alpha:
                return min_value
            beta = min(beta, min_value)
        if len(moves) == 0:
            return self.get_utility_value(state)
        return min_value

    @abstractmethod
    def get_utility_value(self, state):
        '''
        Returns the utility value of the given state
        '''
        pass
    