from .channel import ChatChannel
from .user import PartialUser, User
from .game import PartialGame, Game
from .tags import PartialTag, Tag
from .genericutils import get_datetime_from
from .errors import NoPossibleConversionException, InvalidOperationException


class Stream(ChatChannel):
    """
    Defines a twitch stream
    """
    __slots__ = ('_client', '_id', '_broadcaster', '_game', '_is_live', '_title', '_viewer_count', '_started_at', '_language', '_format_thumbnail_url', '_tags')

    def __init__(self, client, data):
        self._client = client
        self._id = data['id']
        self._broadcaster = PartialUser(data['user_id'], data['user_name'])
        self._game = PartialGame(data['game_id'])
        self._is_live = True if data['type'] == 'live' else False
        self._title = data['title']
        self._viewer_count = data['viewer_count']
        self._started_at = get_datetime_from(data['started_at'])
        self._language = data['language']
        self._format_thumbnail_url = data['thumbnail_url']
        self._tags = []
        for tag in data['tag_ids']:
            self._tags.append(PartialTag(tag))

    def __str__(self):
        return f"{self._broadcaster.username}'s Stream"

    def __repr__(self):
        return f"<Stream - id:{self._id} username:{self._broadcaster.username}>"

    def __eq__(self, other):
        if isinstance(other, Stream):
            return other.id == self._id
        elif isinstance(other, int):
            return other == int(self._id)
        elif isinstance(other, str):
            return other == self._id
        else:
            raise NoPossibleConversionException(f"Cannot compare type <{type(Stream)}> to <{type(other)}>")

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def id(self):
        return self._id

    @property
    def broadcaster(self):
        return self._broadcaster

    @property
    def game(self):
        return self._game

    @property
    def is_live(self):
        return self._is_live

    @property
    def title(self):
        return self._title

    @property
    def viewer_count(self):
        return self._viewer_count

    @property
    def started_at(self):
        return self._started_at

    @property
    def language(self):
        return self._language

    @property
    def format_thumbnail_url(self):
        return self._format_thumbnail_url

    @property
    def tags(self):
        return self._tags

    async def fetch_streamer(self):
        if not isinstance(self._broadcaster, User):
            self._broadcaster = await self._broadcaster.fetch_user()
        return self._broadcaster

    async def fetch_game(self):
        if not isinstance(self._game, Game):
            self._game = await self._game.fetch_game()
        return self._game

    async def fetch_tags(self):
        update = []
        for tag in self._tags:
            if not isinstance(tag, Tag):
                update.append(tag.id)
        # TODO:: self._tags = await client.fetch_tags(update)
        return self._tags

    async def update_description(self, description):
        streamer = await self.fetch_streamer()
        return await streamer.update_description(description)

    async def get_extensions(self):
        streamer = await self.fetch_streamer()
        return await streamer.get_extensions()

    async def get_active_extensions(self):
        streamer = await self.fetch_streamer()
        return await streamer.get_active_extensions()

    async def update_extensions(self, extensions):
        streamer = await self.fetch_streamer()
        return await streamer.update_extensions(extensions)

    async def update_metadata(self):
        streamer = await self.fetch_streamer()
        return await streamer.update_metadata()

    async def get_followers(self):
        streamer = await self.fetch_streamer()
        return streamer.get_followers()

    async def get_following(self):
        streamer = await self.fetch_streamer()
        return streamer.get_following()

    async def get_clips(self):
        streamer = await self.fetch_streamer()
        return streamer.get_clips()

    async def create_clip(self):
        streamer = await self.fetch_streamer()
        await self.update_metadata()
        if self.is_live:
            # TODO:: return await client.create_clip(streamer)
            pass
        else:
            raise InvalidOperationException("Cannot create a clip when the stream is offline")

    async def get_bits_leaderboard(self, **kwargs):
        streamer = await self.fetch_streamer()
        # TODO:: return await client.get_bits_leaderboard(streamer, kwargs)
        pass

    async def create_marker(self):
        streamer = await self.fetch_streamer()
        await self.update_metadata()
        if self.is_live:
            # TODO:: return await client.create_marker(streamer)
            pass
        else:
            raise InvalidOperationException("Cannot create a marker when the stream is offline")

    async def get_markers(self):
        streamer = await self.fetch_streamer()
        return streamer.get_markers()

    async def get_subscribers(self):
        streamer = await self.fetch_streamer()
        return streamer.get_subscribers()

    async def replace_stream_tags(self, tags):
        # TODO:: rep_tags =  await client.replace_tags(streamer, tags)
        rep_tags = None
        self._tags = rep_tags
        return tags

    async def get_videos(self):
        streamer = await self.fetch_streamer()
        return streamer.get_videos()
