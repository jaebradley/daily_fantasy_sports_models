from dataclasses import dataclass
from typing import Optional

from core.sets import is_disjoint
from draft_kings.nba.models.contests.salary_cap.player_pool.player import Player as PlayerPoolPlayer
from draft_kings.nba.models.core.position import Position


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


class InvalidPointGuardPosition(InvalidLineupError):
    pass


class InvalidShootingGuardPosition(InvalidLineupError):
    pass


class InvalidSmallForwardPosition(InvalidLineupError):
    pass


class InvalidPowerForwardPosition(InvalidLineupError):
    pass


class InvalidCenterPosition(InvalidLineupError):
    pass


class InvalidGuardPosition(InvalidLineupError):
    pass


class InvalidForwardPosition(InvalidLineupError):
    pass


class InvalidUtilityPosition(InvalidLineupError):
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

    dataclass(init=True,
              repr=True,
              eq=True,
              order=False,
              unsafe_hash=False,
              frozen=True)

    class Builder:
        point_guard: Optional[PlayerPoolPlayer]
        shooting_guard: Optional[PlayerPoolPlayer]
        small_forward: Optional[PlayerPoolPlayer]
        power_forward: Optional[PlayerPoolPlayer]
        center: Optional[PlayerPoolPlayer]
        guard: Optional[PlayerPoolPlayer]
        forward: Optional[PlayerPoolPlayer]
        utility: Optional[PlayerPoolPlayer]
        salary: float

        def set_point_guard(self, point_guard: PlayerPoolPlayer) -> None:
            if self.point_guard is None:
                raise ValueError()

            if Position.POINT_GUARD not in point_guard.positions:
                raise InvalidPointGuardPosition()

            if 50_000 < (point_guard.salary + self.salary):
                raise MustNotExceedTheSalaryCap()

            self.point_guard = point_guard
            self.salary += point_guard.salary

        def build(self) -> Lineup:
            return Lineup(
                point_guard=self.point_guard,
                shooting_guard=self.shooting_guard,
                small_forward=self.small_forward,
                power_forward=self.power_forward,
                center=self.center,
                guard=self.guard,
                forward=self.forward,
                utility=self.utility
            )

    # G (PG,SG)
    GUARD_POSITIONS = {
        Position.POINT_GUARD,
        Position.SHOOTING_GUARD
    }
    # F (SF, PF)
    FORWARD_POSITIONS = {
        Position.SMALL_FORWARD,
        Position.SMALL_FORWARD
    }
    # Util (PG,SG,SF,PF,C)
    UTILITY_POSITIONS = {
        Position.POINT_GUARD,
        Position.SHOOTING_GUARD,
        Position.SMALL_FORWARD,
        Position.POWER_FORWARD,
        Position.CENTER
    }

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

        if Position.POINT_GUARD not in self.point_guard.positions:
            raise InvalidPointGuardPosition()

        if Position.SHOOTING_GUARD not in self.shooting_guard.positions:
            raise InvalidShootingGuardPosition()

        if Position.SMALL_FORWARD not in self.small_forward.positions:
            raise InvalidSmallForwardPosition()

        if Position.POWER_FORWARD not in self.power_forward.positions:
            raise InvalidPowerForwardPosition()

        if Position.CENTER not in self.center.positions:
            raise InvalidCenterPosition()

        if is_disjoint(self.guard.positions, Lineup.GUARD_POSITIONS):
            raise InvalidGuardPosition()

        if is_disjoint(self.forward.positions, Lineup.FORWARD_POSITIONS):
            raise InvalidForwardPosition()

        if is_disjoint(self.utility.positions, Lineup.UTILITY_POSITIONS):
            raise InvalidUtilityPosition()
