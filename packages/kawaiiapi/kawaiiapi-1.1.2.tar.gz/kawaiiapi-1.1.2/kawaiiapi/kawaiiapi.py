import aiohttp


class Kawaii:
    def __init__(self, token):
        self.token = token

    async def get(self, main, endpoint, f=None):
        if f is None:
            f = []
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://kawaii.red/api/{main}/{endpoint}/token={self.token}&filter={f}/") as url:
                image = await url.json()
                return image["response"]

    async def endpoints(self, main=None):
        if main is None:
            main = "gif"
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://kawaii.red/api/{main}/endpoints/token={self.token}/") as url:
                points = await url.json()
                return points["response"]

