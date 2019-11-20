from .errors import APIMissMatchException, NoPossibleConversionException
from .user import PartialUser, BannedPartialUser
from .genericutils import get_datetime_from, get_default_timestamp


class ModerationEventType:
    """
    Defines the type of moderation event type twitch distinguishes
    """

    Ban = 'moderation.user.ban'  # String that tracks the ban event
    Unban = 'moderation.user.unban'  # String that tracks the unban event

    @staticmethod
    def ensure_type(etype):
        if etype == ModerationEventType.Ban or etype == ModerationEventType.Unban:
            return etype
        else:
            raise APIMissMatchException(f'ModerationEventType<{etype}> is not valid!')


class ModerationEvent:
    """
    Defines a twitch moderation event
    """

    __slots__ = ('_id', '_timestamp', '_event_from', '_event_for', '_event_type', '_expires_at')

    def __init__(self, data):
        self._id = data['id']
        self._timestamp = get_datetime_from(data['event_timestamp'])
        self._event_from = PartialUser(data['event_data']['broadcaster_id'], data['event_data']['broadcaster_name'])
        self._event_for = BannedPartialUser(data['event_data']['user_id'], data['event_data']['user_name'], data['event_data']['expires_at'])
        self._event_type = ModerationEventType.ensure_type(data['event_type'])
        # This distinguishes "Moderation Event" from "Banned Event". We coalesce them here
        if 'expires_at' in data['event_data']:
            self._expires_at = get_datetime_from(data['event_data']['expires_at'])
        else:
            self._expires_at = get_default_timestamp()

    def __eq__(self, other):
        if isinstance(other, ModerationEvent):
            return other.id == self._id
        elif isinstance(other, int):
            return other == self._id
        elif isinstance(other, str):
            return other == self._id
        else:
            raise NoPossibleConversionException(f"Cannot compare type <{type(ModerationEvent)}> to <{type(other)}>")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"<ModerationEvent - id:{self._id} expat:{self._expires_at} timestamp:{str(self._timestamp)}>"

    def __str__(self):
        return f"ModerationEvent {self._id}: {self._event_for} was {self._event_type} from {self._event_from} on {self._timestamp} until {self._expires_at}"

    @property
    def id(self):
        return self._id

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def from_user(self):
        return self._event_from

    @property
    def for_user(self):
        return self._event_for

    @property
    def type(self):
        return self._event_type

    @property
    def expires_at(self):
        return self._expires_at
