from model.player.player import PLAYER_SYMBOL

class GameConsoleView:
    def __init__(self, board_console_view):
        self.board_console_view = board_console_view

    def display_board(self):
        self.board_console_view.display()

    def display_illegal_move(self, row, col):
        print("Illegal move: ", [row + 1, col + 1])

    def get_move(self):
        string_input = input('Input a move in the form [row, column]: ')
        try:
            input_coords = eval(string_input)
        except:
            print('Invalid input: ' + string_input)
            return self.get_move()
        if not isinstance(input_coords, list) or len(input_coords) != 2:
            print('Invalid input: ' + string_input)
            return self.get_move()
        else:
            row, col = tuple(input_coords)
            return row - 1, col - 1

    def display_curr_player(self, player):
        print("Current player: " + PLAYER_SYMBOL[player])

    def display_winner(self, player):
        print("Game over.")
        if player == 0:
            print("Draw.")
        else:
            print("Player " + PLAYER_SYMBOL[player] + " won.")