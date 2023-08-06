import typing
import random
import asyncio
import aiohttp
import requests

from .errors import *
from .client import BaseClass


class WaifuAsync(BaseClass):
    
    def __init__(self, images_type: typing.Literal['sfw', 'nsfw']='sfw', authorization: str="", *, loop: asyncio.AbstractEventLoop=None):
        super().__init__(authorization)

        if loop is None:
            loop = asyncio.get_event_loop()

        self.images_type = images_type
        self._http = aiohttp.ClientSession(
            loop=loop,
            headers={
                "User-Agent": self.user_agent,
                "Authorization": self.authorization
            }
        )

    async def close(self):
        await self._http.close()

    async def _request(self, path: str) -> dict:
        async with self._http.get(self.BASE_URL + f'/{path}') as response:
            if not response.ok:
                raise EndpointNotFound(f'Not found. Make sure the specified parameters are in the list of api endpoints: {self.endpoints}')
            else:
                data = await response.json()
        return data

    async def get_image(self, image_category: str, image_type: str=None) -> str:
        """
        image_type: `https://api.waifu.pics/<image_type>/<image_category>`
        ------------------------------------------↑
            Image type is `SFW` or `NSFW`, default is `SFW`.

        image_category: `https://api.waifu.pics/<image_type>/<image_category>`
        ------------------------------------------------------------↑
            The image category you want.
            A list of all categories of the image type you need can be viewed at `https://waifu.pics/more` or using: `WaifuAsync().endpoints`
            this will return a list of all waifu-pics-api endpoints
        """
        data = await self._request(f'/{image_type or self.images_type}' + f'/{image_category}')
        return data['url']

    async def random_image_category(self, image_type: str=None) -> str:
        """
        Returns an image of a random category from a given type, by default `SFW`.
        """
        return await self.get_image(random.choice(self.endpoints[image_type or self.images_type]), image_type or self.images_type)
