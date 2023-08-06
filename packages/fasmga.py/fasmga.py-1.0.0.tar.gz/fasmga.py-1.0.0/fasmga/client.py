import asyncio
import typing
from aiohttp import ClientResponse, ClientSession, ClientResponseError
from .utils import DictWithoutNones, TotallyARunningLoop
from .errors import *
from .url import URL


class Client:
    FASMGA_API_URL = "http://fasmvps.ga:2002"

    def __init__(
        self,
        token,
        loop: asyncio.AbstractEventLoop = None,
        session: ClientSession = None,
        discord=False,
    ):
        self._session = session
        self.token = token
        self.loop = loop or asyncio.get_event_loop()
        self.has_created_loop = loop == None
        self.has_created_session = session == None
        self.discord = discord
        self.running_url_loop = TotallyARunningLoop()
        self.urls: typing.List[URL] = []
        self._ready = asyncio.Event()

    @property
    def session(self) -> ClientSession:
        if self._session == None:
            self._session = ClientSession(loop=self.loop)

        return self._session

    async def on_ready(self):
        return

    async def handle_status_codes(self, request: ClientResponse, datas: dict = {}):
        cls = HTTPException
        if request.status == 429:
            cls = TooManyRequests
        elif request.status == 400:
            cls = BadRequest

        return await self.on_http_exception(cls(request.status, datas))

    async def on_http_exception(self, error: HTTPException):
        raise error

    async def test_connection(self):
        tosend = {"Authorization": self.token}
        ratelimit = await self.session.get(
            self.FASMGA_API_URL + "/ratelimit", headers=tosend
        )
        data = await ratelimit.json()
        try:
            ratelimit.raise_for_status()
        except ClientResponseError:
            return await self.handle_status_codes(ratelimit, datas=data)


    async def request(self, uri, **kwargs):
        kwargs.update({"token": self.token})
        await self.test_connection()
        resp = await self.session.post(self.FASMGA_API_URL + uri, data=kwargs)
        ret = await resp.json()
        try:
            resp.raise_for_status()
        except ClientResponseError:
            return await self.handle_status_codes(resp, datas=ret)

        return ret

    async def shorten(
        self, url, custom_id=None, password=None, *, nsfw=False, idtype="abcdefgh"
    ):
        idtypes = ["abcdefgh", "abc12345", "aBCde"]
        if not idtype in idtypes:
            raise TypeError(f"Invalid ID type. Must be one between {idtypes}.")

        id = (
            await self.request(
                "/create",
                **DictWithoutNones(
                    url=url,
                    nsfw=nsfw,
                    idtype=idtype,
                    id=custom_id,
                    password=password,
                ),
            )
        )["success"]

        ret = URL(self, redirect_url=url, ID=id, nsfw=nsfw)
        self.urls.append(ret)

        return ret

    async def fetch_all_urls(self):
        urls: typing.List[dict] = await self.request("/list")
        ret: typing.List[URL] = []
        for url in urls:
            ret.append(URL(self, **url))

        return ret

    def get_url(self, id):
        for url in self.urls:
            if url.id == id:
                return url

    async def url_loop(self):
        while True:
            urls = await self.fetch_all_urls()
            for url in urls:
                if not self.get_url(url.id):
                    self.urls.append(url)

                await asyncio.sleep(0)

            self._ready.set()
            await asyncio.sleep(10)

    def start_url_loop(self):
        if self.discord:
            from discord.ext import tasks

            self.running_url_loop = tasks.loop()(self.url_loop)
            self.running_url_loop.start()
        else:
            self.running_url_loop = asyncio.ensure_future(self.url_loop())

    async def wait_until_ready(self):
        return await self._ready.wait()

    async def connect(self):
        await self.test_connection()
        self.start_url_loop()
        await self.wait_until_ready()
        await self.on_ready()

    def start(self):
        try:
            self.loop.run_until_complete(self.connect())
            self.loop.run_forever()
        finally:
            self.loop.run_until_complete(self.close())

    async def close(self):
        self.running_url_loop.cancel()
        if self.has_created_session:
            await self.session.close()

        if self.has_created_loop:
            self.loop.stop()

    def on(self, event):
        if event.startswith("on_"):
            event = event.replace("on_", "", 1)

        def decorate(func):
            setattr(self, f"on_{event}", func)
            return func

        return decorate

    async def edit(self, id, *, url=None, password=None, nsfw=False):
        return await self.request(
            "/edit",
            **DictWithoutNones(
                id=id,
                url=url,
                nsfw=nsfw,
                password=password,
            ),
        )
