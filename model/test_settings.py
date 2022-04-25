# test settings
import unittest
from client.client import Client
from model.game_mode import GameMode
from settings import Settings

class TestSettings(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()

    def test_get_board_size(self):
        self.assertEqual(self.settings.get_board_size(), 4)

    def test_get_board_color(self):
        self.assertEqual(self.settings.get_board_color(), "green")

    def test_get_game_mode(self):
        self.assertEqual(self.settings.get_board_color(), GameMode.LOCAL)


