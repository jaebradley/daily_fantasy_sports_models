from unittest import TestCase

from .models import Player, InvalidPlayerError, Position


class TestPlayer(TestCase):
    def test_invalid_player(self):
        with self.assertRaises(InvalidPlayerError):
            Player(
                "",
                "Jae",
                {Position.POINT_GUARD}
            )

        with self.assertRaises(InvalidPlayerError):
            Player(
                "1",
                "",
                {Position.POINT_GUARD}
            )

        with self.assertRaises(InvalidPlayerError):
            Player(
                "1",
                "Jae",
                {}
            )
