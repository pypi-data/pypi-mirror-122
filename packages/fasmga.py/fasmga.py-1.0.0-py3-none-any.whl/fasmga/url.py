class URL:
    def __init__(self, client, **kwargs):
        self.client = client
        self.id = kwargs["ID"].strip("/")
        self.uri = kwargs["redirect_url"]
        self.nsfw = kwargs["nsfw"]
        self.clicks = kwargs.get("clicks", 0)

    def __str__(self):
        return f"https://fasm.ga/{self.id}"

    def __repr__(self):
        return f"<URL id='{self.id}' uri='{self.uri}' nsfw={self.nsfw}>"

    async def edit(self, *, url=None, password=None, nsfw=False):
        await self.client.edit(self.id, url=url, password=password, nsfw=nsfw)
        self.uri = url
        self.nsfw = nsfw
