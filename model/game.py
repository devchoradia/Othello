import numpy as np

from model.observer import Observable
from model.player.player import Player


class Game(Observable):
    def __init__(self, board_size=8, board=None, curr_player=Player.BLACK):
        super().__init__()
        if board_size < 3:
            print("Invalid board size. Using default 8x8 board.")
            board_size = 8
        self.board_size = board_size
        self.curr_player = curr_player
        self.move_history = []
        if board is None:
            self.board = np.zeros((board_size, board_size), dtype=np.int)
            self.init_board()
        else:
            self.board = board

    # Places the initial four tiles
    def init_board(self):
        center = int(self.board_size / 2)
        self.board[center, center] = int(Player.WHITE)
        self.board[center, center - 1] = int(Player.BLACK)
        self.board[center - 1, center] = int(Player.BLACK)
        self.board[center - 1, center - 1] = int(Player.WHITE)

        # Performs the given move for the current player, and updates the resulting captured tiles

    def make_move(self, row, col):
        '''
        Once the board is updated, notify the observers
        '''
        self.move_history.append((self.curr_player, (row, col)))
        self.board[row, col] = int(self.curr_player)
        self.update_tiles(row, col)

    # Finds captured tiles based on the player's move and updates them
    def update_tiles(self, row, col):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                if col + dx < 0 or col + dx >= self.board_size or row + dy < 0 or row + dy >= self.board_size:
                    continue
                neighbor = self.board[row + dy, col + dx]
                if neighbor == 0 or neighbor == int(self.curr_player):
                    continue

                captured = [(row + dy, col + dx)]
                i = 2
                while i < self.board_size:
                    captured.append((row + i * dy, col + i * dx))
                    if col + i * dx < 0 or col + i * dx >= self.board_size or row + i * dy < 0 or row + i * dy >= self.board_size:
                        break
                    if self.board[row + i * dy, col + i * dx] == 0:
                        break
                    if self.board[row + i * dy, col + i * dx] == int(self.curr_player):
                        self.capture_tiles(captured)
                    i += 1
        return False

    # Takes a list of tile positions that are captured, and updates those tiles
    def capture_tiles(self, captured_positions):
        for row, col in captured_positions:
            self.board[row, col] = int(self.curr_player)

    # Switches the player turn
    def switch_player_turn(self):
        '''
        Once the current player is updated, notify the observers
        '''
        self.curr_player = Player(len(Player) + 1 - self.curr_player)
        self.notify_observers()

    # Determines whether the given move is legal/valid
    def is_legal_move(self, row, col, player=None):
        if player is None:
            player = self.curr_player
        if row < 0 or row >= self.board_size:
            return False
        if col < 0 or col >= self.board_size:
            return False
        if self.board[row, col] != 0:
            return False

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                isInvalidDirection = dx == 0 and dy == 0
                if isInvalidDirection or not self.is_capturable(row + dy, col + dx, player):
                    continue
                i = 2
                while i < self.board_size:
                    newCol = col + i * dx
                    newRow = row + i * dy
                    hasReachedEndOfBoard = newCol < 0 or newCol >= self.board_size or newRow < 0 or newRow >= self.board_size
                    if hasReachedEndOfBoard or self.board[newRow, newCol] == 0:
                        break
                    if self.board[newRow, newCol] == int(player):
                        return True;
                    i += 1
        return False

    # Determine whether the tile at the given location is the current player's opponent
    def is_capturable(self, row, col, player=None):
        if player is None:
            player = self.curr_player
        # If the location is out of bounds, it isnot capturable
        if col < 0 or col >= self.board_size or row < 0 or row >= self.board_size:
            return False
        # The tile is capturable iff it is an opponentplayer
        tile = self.board[row, col]
        return tile != 0 and tile != int(player)

    # Determines whether the current player can move
    def has_valid_move(self, player=None):
        if player is None:
            player = self.curr_player
        for row_idx, row in enumerate(self.board):
            for col_idx, tile in enumerate(row):
                if tile == 0 and self.is_legal_move(row_idx, col_idx, player):
                    return True
        return False

    # Get all valid moves for the given player
    def get_valid_moves(self, player=None):
        if player is None:
            player = self.curr_player
        valid_moves = []
        for row_idx, row in enumerate(self.board):
            for col_idx, tile in enumerate(row):
                if tile == 0 and self.is_legal_move(row_idx, col_idx, player):
                    valid_moves.append((row_idx, col_idx))
        return valid_moves

    # Returns whether the game is over as a result of the current player's move
    def is_game_terminated(self):
        has_valid_move = False
        for player in Player:
            if self.has_valid_move(player):
                has_valid_move = True
        return self.has_player_captured_all() or self.is_board_full() or not has_valid_move

    # Returns whether the current player has captured all of their opponents tiles
    def has_player_captured_all(self):
        for row in self.board:
            for tile in row:
                if tile != int(self.curr_player):
                    return False
        return True

    # Returns the winning player on the board
    def get_winner(self):
        if self.has_player_captured_all():
            return self.curr_player
        else:
            return self.get_player_with_max_tiles()

    # Returns the player with more tiles on the board, or 0 if it is a draw
    def get_player_with_max_tiles(self):
        max_tile_count = 0
        player_with_max_tile_count = 0
        for i in Player:
            count = (self.board == int(i)).sum()
            if count > max_tile_count:
                player_with_max_tile_count = i
                max_tile_count = count
            elif count == max_tile_count:
                player_with_max_tile_count = 0  # DRAW
        return player_with_max_tile_count

    # Determines whether the board is full
    def is_board_full(self):
        return not np.any(self.board == 0)
