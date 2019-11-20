import asyncio
import signal
import typing

from .game import Game, PartialGame
from .extension import Extension
from .http import HTTPConnection
from .errors import TwitchException
from .scope import Scope
from .user import User, PartialUser, BannedPartialUser
from .stream import Stream
from .video import Video


class Twitch:
    def __init__(self, client_id, client_secret, *, loop=None, capabilities: typing.List[Scope] = None):
        self.loop = loop or asyncio.get_event_loop()
        self.http = HTTPConnection(client_id, loop=self.loop)
        self._client_id = client_id
        self._client_secret = client_secret
        self._capabilities = capabilities or []

        self.loop.add_signal_handler(signal.SIGTERM, lambda: self.close())

    # Temporary solution until actual coroutine running is setup
    def run_coro(self, coro):
        return self.loop.run_until_complete(coro)

    # https://dev.twitch.tv/docs/api/reference#get-extension-analytics
    async def get_extension_analytics_url(self, extension=None, limit=20, started_at=None, ended_at=None, analytics_type=None):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-game-analytics
    async def get_game_analytics_url(self, game=None, limit=20, started_at=None, ended_at=None, analytics_type=None):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-bits-leaderboard
    async def get_bits_leaderboard(self, user, limit=10, started_at=None, period='all'):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-extension-transactions
    async def get_extension_transactions(self, extension, transaction=None, limit=20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#create-clip
    async def create_clip(self, stream, clip_after_delay=False):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-clips
    async def get_clips(self, stream, game=None, clip=False):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#create-entitlement-grants-upload-url
    async def get_entitlement_upload_url(self, manifest):
        # TODO Entitlements later
        pass

    # https://dev.twitch.tv/docs/api/reference#get-code-status
    async def get_entitlement_codes_status(self, user, codes):
        # TODO Entitlements later
        pass

    # https://dev.twitch.tv/docs/api/reference#get-code-status
    async def get_entitlement_code_status(self, user, code):
        # TODO Entitlements later
        pass

    # https://dev.twitch.tv/docs/api/reference#redeem-code
    async def redeem_entitlement_code(self, user, code):
        # TODO Entitlements later
        pass

    # https://dev.twitch.tv/docs/api/reference#redeem-code
    async def redeem_entitlement_codes(self, user, codes):
        # TODO Entitlements later
        pass

    # https://dev.twitch.tv/docs/api/reference#get-top-games
    async def get_top_games(self, limit=20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-games
    async def get_game(self, game: typing.Union[int, str, Game, PartialGame]):
        data = await self.http.get_game(game)
        return Game(data[data][0])

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
    async def is_message_allowed(self, stream, message=None):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#check-automod-status
    async def are_messages_allowed(self, stream, messages=None):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-banned-events
    async def get_banned_events(self, stream, for_users=None, limit=20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-banned-users
    async def get_banned_users(self, stream, for_users=None):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-moderators
    async def get_moderators(self, stream, for_users=None):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-moderator-events
    async def get_moderator_events(self, stream, for_users=None):
        # Alias
        return await self.get_banned_events(stream, for_users=for_users)

    # https://dev.twitch.tv/docs/api/reference#get-streams
    async def get_stream(self, user):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-streams
    async def get_streams(self, users=None, games=None, language='en', limit=20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-streams-metadata
    async def get_stream_metadata(self, user):
        # TODO Figure out API later
        pass

    # https://dev.twitch.tv/docs/api/reference#get-streams-metadata
    async def get_streams_metadata(self, users=None, games=None, language='en', limit=20):
        # TODO Figure out API later
        pass

    # https://dev.twitch.tv/docs/api/reference#create-stream-marker
    async def create_stream_marker(self, stream, description=None):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-stream-markers
    async def get_stream_markers(self, from_type: typing.Union[Stream, Video], limit=20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-broadcaster-subscriptions
    async def get_subscriptions(self, user, for_users=None):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-all-stream-tags
    async def get_all_stream_tags(self, limit=20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-all-stream-tags
    async def get_stream_tags(self, tags, limit=20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-all-stream-tags
    async def get_stream_tag(self, tag, limit=20):
        # Alias
        return await self.get_stream_tags([tag], limit=limit)

    # https://dev.twitch.tv/docs/api/reference#get-stream-tags
    async def get_streamer_tags(self, stream):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#replace-stream-tags
    async def replace_streamer_tags(self, stream, tags):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-users
    async def get_user(self, user: typing.Union[int, str, User, PartialUser, BannedPartialUser]):
        data = await self.http.get_user(user)
        return User(self, data['data'][0])

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
    async def get_followers(self, user, limit=20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-users-follows
    async def get_followings(self, user, limit=20):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#update-user
    async def update_description(self, user, description):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-user-extensions
    async def get_extensions(self, user):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-user-active-extensions
    async def get_active_extensions(self, user):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#update-user-extensions
    async def update_extensions(self, user, extensions):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-videos
    async def get_videos(self, *for_object: typing.Union[int, str, Video, User, PartialUser, BannedPartialUser, Game, PartialGame]):
        # TODO
        pass

    # https://dev.twitch.tv/docs/api/reference#get-videos
    async def get_video(self, video):
        return await self.get_videos(video)

    # https://dev.twitch.tv/docs/api/reference#get-webhook-subscriptions
    async def get_webhooks(self, user, limit=20):
        # TODO
        pass

    async def close(self):
        if self.http is not None:
            await self.http.close()

        if self.loop.is_running():
            self.loop.stop()

        if not self.loop.is_closed():
            self.loop.close()
