from unittest import TestCase

from .player import Player, InvalidIdError, InvalidNameError


class TestPlayer(TestCase):
    def test_invalid_player(self):
        with self.assertRaises(InvalidIdError):
            Player(
                id="",
                name="Jae"
            )

        with self.assertRaises(InvalidNameError):
            Player(
                id="1",
                name=""
            )

    def test_valid_player(self):
        self.assertIsNotNone(
            Player(id="1", name="jae")
        )
