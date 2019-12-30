from .user import PartialUser
from .errors import NoPossibleConversionException
from .genericutils import get_datetime_from


class Follower:
    """
    Defines a twitch follower
    """

    __slots__ = ('_follower', '_following', '_followed_at')

    def __init__(self, client, data):
        self._follower = PartialUser(client, data['from_id'], data['from_name'])
        self._following = PartialUser(client, data['to_id'], data['to_name'])
        self._followed_at = get_datetime_from(data['followed_at'])

    def __eq__(self, other):
        if isinstance(other, Follower):
            return self._follower == other.follower and self._following == other.following and self._followed_at == other.followed_at
        else:
            raise NoPossibleConversionException(f"Cannot compare type <{type(Follower)}> to <{type(other)}>")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"<Follower - {self._follower} -> {self._following} : {self._followed_at}>"

    def __str__(self):
        return f"Follower: {self._follower} followed {self._following} at {self._followed_at}"

    @property
    def follower(self):
        return self._follower

    @property
    def following(self):
        return self._following

    @property
    def followed_at(self):
        return self._followed_at
