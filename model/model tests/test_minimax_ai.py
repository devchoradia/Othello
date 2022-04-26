# test minimax
import unittest
from model.ai.minimax_ai import MinimaxAI
from model.ai.minimax_ai import MinimaxAI2
from model.ai.minimax_ai import MinimaxAI3
from model.player.player import Player
from model.game import Game

class TestMinimax(unittest.TestCase):
    def setUp(self):
        self.minimax = MinimaxAI()
        self.minimax3 = MinimaxAI3()
        self.game = Game()

    def test_corner_closeness(self):

        self.assertTrue(self.minimax.corner_closeness(self.game.board, int(Player.WHITE), 0, 1, 0))

    def test_is_uncapturable(self):
            self.game.board[0, 0] = int(Player.WHITE)
            self.assertTrue(self.minimax.is_uncapturable(self.game.board, int(Player.WHITE), 0, 0, 0))

    def test_is_uncapturable_full_row(self):
        for spot in range(self.game.board_size):
            self.game.board[0, spot] = int(Player.WHITE)
        self.assertTrue(self.minimax.is_uncapturable(self.game.board, int(Player.WHITE), 0, 3, 0))

    def test_is_uncapturable_not(self):
        self.assertFalse(self.minimax.is_uncapturable(self.game.board, int(Player.WHITE), 4, 4, 0))

    def test_heuristic(self):
        self.game.make_move(3, 2)
        self.assertEqual(self.minimax.heuristic(self.game.board), (1, 4))

    def test_heuristic_with_uncapturables(self):
        self.game.make_move(3, 2)
        self.game.switch_player_turn()
        '''
                0   1   2   3   4   5   6   7
                 X │ X │ X │ X │ X │ X │ X │ X │0
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │ O │   │   │   │   │1
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │ O │   │   │   │   │2
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │ O │ X │   │   │   │3
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │ O │ O │ X │   │   │   │4
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │ X │   │   │   │5
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │6
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │7
                ───┼───┼───┼───┼───┼───┼───┼───┼
                '''
        self.game.make_move(2, 4)
        self.game.switch_player_turn()
        self.game.make_move(4, 5)
        self.game.switch_player_turn()
        self.game.make_move(3, 1)
        for spot in range(self.game.board_size):
            self.game.board[spot, 0] = int(Player.BLACK)
        self.assertEqual(self.minimax.heuristic(self.game.board), (5, 8003))

    def test_utility_score(self):
        self.game.make_move(3, 2)
        self.game.switch_player_turn()
        '''
                0   1   2   3   4   5   6   7
                   │   │   │   │   │   │   │   │0
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │ O │   │   │   │   │1
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │ O │   │   │   │   │2
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │ O │ X │   │   │   │3
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │ O │ O │ X │   │   │   │4
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │ X │   │   │   │5
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │6
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │7
                ───┼───┼───┼───┼───┼───┼───┼───┼
                '''
        self.game.make_move(2, 4)
        self.game.switch_player_turn()
        self.game.make_move(4, 5)
        self.game.switch_player_turn()
        self.game.make_move(3, 1)
        self.assertEqual(self.minimax.get_utility_value(self.game.board), 2)

    def test_utility_score_with_black_untouchables(self):
        self.game.make_move(3, 2)
        self.game.switch_player_turn()
        '''
                0   1   2   3   4   5   6   7
                 X │ X │ X │ X │ X │ X │ X │ X │0
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │ O │   │   │   │   │1
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │ O │   │   │   │   │2
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │ O │ X │   │   │   │3
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │ O │ O │ X │   │   │   │4
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │ X │   │   │   │5
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │6
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │7
                ───┼───┼───┼───┼───┼───┼───┼───┼
                '''
        self.game.make_move(2, 4)
        self.game.switch_player_turn()
        self.game.make_move(4, 5)
        self.game.switch_player_turn()
        self.game.make_move(3, 1)
        for spot in range(self.game.board_size):
            self.game.board[spot, 0] = int(Player.BLACK)
        self.assertEqual(self.minimax.get_utility_value(self.game.board), -7998)

    def test_utility_score_with_black_untouchables_minimaxAI3(self):
        self.game.make_move(3, 2)
        self.game.switch_player_turn()
        '''
                0   1   2   3   4   5   6   7
                 X │ X │ X │ X │ X │ X │ X │ X │0
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │ O │   │   │   │   │1
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │ O │   │   │   │   │2
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │ O │ X │   │   │   │3
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │ O │ O │ X │   │   │   │4
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │ X │   │   │   │5
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │6
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │7
                ───┼───┼───┼───┼───┼───┼───┼───┼
                '''
        self.game.make_move(2, 4)
        self.game.switch_player_turn()
        self.game.make_move(4, 5)
        self.game.switch_player_turn()
        self.game.make_move(3, 1)
        for spot in range(self.game.board_size):
            self.game.board[spot, 0] = int(Player.BLACK)
        self.assertEqual(self.minimax3.heuristic(self.game.board), (5, 8003))
