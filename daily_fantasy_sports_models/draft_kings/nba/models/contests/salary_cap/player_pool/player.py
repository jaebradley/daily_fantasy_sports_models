from dataclasses import dataclass
from typing import Set

from daily_fantasy_sports_models.draft_kings.nba.models.core.player import Player as CorePlayer
from daily_fantasy_sports_models.draft_kings.nba.models.core.position import Position


class InvalidPlayerError(ValueError):
    pass


class InvalidGameIdError(InvalidPlayerError):
    pass


class PositionsCannotBeEmptyError(InvalidPlayerError):
    pass


# "In salary cap contests, participants will create a lineup by selecting players listed in the Player Pool.
# Each player listed has an assigned salary"
@dataclass(init=True,
           repr=True,
           eq=True,
           order=False,
           unsafe_hash=False,
           frozen=True)
class Player:
    player: CorePlayer
    positions: Set[Position]
    game_id: str
    # DraftKings does not specify if a salary is guaranteed to be non-negative or positive
    salary: float

    def __post_init__(self):
        if "".__eq__(self.game_id):
            raise InvalidGameIdError()

        if 0 == len(self.positions):
            raise PositionsCannotBeEmptyError()
