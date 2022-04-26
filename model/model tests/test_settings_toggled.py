# toggled test settings
import unittest

from model.game_mode import GameMode
from settings import Settings


class TestSettingsChanged(unittest.TestCase):
    def setup2(self):
        self.settings_changed = Settings()

    def test_update_setting(self):
        self.assertEqual(self.settings_changed.state(), value)

    def test_get_setting_label(self):
        self.assertEqual(self.settings_changed.SETTING_LABELS, "Settings")

    def test_get_setting_options(self):
        self.assertEqual(self.settings_changed.game_mode, self.options[Setting.GAME_MODE].remove(GameMode.REMOTE))

    def test_set_default_settings(self):
        self.assertEqual(self.settings_changed.state, copy.deepcopy(DEFAULT_SETTINGS))
        self.assertEqual(self.settings_changed.options, copy.deepcopy(DEFAULT_SETTINGS))

    def test_get_setting(self):
        self.assertEqual(self.settings_changed.state, [setting])

    def test_save_settings(self, settings):
        self.assertEqual(self.settings_changed.get_board_color(), settings[Setting.BOARD_COLOR])
        self.assertEqual(self.settings_changed.get_board_size(), settings[Setting.BOARD_SIZE])
        self.assertEqual(self.settings_changed.game_mode(), GameMode.LOCAL)

