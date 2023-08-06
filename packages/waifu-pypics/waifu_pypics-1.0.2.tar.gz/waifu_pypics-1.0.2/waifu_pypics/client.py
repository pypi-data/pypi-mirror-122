import random
import asyncio
import typing
import requests

from .errors import *


class BaseClass:

    BASE_URL = "https://api.waifu.pics"

    def __init__(self, authorization: str = ""):
        self.user_agent = "WaifuPics-Api.py"
        self.authorization = authorization
        self._http = None
        self.endpoints = {
            'sfw': [
                'waifu', 'neko', 'shinobu',
                'megumin', 'bully', 'cuddle',
                'cry', 'hug', 'awoo',
                'kiss', 'lick', 'pat',
                'smug', 'bonk', 'yeet',
                'blush', 'smile', 'wave',
                'highfive', 'handhold', 'nom',
                'bite', 'glomp', 'slap',
                'kill', 'kick', 'happy',
                'wink', 'poke','dance',
                'cringe'
                ],
            'nsfw': [
                'waifu',
                'neko',
                'trap',
                'blowjob'
                ]
            }


class Waifu(BaseClass):
    
    def __init__(self, images_type: typing.Literal['sfw', 'nsfw']='sfw', authorization: str=""):
        super().__init__(authorization)
        self.images_type = images_type
        self._http = requests.Session()

    def _request(self, path: str, method: typing.Literal['get', 'post'], **kwargs):
        if method == 'get':
            response = self._http.get(self.BASE_URL + f'/{path}')
        else:
            response = self._http.post(self.BASE_URL + f'/{path}', json=kwargs)
        data = response.json()
        return data

    def get_image(self, image_category: str, image_type: str=None) -> dict:
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
        response = self._http.get(self.BASE_URL + f'/{image_type or self.images_type}' + f'/{image_category}')

        if response.ok:
            data = response.json()
        else:
            raise EndpointNotFound(f'Not found. Make sure the specified parameters are in the list of api endpoints: {self.endpoints}')
        return data['url']

    def random_image_category(self, image_type: str=None) -> str:
        """
        Returns an image of a random category from a given type, by default `SFW`.
        """
        return self.get_image(random.choice(self.endpoints[image_type or self.images_type]), image_type or self.images_type)

    def many(self, exclude: typing.Optional[list], image_category: str, image_type: str=None):
        return self._request(f'/many/{image_type or self.images_type}/{image_category}', 'post', {'exclude': exclude})
