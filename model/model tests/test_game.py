# test game.py

import unittest

import numpy as np

from model.game import Game
from model.player.player import Player


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_make_move(self):
        self.game.make_move(3, 2)
        self.assertEqual(self.game.board[3, 3], int(Player.BLACK))

    def test_switch_player_turn(self):
        previous_player = self.game.curr_player
        self.game.switch_player_turn()
        if previous_player == Player.BLACK:
            self.assertEqual(self.game.curr_player, Player.WHITE)
        else:
            self.assertEqual(self.game.curr_player, Player.BLACK)

    def test_is_legal_move_with_not_legal(self):
        self.assertFalse(self.game.is_legal_move(3, 3))

    def test_is_legal_move_with_legal(self):
        self.assertTrue(self.game.is_legal_move(3, 2))

    def test_is_capturable_with_capturable(self):
        # set board
        '''
                0   1   2   3   4   5   6   7
                   │   │   │   │   │   │   │   │0
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │1
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │2
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │ O │ X │   │   │   │3
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │ X │ O │   │   │   │4
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │5
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │6
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │7
                ───┼───┼───┼───┼───┼───┼───┼───┼
                '''
        self.assertTrue(self.game.is_capturable(4, 4))

    def test_is_capturable_not_capturable(self):
        '''
                0   1   2   3   4   5   6   7
                   │   │   │   │   │   │   │   │0
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │1
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │2
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │ O │ X │   │   │   │3
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │ X │ O │   │   │   │4
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │5
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │6
                ───┼───┼───┼───┼───┼───┼───┼───┼
                   │   │   │   │   │   │   │   │7
                ───┼───┼───┼───┼───┼───┼───┼───┼
                '''
        self.assertFalse(self.game.is_capturable(6, 6))

    def test_has_valid_moves_with_not_valid(self):
        self.game.board = np.full((8, 8), int(Player.BLACK))
        self.assertFalse(self.game.has_valid_move(Player.WHITE))

    def test_has_valid_moves_with_valid(self):
        self.assertTrue(self.game.has_valid_move(Player.BLACK))

    def test_get_valid_moves_BLACK(self):
        self.assertEqual(self.game.get_valid_moves(), [(2, 3), (3, 2), (4, 5), (5, 4)])

    def test_get_valid_moves_WHITE(self):
        self.game.switch_player_turn()
        self.assertEqual(self.game.get_valid_moves(), [(2, 4), (3, 5), (4, 2), (5, 3)])

    def test_is_game_terminated_not_over(self):
        self.assertFalse(self.game.is_game_terminated())

    def test_is_game_terminated_over(self):
        self.game.board = np.full((self.game.board_size, self.game.board_size), int(Player.BLACK))
        self.game.board[3, 3] = int(Player.WHITE)
        self.assertTrue(self.game.is_game_terminated())

    def test_has_player_captured_no_tiles_left(self):
        self.game.board = np.full((self.game.board_size, self.game.board_size), int(Player.BLACK))
        self.assertTrue(self.game.has_player_captured_all())

    def test_has_player_captured_full_with_different_players_tiles(self):
        self.game.board = np.full((self.game.board_size, self.game.board_size), int(Player.BLACK))
        self.game.board[3, 3] = int(Player.WHITE)
        self.assertFalse(self.game.has_player_captured_all())

    def test_has_player_captured_empty_tiles_left(self):
        self.assertFalse(self.game.has_player_captured_all())

    def test_get_winner(self):
        self.game.make_move(3, 2)
        self.assertEqual(self.game.get_winner(), Player.BLACK)

    def test_get_player_with_max_tiles_white(self):
        self.game.switch_player_turn()
        self.game.make_move(3, 2)
        self.assertEqual(self.game.get_player_with_max_tiles(), Player.WHITE)

    def test_get_player_with_max_tiles_black(self):
        self.game.make_move(4, 2)
        self.assertEqual(self.game.get_player_with_max_tiles(), Player.BLACK)

    def test_is_board_full_not_full(self):
        self.assertFalse(self.game.is_board_full())

    def test_is_board_full_is_full(self):
        self.game.board = np.full((8, 8), int(Player.BLACK))
        self.assertTrue(self.game.is_board_full())
