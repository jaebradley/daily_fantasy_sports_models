from dataclasses import dataclass


class InvalidPlayerError(ValueError):
    pass


class InvalidIdError(InvalidPlayerError):
    pass


class InvalidNameError(InvalidPlayerError):
    pass


@dataclass(init=True,
           repr=True,
           eq=True,
           order=False,
           unsafe_hash=False,
           frozen=True)
class Player:
    id: str  # pylint: disable=invalid-name
    name: str

    def __post_init__(self):
        if "".__eq__(self.id):
            raise InvalidIdError()

        if "".__eq__(self.name):
            raise InvalidNameError()
