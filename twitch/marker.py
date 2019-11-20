from .genericutils import get_datetime_from
from .errors import NoPossibleConversionException


class Marker:
    """
    Defines a twitch stream marker
    """

    __slots__ = ('_id', '_timestamp', '_description', '_position', '_url')

    def __init__(self, data):
        self._id = data['id']
        self._timestamp = get_datetime_from(data['created_at'])
        self._description = data['description']
        self._position = data['position_seconds']
        self._url = data['URL'] if 'URL' in data else ''

    def __eq__(self, other):
        if isinstance(other, Marker):
            return other.id == self._id
        elif isinstance(other, str):
            return other == self._id
        else:
            raise NoPossibleConversionException(f"Cannot compare type <{type(Marker)}> to <{type(other)}>")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"<Marker - id:{self._id} desc:{self._description} url:{self._url}>"

    def __str__(self):
        return self._id

    @property
    def id(self):
        return self._id

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def description(self):
        return self._description

    @property
    def position_in_seconds(self):
        return self._position

    @property
    def marker_url(self):
        return self._url
