import aiohttp
import asyncio
import logging
import websocket

from .errors import TwitchException


logger = logging.getLogger(__name__)


class HTTPConnection:
    BASE = 'https://api.twitch.tv/helix'

    def __init__(self, client_id, scopes, *, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self._client_id = client_id
        self._scopes = scopes
        self._session = aiohttp.ClientSession(loop=loop)

    async def rrequest(self, method, url, **kwargs):
        res = await self._session.request(method, url, **kwargs)

        if res.status != 200:
            logger.warning(f'RRequest returned status {res.status} with reason: {res.reason}')

        try:
            return await res.json()
        except:
            return await res.text()

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

        return await self.request('GET', f'/users{params}')

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

    async def get_stream_tags(self, tags, limit):
        # TODO
        pass


class WSConnection(HTTPConnection):
    def __init__(self, client_id, scopes, *, loop=None):
        super().__init__(client_id, scopes, loop=loop)

    async def irc_connect(self, channel, nick, oauth):
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect('wss://irc-ws.chat.twitch.tv:443/') as ws:
                logger.debug('IRC Connection started')
                if oauth.startswith('oauth'):
                    await ws.send_str(f'PASS {oauth}')
                else:
                    await ws.send_str(f'PASS oauth:{oauth}')

                await ws.send_str(f'NICK {nick}')
                await ws.send_str(f'JOIN #{channel}')

                # required to send messages
                await ws.send_str('CAP REQ :twitch.tv/membership')
                # required to get full user info and use commands w/ tags
                await ws.send_str(f'CAP REQ :twitch.tv/tags twitch.tv/commands')

                while not self.loop.is_closed():
                    res = (await ws.receive()).data.strip()
                    print(res)
