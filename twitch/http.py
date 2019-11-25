import aiohttp
import asyncio
import logging

from .errors import TwitchException
from .extension import Extension
from .game import Game, PartialGame
from .stream import Stream
from .transaction import Transaction
from .user import User, PartialUser, BannedPartialUser


logger = logging.getLogger(__name__)


class HTTPConnection:
    BASE = 'https://api.twitch.tv/helix'

    def __init__(self, client, client_id, scopes, *, loop=None):
        self._client = client
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

        for g in games[1:]:
            if isinstance(g, str) and not g.isdigit():
                params += f'&name={g}'
            elif isinstance(g, int) or g.isdigit():
                params += f'&id={g}'

        return await self.request('GET', f'/games{params}')

    async def get_stream(self, user):
        if isinstance(user, (User, PartialUser, BannedPartialUser)):
            return await self.request('GET', f'/streams/?user_id={user.id}')

        if isinstance(user, str) and not user.isdigit():
            return await self.request('GET', f'/streams/?user_login={user}')
        elif isinstance(user, int) or user.isdigit():
            return await self.request('GET', f'/streams/?user_id={user}')

    async def get_streams(self, users, games, langs, limit):
        params = f'?first={limit}'

        if type(langs) in (tuple, list):
            for lang in langs:
                params += f'&language={lang}'
        else:
            params += f'&language={langs}'

        if users:
            if type(users) in (tuple, list):
                for user in users:
                    if isinstance(user, (User, PartialUser, BannedPartialUser)):
                        params += f'&user_id={user.id}'
                    elif isinstance(user, str) and not user.isdigit():
                        params += f'&user_login={user}'
                    elif isinstance(user, int) or user.isdigit():
                        params += f'&user_id={user}'
            else:
                if isinstance(users, (User, PartialUser, BannedPartialUser)):
                    params += f'&user_id={users.id}'
                elif isinstance(users, str) and not users.isdigit():
                    params += f'&user_login={users}'
                elif isinstance(users, int) or users.isdigit():
                    params += f'&user_id={users}'

        if games:
            if type(games) in (tuple, list):
                for game in games:
                    if isinstance(game, (Game, PartialGame)):
                        params += f'&game_id={game.id}'
                    else:
                        params += f'&game_id={game}'
            else:
                if isinstance(games, (Game, PartialGame)):
                    params += f'&game_id={games.id}'
                else:
                    params += f'&game_id={games}'

        return await self.request('GET', f'/streams{params}')

    async def get_stream_tags(self, tags, limit):
        # TODO
        pass

    async def get_follows(self, *, to=None, _from=None, limit):
        if to:
            if isinstance(to, (User, PartialUser, BannedPartialUser)):
                return await self.request('GET', f'/users/follows?first={limit}&to_id={to.id}')
            elif isinstance(to, int) or to.isdigit():
                return await self.request('GET', f'/users/follows?first={limit}&to_id={to}')

        if _from:
            if isinstance(_from, (User, PartialUser, BannedPartialUser)):
                return await self.request('GET', f'/users/follows?first={limit}&from_id={_from.id}')
            elif isinstance(_from, int) or to.isdigit():
                return await self.request('GET', f'/users/follows?first={limit}&from_id={_from}')

    async def get_extension_transactions(self, extension, transaction, limit):
        params = ''

        if not self._client.app_token:
            raise TwitchException('Client method \'start\' was never called or coro was run before start')

        if isinstance(extension, Extension):
            if extension.id != self._client_id:
                raise TwitchException('Extension ID is not the same as the client ID')

            params += f'?extension_id={extension.id}'
        elif isinstance(extension, str):
            if extension != self._client_id:
                raise TwitchException('Extension ID is not the same as the client ID')

            params += f'?extension_id={extension}'

        if isinstance(transaction, list):
            for trans in transaction:
                if isinstance(trans, Transaction):
                    params += f'&id={trans.id}'
                elif isinstance(trans, str):
                    params += f'&id={trans}'
        elif isinstance(transaction, str):
            params += f'&id={transaction}'

        params += f'&first={limit}'

        return await self.request('GET', f'/extensions/transactions{params}', headers={
            'Authorization': f'Bearer {self._client.app_token}',
        })

    def is_closed(self):
        return self._session.closed


class WSConnection(HTTPConnection):
    def __init__(self, client, client_id, scopes, *, loop=None):
        super().__init__(client, client_id, scopes, loop=loop)

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
