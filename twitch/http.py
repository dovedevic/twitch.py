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
        if isinstance(user, str) and not user.isdigit():
            return await self.request('GET', f'/users?login={user}')
        elif isinstance(user, int) or user.isdigit():
            return await self.request('GET', f'/users?id={user}')

    async def get_users(self, users):
        params = ''

        if isinstance(users[0], str) and not users[0].isdigit():
            params += f'?login={users[0]}'
        elif isinstance(users[0], int) or users[0].isdigit():
            params += f'?id={users[0]}'

        for u in users:
            # Skip over first user as its already provided in params
            if users.index(u) == 0:
                continue

            if isinstance(u, str) and not u.isdigit():
                params += f'&login={u}'
            elif isinstance(u, int) or u.isdigit():
                params += f'&id={u}'

        print(params, await self.request('GET', f'/users{params}'))
        return await self.request('GET', f'/users{params}')

    async def get_game(self, game):
        if isinstance(game, str) and not game.isdigit():
            return await self.request('GET', f'/games?name={game}')
        elif isinstance(game, int) or game.isdigit():
            return await self.request('GET', f'/games?id={game}')

    async def get_games(self, games):
        params = ''

        if isinstance(games[0], str) and not games[0].isdigit():
            params += f'?name={games[0]}'
        elif isinstance(games[0], int) or games[0].isdigit():
            params += f'?id={games[0]}'

        for g in games:
            # Skip over first game as its already provided in params
            if games.index(g) == 0:
                continue

            if isinstance(g, str) and not g.isdigit():
                params += f'&name={g}'
            elif isinstance(g, int) or g.isdigit():
                params += f'&id={g}'

        return await self.request('GET', f'/games{params}')
