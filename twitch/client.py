import asyncio
import signal
import typing

from .game import Game
from .http import HTTPConnection
from .errors import TwitchException
from .scope import Scope
from .user import User


class Twitch:
    def __init__(self, client_id, client_secret, *, loop=None, capabilities: typing.List[Scope] = None):
        self.loop = loop or asyncio.get_event_loop()
        self.http = HTTPConnection(client_id, loop=self.loop)
        self._client_id = client_id
        self._client_secret = client_secret
        self._capabilities = capabilities or []

        self.loop.add_signal_handler(signal.SIGTERM, lambda: self.close())

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
        return Game(data[data][0])

    async def get_games(self, *games: typing.Union[int, str]):
        if len(games) > 100:
            raise TwitchException('Game amount cannot be greater than 100')

        data = await self.http.get_games(games)

        ret = []

        for i in range(len(data['data'])):
            ret.append(Game(data['data'][i]))

        return ret

    async def close(self):
        if self.http is not None:
            await self.http.close()

        if self.loop.is_running():
            self.loop.stop()

        if not self.loop.is_closed():
            self.loop.close()
