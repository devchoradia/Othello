from abc import ABC, abstractmethod

# Not implementing this yet
class GameView(ABC):
    def __init__(self, board_view):
        self.board_view = board_view

    def display_board(self):
        self.board_view.display()

    def display_illegal_move(self, row, col):
        print("Illegal move: ", row, col)

    def get_move(self):
        print("Please input a move in the form [row, column]: ")
        string_input = input('Enter your movement: ')
        try:
            input_coords = eval(string_input)
        except:
            return None
        if not isinstance(input_coords, list) or len(input_coords) != 2:
            print('Invalid input')
            return None
        else:
            row, col = input_coords
            return row + 1, col + 1



# abstract methods: $abstract_method
# get_move, #display_player, display_illegal_moves