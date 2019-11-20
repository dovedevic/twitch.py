import asyncio
import signal
import typing

from datetime import datetime
from .game import Game, PartialGame
from .extension import Extension
from .http import HTTPConnection, WSConnection
from .errors import TwitchException
from .user import User, PartialUser, BannedPartialUser
from .stream import Stream
from .video import Video
from .transaction import Transaction
from .clip import Clip
from .tags import Tag, PartialTag


class Twitch:
    def __init__(self, client_id, client_secret, *, loop=None, capabilities: list = None):
        self.coros = []
        self.loop = loop or asyncio.get_event_loop()
        self._access_token = None
        self._client_id = client_id
        self._client_secret = client_secret
        self._capabilities = capabilities or []
        self._refresh_token = None
        self.http = HTTPConnection(client_id, self._capabilities, loop=self.loop)
        self.ws = WSConnection(client_id, [], loop=self.loop)

        self.loop.add_signal_handler(signal.SIGTERM, lambda: self.close())
    
    # https://dev.twitch.tv/docs/api/reference#get-extension-analytics
    async def get_extension_analytics_url(self, extension: typing.Union[str, Extension] = None, limit: int = 20, started_at: datetime = None, ended_at: datetime = None, analytics_type: str = None):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-game-analytics
    async def get_game_analytics_url(self, game: typing.Union[int, str, Game, PartialGame] = None, limit: int = 20, started_at: datetime = None, ended_at: datetime = None, analytics_type: str = None):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-bits-leaderboard
    async def get_bits_leaderboard(self, user: typing.Union[int, str, Stream, User, PartialUser, BannedPartialUser], limit: int = 10, started_at: datetime = None, period: str = 'all'):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-extension-transactions
    async def get_extension_transactions(self, extension: typing.Union[str, Extension], transaction: typing.Union[str, Transaction] = None, limit: int = 20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#create-clip
    async def create_clip(self, stream: typing.Union[int, str, Stream], clip_after_delay: bool = False):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-clips
    async def get_clips(self, stream: typing.Union[int, str, Stream, User, PartialUser, BannedPartialUser], game: typing.Union[int, str, Game, PartialGame] = None, clip: typing.Union[str, Clip] = False):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#create-entitlement-grants-upload-url
    async def get_entitlement_upload_url(self, manifest: typing.Union[int, str]):
        # TODO Entitlements later
        pass

    # https://dev.twitch.tv/docs/api/reference#get-code-status
    async def get_entitlement_codes_status(self, user: typing.Union[int, str, User, PartialUser, BannedPartialUser], *codes: str):
        # TODO Entitlements later
        pass

    # https://dev.twitch.tv/docs/api/reference#get-code-status
    async def get_entitlement_code_status(self, user: typing.Union[int, str, User, PartialUser, BannedPartialUser], code: str):
        # Alias
        return await self.get_entitlement_codes_status(user, code)

    # https://dev.twitch.tv/docs/api/reference#redeem-code
    async def redeem_entitlement_codes(self, user: typing.Union[int, str, User, PartialUser, BannedPartialUser], *codes: str):
        # TODO Entitlements later
        pass

    # https://dev.twitch.tv/docs/api/reference#redeem-code
    async def redeem_entitlement_code(self, user: typing.Union[int, str, User, PartialUser, BannedPartialUser], code: str):
        return await self.redeem_entitlement_codes(user, code)

    # https://dev.twitch.tv/docs/api/reference#get-top-games
    async def get_top_games(self, limit: int=20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-games
    async def get_game(self, game: typing.Union[int, str, Game, PartialGame]):
        return await self.get_games(game)

    # https://dev.twitch.tv/docs/api/reference#get-games
    async def get_games(self, *games: typing.Union[int, str, Game, PartialGame]):
        if len(games) > 100:
            raise TwitchException('Game amount cannot be greater than 100')

        data = await self.http.get_games(games)

        ret = []

        for i in range(len(data['data'])):
            ret.append(Game(data['data'][i]))

        return ret

    # https://dev.twitch.tv/docs/api/reference#check-automod-status
    async def are_messages_allowed(self, stream: typing.Union[int, str, Stream], *messages: str):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#check-automod-status
    async def is_message_allowed(self, stream: typing.Union[int, str, Stream], message: str):
        # Alias
        return await self.are_messages_allowed(stream, message)

    # https://dev.twitch.tv/docs/api/reference#get-banned-events
    async def get_banned_events(self, stream: typing.Union[int, str, Stream], for_users: typing.Union[int, str, User, PartialUser, BannedPartialUser] = None, limit: int = 20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-banned-users
    async def get_banned_users(self, stream: typing.Union[int, str, Stream], for_users: typing.Union[int, str, User, PartialUser, BannedPartialUser] = None):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-moderators
    async def get_moderators(self, stream: typing.Union[int, str, Stream], for_users: typing.Union[int, str, User, PartialUser] = None):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-moderator-events
    async def get_moderator_events(self, stream: typing.Union[int, str, Stream], for_users: typing.Union[int, str, User, PartialUser] = None):
        # Alias
        return await self.get_banned_events(stream, for_users=for_users)

    # https://dev.twitch.tv/docs/api/reference#get-streams
    async def get_stream(self, user: typing.Union[int, str, User, PartialUser, BannedPartialUser]):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-streams
    async def get_streams(self, users: typing.Union[int, str, User, PartialUser, BannedPartialUser] = None, games: typing.Union[int, str, Game, PartialGame] = None, language: str = 'en', limit: int = 20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-streams-metadata
    async def get_streams_metadata(self, users: typing.Union[int, str, User, PartialUser, BannedPartialUser] = None, games: typing.Union[int, str, Game, PartialGame] = None, language: str = 'en', limit: int = 20):
        # TODO Figure out API later
        pass

    # https://dev.twitch.tv/docs/api/reference#get-streams-metadata
    async def get_stream_metadata(self, user: typing.Union[int, str, User, PartialUser, BannedPartialUser]):
        # Alias
        return await self.get_streams_metadata(user)

    # https://dev.twitch.tv/docs/api/reference#create-stream-marker
    async def create_stream_marker(self, stream: typing.Union[int, str, Stream], description: str = None):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-stream-markers
    async def get_stream_markers(self, from_type: typing.Union[Stream, Video], limit: int = 20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-broadcaster-subscriptions
    async def get_subscriptions(self, user: typing.Union[int, str, Stream, User, PartialUser, BannedPartialUser], for_users: typing.Union[int, str, User, PartialUser, BannedPartialUser] = None):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-all-stream-tags
    async def get_all_stream_tags(self, limit: int = 20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-all-stream-tags
    async def get_stream_tags(self, tags: typing.Union[str, Tag, PartialTag], limit: int = 20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-all-stream-tags
    async def get_stream_tag(self, tag: typing.Union[str, Tag, PartialTag], limit: int = 20):
        # Alias
        return await self.get_stream_tags(tag, limit=limit)

    # https://dev.twitch.tv/docs/api/reference#get-stream-tags
    async def get_streamer_tags(self, stream: typing.Union[int, str, Stream]):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#replace-stream-tags
    async def replace_streamer_tags(self, stream: typing.Union[int, str, Stream], tags: typing.Union[str, Tag, PartialTag]):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-users
    async def get_user(self, user: typing.Union[int, str, User, PartialUser, BannedPartialUser]):
        return await self.get_users(user)

    # https://dev.twitch.tv/docs/api/reference#get-users
    async def get_users(self, *users: typing.Union[int, str, User, PartialUser, BannedPartialUser]):
        if len(users) > 100:
            raise TwitchException('User amount cannot be greater than 100')

        data = await self.http.get_users(users)

        ret = []

        for i in range(len(data['data'])):
            ret.append(User(self, data['data'][i]))

        return ret

    # https://dev.twitch.tv/docs/api/reference#get-users-follows
    async def get_followers(self, user: typing.Union[int, str, Stream, User, PartialUser, BannedPartialUser], limit: int = 20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-users-follows
    async def get_followings(self, user: typing.Union[int, str, Stream, User, PartialUser, BannedPartialUser], limit: int = 20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#update-user
    async def update_description(self, user: typing.Union[int, str, User, PartialUser, BannedPartialUser], description: str):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-user-extensions
    async def get_extensions(self, user: typing.Union[int, str, User, PartialUser, BannedPartialUser]):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-user-active-extensions
    async def get_active_extensions(self, user: typing.Union[int, str, User, PartialUser, BannedPartialUser]):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#update-user-extensions
    async def update_extensions(self, user: typing.Union[int, str, User, PartialUser, BannedPartialUser], extensions: typing.Union[str, Extension]):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-videos
    async def get_videos(self, *for_object: typing.Union[int, str, Video, User, PartialUser, BannedPartialUser, Game, PartialGame]):
        # TODO
        if len(for_object) > 100:
            raise TwitchException('Length of objects cannot be greater than 100')

        pass

    # https://dev.twitch.tv/docs/api/reference#get-videos
    async def get_video(self, video: Video):
        return await self.get_videos(video)

    # https://dev.twitch.tv/docs/api/reference#get-webhook-subscriptions
    async def get_webhooks(self, user: typing.Union[int, str, User, PartialUser, BannedPartialUser], limit: int = 20):
        # TODO
        pass

    # Temporary solution until actual coroutine running is setup
    def run_coro(self, coro):
        return self.loop.run_until_complete(coro)

    def run_coro_on_start(self, coro):
        self.coros.append(coro)

    async def close(self):
        if self.http is not None:
            await self.http.close()

        if self.loop.is_running():
            self.loop.stop()

        if not self.loop.is_closed():
            self.loop.close()

    def start_irc(self, channel_name, nickname, oauth):
        self.loop.create_task(self._connect(channel_name, nickname, oauth))
        self.loop.run_forever()

    async def _connect(self, name, nick, oauth):
        await self.ws.irc_connect(name, nick, oauth)

    def is_closed(self):
        return self.loop.is_closed()
