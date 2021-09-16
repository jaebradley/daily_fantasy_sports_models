from unittest import TestCase

from draft_kings.nba.models.contests.salary_cap.player_pool.player import Player as ContestPlayer, \
    InvalidGameIdError, PositionsCannotBeEmptyError
from draft_kings.nba.models.core.player import Player
from draft_kings.nba.models.core.position import Position


class TestPlayer(TestCase):
    def test_invalid_player(self):
        with self.assertRaises(InvalidGameIdError):
            ContestPlayer(
                player=Player(
                    id="1",
                    name="jae"
                ),
                positions={Position.POINT_GUARD},
                game_id="",
                salary=0
            )

        with self.assertRaises(PositionsCannotBeEmptyError):
            ContestPlayer(
                player=Player(
                    id="1",
                    name="jae"
                ),
                positions=set(),
                game_id="1",
                salary=0
            )

    def test_valid_player(self):
        self.assertIsNotNone(
            ContestPlayer(
                player=Player(
                    id="1",
                    name="jae"
                ),
                positions={Position.POINT_GUARD},
                game_id="foo",
                salary=0
            )
        )
