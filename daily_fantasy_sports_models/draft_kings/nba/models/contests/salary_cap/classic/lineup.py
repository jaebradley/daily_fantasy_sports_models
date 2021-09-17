from dataclasses import dataclass

from daily_fantasy_sports_models.core.sets import is_disjoint
from daily_fantasy_sports_models.draft_kings.nba.models.contests.salary_cap.player_pool.player import Player \
    as PlayerPoolPlayer
from daily_fantasy_sports_models.draft_kings.nba.models.core.position import Position


class InvalidLineupError(ValueError):
    pass


class DuplicatePlayerError(InvalidLineupError):
    pass


# "Lineups...must include players from at least 2 different NBA games"
class MustIncludePlayersFromAtLeast2DifferentGames(InvalidLineupError):
    pass


# "a valid lineup must not exceed the salary cap of $50,000"
class MustNotExceedTheSalaryCap(InvalidLineupError):
    pass


class InvalidPlayerPosition(InvalidLineupError):
    pass


# https://www.draftkings.com/help/rules/4
# In salary cap contests, participants will create a lineup by selecting players listed in the Player Pool.
# Each player listed has an assigned salary and a valid lineup must not exceed the salary cap of $50,000.
# Lineups will consist of 8 players and must include players from at least 2 different NBA games.
@dataclass(init=True,
           repr=True,
           eq=True,
           order=False,
           unsafe_hash=False,
           frozen=True)
class Lineup:  # pylint: disable=too-many-instance-attributes

    POINT_GUARD_POSITIONS = frozenset({
        Position.POINT_GUARD
    })

    SHOOTING_GUARD_POSITIONS = frozenset({
        Position.SHOOTING_GUARD
    })

    SMALL_FORWARD_POSITIONS = frozenset({
        Position.SMALL_FORWARD
    })

    POWER_FORWARD_POSITIONS = frozenset({
        Position.POWER_FORWARD
    })

    CENTER_POSITIONS = frozenset({
        Position.CENTER
    })

    # G (PG,SG)
    GUARD_POSITIONS = POINT_GUARD_POSITIONS.union(SHOOTING_GUARD_POSITIONS)
    # F (SF, PF)
    FORWARD_POSITIONS = SMALL_FORWARD_POSITIONS.union(POWER_FORWARD_POSITIONS)
    # Util (PG,SG,SF,PF,C)
    UTILITY_POSITIONS = GUARD_POSITIONS.union(FORWARD_POSITIONS.union(CENTER_POSITIONS))

    point_guard: PlayerPoolPlayer
    shooting_guard: PlayerPoolPlayer
    small_forward: PlayerPoolPlayer
    power_forward: PlayerPoolPlayer
    center: PlayerPoolPlayer
    guard: PlayerPoolPlayer
    forward: PlayerPoolPlayer
    utility: PlayerPoolPlayer

    def __post_init__(self):
        lineup_players = [
            self.point_guard,
            self.shooting_guard,
            self.small_forward,
            self.power_forward,
            self.center,
            self.guard,
            self.forward,
            self.utility
        ]

        if 8 != len(set(
                map(
                    lambda contest_player: contest_player.player,
                    lineup_players
                )
        )):
            raise DuplicatePlayerError()

        if 2 > len(set(
                map(
                    lambda contest_player: contest_player.game_id,
                    lineup_players
                )
        )):
            raise MustIncludePlayersFromAtLeast2DifferentGames()

        if 50_000 < sum(
                map(
                    lambda contest_player: contest_player.salary,
                    lineup_players
                )
        ):
            raise MustNotExceedTheSalaryCap()

        for eligible_positions, player in {
            Lineup.POINT_GUARD_POSITIONS: self.point_guard,
            Lineup.SHOOTING_GUARD_POSITIONS: self.shooting_guard,
            Lineup.SMALL_FORWARD_POSITIONS: self.small_forward,
            Lineup.POWER_FORWARD_POSITIONS: self.power_forward,
            Lineup.CENTER_POSITIONS: self.center,
            Lineup.GUARD_POSITIONS: self.guard,
            Lineup.FORWARD_POSITIONS: self.forward,
            Lineup.UTILITY_POSITIONS: self.utility
        }.items():
            if is_disjoint(eligible_positions, player.positions):
                raise InvalidPlayerPosition()
