# test minimax abstract class
import unittest
from model.ai.minimax_ai import MinimaxAI
from model.ai.minimax_ai import MinimaxAI2
from model.ai.minimax_ai import MinimaxAI3
from model.player.player import Player
from model.game import Game


class TestAbstractMinimax(unittest.TestCase):
    def setup(self):
        self.minimax = MinimaxAI()
        self.minimax2 = MinimaxAI2()
        self.minimax3 = MinimaxAI3()
        self.game = Game()

    def test_decision(self):
        self.game.decision(1)
        x = self.game.decision()
        self.assertTrue(x, 1)

    def test_max_value(self):
        self.game.depth[0] = self.get_utility_value(state)
        self.assertEqual(self.get_utility_value(state), self.get_utility_value(state))

    def test_min_value(self):
        self.assertEqual(self.min_value, (min(self.maxvalue, self.min_value)))
