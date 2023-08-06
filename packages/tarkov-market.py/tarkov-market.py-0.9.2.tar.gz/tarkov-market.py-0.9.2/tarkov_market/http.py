from __future__ import annotations

import json
import aiohttp
import asyncio
import weakref

from typing import (
    Any,
    ClassVar,
    Coroutine,
    Optional,
    Union,
    Dict,
    List,
    Type,
    TypeVar,
    TYPE_CHECKING,
)

from urllib.parse import quote as _uriquote

from . import utils
from .utils import MISSING
from .errors import LoginFailure

if TYPE_CHECKING:
    from .types import item

    from .types.item import LangType

    T = TypeVar('T')
    BE = TypeVar('BE', bound=BaseException)
    MU = TypeVar('MU', bound='MaybeUnlock')
    Response = Coroutine[Any, Any, T]


async def json_or_text(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text(encoding='utf-8')

    try:

        if response.headers['content-type'] == 'application/json; charset=utf-8':
            return json.loads(text)

    except KeyError:
        pass

    return text


class Route:
    BASE: ClassVar[str] = 'https://tarkov-market.com/api/v1'

    def __init__(self, method: str, path: str, **parameters: Any):
        self.path: str = path
        self.method: str = method

        url = "{}{}".format(self.BASE, path)

        if parameters:
            url = url.format_map({k: _uriquote(v) if isinstance(v, str) else v for k, v in parameters.items()})

        self.url = url

    @property
    def bucket(self) -> str:
        return f'{self.path}'


class MaybeUnlock:

    def __init__(self, lock: asyncio.Lock) -> None:
        self.lock: asyncio.Lock = lock
        self._unlock: bool = True

    def __enter__(self: MU) -> MU:
        return self

    def defer(self) -> None:
        self._unlock = False

    def __exit__(
        self,
        exc_type: Optional[Type[BE]],
        exc: Optional[BE],
        traceback
    ) -> None:

        if self._unlock:
            self.lock.release()


class HTTPClient:

    def __init__(
        self,
        connector: Optional[aiohttp.BaseConnector] = None,
        *,
        token: str,
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop() if loop is None else loop
        self.connector = connector
        self._locks: weakref.WeakValueDictionary = weakref.WeakValueDictionary()
        self.token: str = token
        self.__session: aiohttp.ClientSession = MISSING

    async def request(self, route: Route, **kwargs: Any) -> Any:
        bucket = route.bucket
        method = route.method
        url = route.url

        lock = self._locks.get(bucket)

        if lock is None:
            lock = asyncio.Lock()

            if bucket is not None:
                self._locks[bucket] = lock

        headers: Dict[str, str] = {
            "x-api-key": self.token,
        }

        if 'json' in kwargs:
            headers['Content-Type'] = 'application/json'
            kwargs['data'] = utils._to_json(kwargs.pop('json'))

        kwargs['headers'] = headers

        await lock.acquire()

        with MaybeUnlock(lock) as maybe_lock:

            for tries in range(5):

                try:

                    async with self.__session.request(method, url, **kwargs) as response:
                        data = await json_or_text(response)

                        if 'error' in data:
                            reason = data['error']

                            if reason == 'Access denied':
                                raise LoginFailure(f'{self.token} is Invalid API KEY.')

                            if reason in (
                                'You reach your limit of 300 reqs per minute',
                                'You reach your limit of 5 req per minute'
                            ):
                                maybe_lock.defer()
                                self.loop.call_later(60, lock.release)

                        if 300 > response.status >= 200:
                            return data

                        if response.status in {500, 502, 504}:
                            await asyncio.sleep(1 + tries * 2)
                            continue

                except OSError as e:

                    if tries < 4 and e.errno in (54, 10054):
                        await asyncio.sleep(1 + tries * 2)
                        continue

                    raise

    async def recreate(self):
        self.__session = aiohttp.ClientSession()

    async def close(self):

        if not self.__session.closed:
            await self.__session.close()

    async def __aenter__(self):

        if self.__session is not MISSING and self.__session.closed:
            await self.recreate()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
        return

    def get_item_by_name(
        self,
        name: str,
        *,
        lang: Optional[LangType] = None
    ) -> Response[List[item.Item]]:

        if lang:
            payload: Dict[str, str] = {
                "q": name,
                "lang": lang
            }
            r = Route('POST', '/item', json=payload)

        else:
            r = Route('GET', '/item?q={item_name}', item_name=name)

        return self.request(r)

    def get_item_by_uid(self, uid) -> Response[List[item.Item]]:
        r = Route('GET', '/item?uid={uid}', uid=uid)
        return self.request(r)

    def get_all_items(self) -> Response[List[item.Item]]:
        r = Route('GET', '/items/all')
        return self.request(r)

    def get_all_bsg_items(self) -> Response[List[item.BSGItem]]:
        r = Route('GET', '/bsg/items/all')
        return self.request(r)

    def save_json(self):
        r = Route('GET', '/bsg/items/all/download')
        return self.request(r)
