import asyncio
import typing

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

    async def get_user(self, user: typing.Union[int, str]):
        data = await self.http.get_user(user)
        return User(data['data'][0])

    async def get_users(self, *users: typing.Union[int, str]):
        if len(users) > 100:
            raise TwitchException('User amount cannot be greater than 100')

        ret = []

        for user in users:
            data = await self.http.get_user(user)
            ret.append(User(data['data'][0]))

        return ret

    async def close(self):
        if self.http is not None:
            await self.http.close()
