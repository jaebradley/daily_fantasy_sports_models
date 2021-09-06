from dataclasses import dataclass
from enum import Enum
from typing import Set


class Position(Enum):
    POINT_GUARD = "POINT GUARD"
    SHOOTING_GUARD = "SHOOTING GUARD"
    SMALL_FORWARD = "SMALL FORWARD"
    POWER_FORWARD = "POWER FORWARD"
    CENTER = "CENTER"


class InvalidPlayerError(ValueError):
    pass


@dataclass(init=True,
           repr=True,
           eq=False,
           order=False,
           unsafe_hash=False,
           frozen=True)
class Player:
    id: str  # pylint: disable=invalid-name
    name: str
    positions: Set[Position]

    def __post_init__(self):
        if "".__eq__(self.id):
            raise InvalidPlayerError("id cannot be a blank string")

        if "".__eq__(self.name):
            raise InvalidPlayerError("name cannot be a blank string")

        if 0 == len(self.positions):
            raise InvalidPlayerError("positions cannot be empty")

    def __eq__(self, other):
        if isinstance(other, Player):
            return other.id == self.id
        return NotImplemented


class InvalidSalaryCapContestPlayerError(ValueError):
    pass


@dataclass(init=True,
           repr=True,
           eq=True,
           order=False,
           unsafe_hash=False,
           frozen=True)
class SalaryCapContestPlayer:
    player: Player
    game_id: str
    salary: float

    def __post_init__(self):
        if "".__eq__(self.game_id):
            raise InvalidSalaryCapContestPlayerError("game id cannot be a blank string")

        if 0 >= self.salary:
            raise InvalidSalaryCapContestPlayerError("salary must be a positive integer")


# "Contest results will be determined by the total points accumulated by each individual lineup entry"
@dataclass(init=True,
           repr=True,
           eq=True,
           order=False,
           unsafe_hash=False,
           frozen=True)
class SalaryCapContestResultPlayer(SalaryCapContestPlayer):
    points: float


class InvalidSalaryCapContestLineupError(ValueError):
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
class SalaryCapContestLineup:  # pylint: disable=too-many-instance-attributes
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

    point_guard: SalaryCapContestPlayer
    shooting_guard: SalaryCapContestPlayer
    small_forward: SalaryCapContestPlayer
    power_forward: SalaryCapContestPlayer
    center: SalaryCapContestPlayer
    guard: SalaryCapContestPlayer
    forward: SalaryCapContestPlayer
    utility_player: SalaryCapContestPlayer

    @staticmethod
    def is_disjoint(first: Set, second: Set):
        return 0 == len(first.intersection(second))

    def __post_init__(self):
        contest_players = [
            self.point_guard,
            self.shooting_guard,
            self.small_forward,
            self.power_forward,
            self.center,
            self.guard,
            self.forward,
            self.utility_player
        ]

        players = set(
            map(
                lambda contest_player: contest_player.player,
                contest_players
            )
        )

        if 8 != len(players):
            raise InvalidSalaryCapContestLineupError("each player must be unique")

        game_ids = set(
            map(
                lambda player: player.id,
                players
            )
        )

        if 2 > len(game_ids):
            raise InvalidSalaryCapContestLineupError("players from at least two games must be used")

        salary = sum(
            map(
                lambda contest_player: contest_player.salary,
                contest_players
            )
        )

        if 50_000 < salary:
            raise InvalidSalaryCapContestLineupError("players may not exceed a salary of $50,000")

        if SalaryCapContestLineup.is_disjoint(self.guard.player.positions, SalaryCapContestLineup.GUARD_POSITIONS):
            raise InvalidSalaryCapContestLineupError("invalid guard player positions")

        if SalaryCapContestLineup.is_disjoint(self.forward.player.positions, SalaryCapContestLineup.FORWARD_POSITIONS):
            raise InvalidSalaryCapContestLineupError("invalid forward player positions")

        if SalaryCapContestLineup.is_disjoint(self.utility_player.player.positions,
                                              SalaryCapContestLineup.UTILITY_POSITIONS):
            raise InvalidSalaryCapContestLineupError("invalid utility player positions")
