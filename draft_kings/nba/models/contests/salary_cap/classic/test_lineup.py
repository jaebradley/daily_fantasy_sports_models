from unittest import TestCase

from draft_kings.nba.models.contests.salary_cap.classic.lineup import Lineup, DuplicatePlayerError
from draft_kings.nba.models.contests.salary_cap.player_pool.player import Player as PlayerPoolPlayer
from draft_kings.nba.models.core.player import Player
from draft_kings.nba.models.core.position import Position


class TestLineup(TestCase):
    def test_non_unique_players_are_invalid(self):
        with self.assertRaises(DuplicatePlayerError):
            Lineup(
                point_guard=PlayerPoolPlayer(
                    player=Player(
                        id="1",
                        name="jae"
                    ),
                    positions={Position.POINT_GUARD},
                    game_id="foo",
                    salary=1
                ),
                shooting_guard=PlayerPoolPlayer(
                    player=Player(
                        id="1",
                        name="jae"
                    ),
                    positions={Position.SHOOTING_GUARD},
                    game_id="bar",
                    salary=2
                ),
                small_forward=PlayerPoolPlayer(
                    player=Player(
                        id="2",
                        name="badley"
                    ),
                    positions={Position.SMALL_FORWARD},
                    game_id="a",
                    salary=3
                ),
                power_forward=PlayerPoolPlayer(
                    player=Player(
                        id="3",
                        name="some power forward"
                    ),
                    positions={Position.POWER_FORWARD},
                    game_id="b",
                    salary=4
                ),
                center=PlayerPoolPlayer(
                    player=Player(
                        id="4",
                        name="some center"
                    ),
                    positions={Position.CENTER},
                    game_id="c",
                    salary=5
                ),
                guard=PlayerPoolPlayer(
                    player=Player(
                        id="5",
                        name="some guard"
                    ),
                    positions={Position.POINT_GUARD},
                    game_id="d",
                    salary=6
                ),
                forward=PlayerPoolPlayer(
                    player=Player(
                        id="5",
                        name="some forward"
                    ),
                    positions={Position.SMALL_FORWARD},
                    game_id="e",
                    salary=7
                ),
                utility=PlayerPoolPlayer(
                    player=Player(
                        id="6",
                        name="some utility player"
                    ),
                    positions={Position.CENTER},
                    game_id="f",
                    salary=8
                )
            )
