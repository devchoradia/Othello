# test session
import unittest

from session import Session


class TestSession(unittest.TestCase):
    def setUp(self):
        self.session = Session()
        self.session.log_in("Jeff_5", 4)

    def test_is_logged_in_is_logged(self):
        self.assertTrue(self.session.is_logged_in())

    def test_is_logged_in_not_logged(self):
        self.session.log_out()
        self.assertFalse(self.session.is_logged_in())

    def test_get_username(self):
        self.assertEqual(self.session.get_username(), "Jeff_5")

    def test_ELORating(self):
        new_rating = self.session.get_ELORating() + 1
        self.session.update_ELORating(new_rating)
        self.assertEqual(self.session.get_ELORating(), 5)
