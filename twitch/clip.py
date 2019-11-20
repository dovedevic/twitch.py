from datetime import datetime
from .errors import NoPossibleConversionException, NotAuthorizedException
from .user import PartialUser
from .game import PartialGame
from .genericutils import get_datetime_from


class Clip:
    """
    Defines a twitch clip
    """

    __slots__ = ('_id', '_timestamp', '_broadcaster', '_creator', '_video_id', '_game', '_language', '_title', '_view_count', '_thumbnail_url', '_clip_url', '_embed_url', '_edit_url')

    def __init__(self, data):
        self._id = data['id']
        self._timestamp = get_datetime_from(data['created_at'])
        self._broadcaster = PartialUser(data['broadcaster_id'], data['broadcaster_name'])
        self._creator = PartialUser(data['creator_id'], data['creator_name'])
        self._video_id = data['video_id']
        self._game = PartialGame(data['game_id'])
        self._language = data['language']
        self._title = data['title']
        self._view_count = data['view_count']
        self._thumbnail_url = data['thumbnail_url']
        self._clip_url = data['url']
        self._embed_url = data['embed_url']
        self._edit_url = data['edit_url'] if 'edit_url' in data else ''

    def __eq__(self, other):
        if isinstance(other, Clip):
            return other.id == self._id
        elif isinstance(other, str):
            return other == self._id
        else:
            raise NoPossibleConversionException(f"Cannot compare type <{type(Clip)}> to <{type(other)}>")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"<Clip - id:{self._id} title:{self._title} timestamp:{str(self._timestamp)}>"

    def __str__(self):
        return f"Clip {self._id}: {self._creator} clipped {self._broadcaster} for game {self._game.id} and called it '{self._title}'"

    @property
    def id(self):
        return self._id

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def broadcaster(self):
        return self._broadcaster

    @property
    def creator(self):
        return self._creator

    @property
    def video_id(self):
        return self._video_id

    @property
    def game(self):
        return self._game

    @property
    def language(self):
        return self._language

    @property
    def title(self):
        return self._title

    @property
    def view_count(self):
        return self._view_count

    @property
    def thumbnail__url(self):
        return self._thumbnail_url

    @property
    def clip_url(self):
        return self._clip_url

    @property
    def embed_url(self):
        return self._embed_url

    @property
    def edit_url(self):
        if self._edit_url:
            return self._edit_url
        else:
            raise NotAuthorizedException("You are not authorized to view the edit url")
