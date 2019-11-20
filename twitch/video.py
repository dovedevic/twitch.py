from .genericutils import get_datetime_from
from .errors import NoPossibleConversionException, APIMissMatchException
from .user import PartialUser


class VideoType:
    """
    Defines the broadcasters twitch distinguishes
    """

    Upload = 'upload'
    Archive = 'archive'
    Highlight = 'highlight'

    @staticmethod
    def ensure_type(vtype):
        if vtype == VideoType.Upload or \
           vtype == VideoType.Archive or \
           vtype == VideoType.Highlight:
            return vtype
        else:
            raise APIMissMatchException(f'VideoType<{vtype}> is not valid!')


class Video:
    """
    Defines a twitch stream VOD or video
    """

    __slots__ = ('_id', '_broadcaster', '_title', '_description', '_created_at', '_published_at', '_url', '_thumbnail_url', '_viewable', '_view_count', '_language', '_type', '_duration')

    def __init__(self, data):
        self._id = data['id']
        self._broadcaster = PartialUser(data['user_id'], data['user_name'])
        self._title = data['title']
        self._description = data['description']
        self._created_at = get_datetime_from(data['created_at'])
        self._published_at = get_datetime_from(data['published_at'])
        self._url = data['url']
        self._thumbnail_url = data['thumbnail_url']
        self._viewable = data['viewable'] == 'public'
        self._view_count = data['view_count']
        self._language = data['language']
        self._type = VideoType.ensure_type(data['type'])
        self._duration = data['duration']

    def __eq__(self, other):
        if isinstance(other, Video):
            return other.id == self._id
        elif isinstance(other, int):
            return other == int(self._id)
        elif isinstance(other, str):
            return other == self._id
        else:
            raise NoPossibleConversionException(f"Cannot compare type <{type(Video)}> to <{type(other)}>")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"<Video - id:{self._id} desc:{self._description} url:{self._url}>"

    def __str__(self):
        return self._id

    @property
    def id(self):
        return self._id

    @property
    def broadcaster(self):
        return self._broadcaster

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def created_at(self):
        return self._created_at

    @property
    def published_at(self):
        return self._published_at

    @property
    def url(self):
        return self._url

    @property
    def thumbnail_url(self):
        return self._thumbnail_url

    @property
    def viewable(self):
        return self._viewable

    @property
    def view_count(self):
        return self._view_count

    @property
    def language(self):
        return self._language

    @property
    def type(self):
        return self._type

    @property
    def duration(self):
        return self._duration

