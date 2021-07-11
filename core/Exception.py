class ChannelOccupiedException(Exception):
    pass


class PlayerOccupiedException(Exception):
    pass


class NoSuchGameException(Exception):
    pass


class NoSuchRoomException(Exception):
    pass


class PlayerNotInRoomException(Exception):
    pass


class NotOwnerException(Exception):
    pass


class InGamingException(Exception):
    pass


class NotInGamingException(Exception):
    pass


class GamePopulationException(Exception):
    pass


class UnexpectedErrorException(Exception):
    def __init__(self):
        super("If you see this error, please contact me.")


class GamePlayException(Exception):
    pass
