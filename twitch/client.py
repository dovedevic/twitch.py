import asyncio
import signal
import typing

from .game import Game
from .http import HTTPConnection
from .errors import TwitchException
from .scope import Scope
from .subscription import Subscription
from .user import User


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

        self.loop.add_signal_handler(signal.SIGTERM, lambda: self.close())

    # Temporary solution until actual coroutine running is setup
    def run_coro(self, coro):
        return self.loop.run_until_complete(coro)

    def run_coro_on_start(self, coro):
        self.coros.append(coro)

    async def get_user(self, user: typing.Union[int, str]):
        data = await self.http.get_user(user)
        return User(data['data'][0])

    async def get_users(self, *users: typing.Union[int, str]):
        if len(users) > 100:
            raise TwitchException('User amount cannot be greater than 100')

        data = await self.http.get_users(users)

        ret = []

        for i in range(len(data['data'])):
            ret.append(User(data['data'][i]))

        return ret

    async def get_game(self, game: typing.Union[int, str]):
        data = await self.http.get_game(game)
        return Game(data['data'][0])

    async def get_games(self, *games: typing.Union[int, str]):
        if len(games) > 100:
            raise TwitchException('Game amount cannot be greater than 100')

        data = await self.http.get_games(games)

        ret = []

        for i in range(len(data['data'])):
            ret.append(Game(data['data'][i]))

        return ret

    async def get_subscription(self, broadcaster_id: int, user: int = None):
        if Scope.Channel.Subscriptions.read() not in self._capabilities:
            raise TwitchException('Scope.Channel.Subscriptions is needed to view channel subscriptions')

        data = await self.http.get_subscription(broadcaster_id, user)
        # TODO: Remove this debug print when done
        print(data)
        return Subscription(data['data'][0])

    async def get_subscriptions(self, broadcaster_id: int, users: typing.List[int] = None):
        # TODO: Setup this
        if Scope.Channel.Subscriptions.read() not in self._capabilities:
            raise TwitchException('Scope.Channel.Subscriptions is needed to view channel subscriptions')

    def start(self):
        self.loop.create_task(self._start())
        self.loop.run_forever()

    async def _start(self):
        res = await self.http.rrequest('POST', f'https://id.twitch.tv/oauth2/token?client_id={self._client_id}' +
                                               f'&client_secret={self._client_secret}&grant_type=client_credentials' +
                                               f'&scope={" ".join(self._capabilities)}')

        # TODO: Deal with access_token
        print(res)

        for coro in self.coros:
            await coro

        await self._run()

    async def _run(self):
        pass

    async def close(self):
        if self.http is not None:
            await self.http.close()

        if self.loop.is_running():
            self.loop.stop()

        if not self.loop.is_closed():
            self.loop.close()

    def is_closed(self):
        return self.loop.is_closed()
