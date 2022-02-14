from model.player import Player
import numpy as np

class Game:
    def __init__(self, board_size = 8):
        if board_size < 3:
            print("Invalid board size. Using default 8x8 board.")
            board_size = 8
        self.board_size = board_size
        self.curr_player = Player.BLACK
        self.board = np.zeros((board_size, board_size), dtype=np.int)
        self.init_board()

    def init_board(self):
        center = int(self.board_size / 2)
        self.board[center, center] = int(Player.WHITE)
        self.board[center, center - 1] = int(Player.BLACK)
        self.board[center - 1, center] = int(Player.BLACK)
        self.board[center - 1, center - 1] = int(Player.WHITE) 

    def make_move(self, row, col):
        self.board[row, col] = int(self.curr_player)
        self.update_tiles(row, col)

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
    
    def capture_tiles(self, captured_positions):
        for row, col in captured_positions:
            self.board[row, col] = int(self.curr_player)
    
    def switch_player_turn(self):
        self.curr_player = Player(len(Player) + 1 - self.curr_player)

    def is_legal_move(self, row, col):
        if row < 0 or row >= self.board_size:
            return False
        if col < 0 or col >= self.board_size:
            return False
        if self.board[row, col] != 0:
            return False
        
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                if col + dx < 0 or col + dx >= self.board_size or row + dy < 0 or row + dy >= self.board_size:
                    continue
                neighbor = self.board[row + dy, col + dx]
                if neighbor == 0 or neighbor == int(self.curr_player):
                    continue
                i = 2
                while i < self.board_size:
                    if col + i * dx < 0 or col + i * dx >= self.board_size or row + i * dy < 0 or row + i * dy >= self.board_size:
                        break
                    if self.board[row + i * dy, col + i * dx] == 0:
                        break
                    if self.board[row + i * dy, col + i * dx] == int(self.curr_player):
                        return True;            
                    i+=1
        return False

    def has_valid_move(self):
        for row_idx, row in enumerate(self.board):
            for col_idx, tile in enumerate(row):
                if tile == 0 and self.is_legal_move(row_idx, col_idx):
                    return True
        return False

    def is_game_terminated(self):
        return self.has_player_captured_all() or self.is_board_full()

    def has_player_captured_all(self):
        for row in self.board:
            for tile in row:
                if tile != 0 and tile != int(self.curr_player):
                    return False
        return True

    def get_winner(self):
        # TODO: check if this works
        if self.has_player_captured_all():
            return self.curr_player
        else:
            return self.get_player_with_max_tiles()

    def get_player_with_max_tiles(self):
        max_tile_count = 0
        player_with_max_tile_count = 0
        for i in range(len(Player)):
            count = (self.board == 3).sum()
            if count > max_tile_count:
                player_with_max_tile_count = i
            if count == max_tile_count:
                player_with_max_tile_count = 0 # DRAW
        return player_with_max_tile_count

    def is_board_full(self):
        return not np.any(self.board == 0)
        # for row in self.board:
        #     for tile in row:
        #         if tile != Player.NONE:
        #             return False
        # return true
    
    