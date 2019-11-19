import aiohttp
import asyncio
import logging


logger = logging.getLogger(__name__)


class HTTPConnection:
    BASE = 'https://api.twitch.tv/helix'

    def __init__(self, client_id, *, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self._client_id = client_id
        self._session = aiohttp.ClientSession(loop=loop)

    async def request(self, method, url, **kwargs):
        headers = kwargs.pop('headers', {})
        headers['Client-ID'] = self._client_id

        res = await self._session.request(method, f'{self.BASE}{url}', headers=headers)

        if res.status != 200:
            logger.warning(f'Request returned status {res.status} with reason: {res.reason}')

        return await res.json()

    async def close(self):
        if self._session:
            await self._session.close()

    async def get_user(self, user):
        if isinstance(user, str):
            return await self.request('GET', f'/users?login={user}')
        elif isinstance(user, int):
            return await self.request('GET', f'/users?id={user}')
