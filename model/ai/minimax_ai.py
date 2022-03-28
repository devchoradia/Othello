from model.player import Player
from model.game import Game
import numpy as np

class MinimaxAI:
    def decision(self, state):
        '''
        Returns the best move (tuple) based on the minimax algorithm
        '''
        best_value, best_move = self.max_value(state, float('-inf'), float('inf'))
        return best_move

    def max_value(self, state, alpha, beta, depth=10):
        '''
        Returns the max utility value (and its corresponding move) possible from this state
        '''
        best_move = None
        board_size = len(state)
        model = Game(board_size=board_size, board=state.copy(), curr_player=Player.BLACK)
        if depth == 0:
            return self.get_utility_value(state), best_move
        best_value = float('-inf')
        moves = model.get_valid_moves(player=Player.WHITE)
        for move in moves:
            print(move, alpha, beta, best_value)
            model = Game(board_size=board_size, board=state.copy(), curr_player=Player.WHITE)
            row, col = move
            new_state = model.make_move(row, col)
            a = self.min_value(model.board, alpha, beta, depth=depth-1)
            if a == max(best_value, a):
                best_move = (row, col)
                print("set next best value", best_value)
            best_value = max(best_value, a)
            print("a", a)
            if best_value >= beta:
                return best_value, best_move
            alpha = max(alpha, best_value)
        print(best_move)
        if len(moves) == 0:
            return self.get_utility_value(state, Player.WHITE), best_move
        return best_value, best_move

    def min_value(self, state, alpha, beta, depth=10):
        '''
        Returns the min utility value possible from this state
        '''
        min_value = float('inf')
        board_size = len(state)
        min_move = None
        model = Game(board_size=board_size, board=state.copy(), curr_player=Player.BLACK)
        if depth == 0:
            return self.get_utility_value(state)
        moves = model.get_valid_moves(player=Player.BLACK)
        for move in moves:
            model = Game(board_size=board_size, board=state.copy(), curr_player=Player.BLACK)
            row, col = move
            new_state = model.make_move(row, col)
            max_value, max_move = self.max_value(model.board, alpha, beta)
            if max_value == min(min_value, max_value):
                min_move = (row, col)
            min_value = max(min_value, max_value)
            if min_value <= alpha:
                return min_value
            beta = min(beta, min_value)
        if len(moves) == 0:
            return self.get_utility_value(state, Player.BLACK)
        return min_value

    def is_uncapturable(self, board, player, row, col, direction):
        corner_tiles = [(0, 0), (len(board) - 1, len(board) - 1), (0, len(board) - 1), (len(board) - 1, 0)]
        border_indices = [len(board) - 1, 0]
        if (row, col) in corner_tiles:
            return True
        elif col == len(board) - 1 or col == 0:
            if direction == 0 or direction == -1:
                if board[row - 1, col] == int(player):
                    is_uncapturable = self.is_uncapturable(board, int(player), col, row - 1, -1)
                    if is_uncapturable == True:
                        return is_uncapturable
            if direction == 0 or direction == 1:
                if board[row + 1, col] == int(player):
                    return self.is_uncapturable(board, int(player), col, row + 1, 1)
        elif row == len(board) - 1 or row == 0:
            if direction == 0 or direction == -1:
                if board[row, col - 1] == int(player):
                    is_uncapturable = self.is_uncapturable(board, int(player), col - 1, row, -1)
                    if is_uncapturable == True:
                        return is_uncapturable
            if direction == 0 or direction == 1:
                if board[row, col + 1] == int(player):
                    return self.is_uncapturable(board, int(player), col + 1, row, 0)
        return False

    def heuristic(self, state):
        '''
        Estimates the utility value of the state of the board
        '''
        computer_score = 0
        opponent_score = 0
        for row_idx, row in enumerate(state):
            for col_idx, tile in enumerate(row):
                if tile == int(Player.WHITE): # Our tile
                    computer_score += 1
                    if self.is_uncapturable(state, Player.WHITE, row_idx, col_idx, 0):
                        computer_score += 999
                elif tile == int(Player.BLACK): # Opponent tile
                    opponent_score += 1
                    if self.is_uncapturable(state, Player.BLACK, row_idx, col_idx, 0):
                        opponent_score += 999
        return computer_score, opponent_score

    def get_utility_value(self, state, player):
        '''
        Returns the utility value of the given state
        '''
        computer_score, opponent_score, = self.heuristic(state)
        if int(player) == int(Player.BLACK):
            return opponent_score - computer_score
        return computer_score - opponent_score
    