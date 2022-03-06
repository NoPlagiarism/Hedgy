import aiohttp
import discord
from discord import Embed, File
from io import BytesIO
from .meta import Exists as Settings
import random
from loguru import logger
from time import time


random.seed(time())


class GetGenerator:
    """Generator init and get_embed stub"""
    name: str  # Name of generator
    url: str   # Generator url

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_embed(self) -> Embed:
        return Embed(title="LOL, debudge", description="Yeah, it is and " + str(type(self)), )


class OneImageGenerator(GetGenerator):
    """One image generator"""
    img_url: str   # Url of image

    def __init__(self, **kwargs):
        super(OneImageGenerator, self).__init__(**kwargs)
        self.img_url = kwargs.get("img_url", self.url)

    async def get_image(self) -> File:
        # Возвращает скачанное изображение
        async with aiohttp.ClientSession() as session:
            async with session.get(self.img_url, verify_ssl=False) as resp:
                image_raw = await resp.read()
        return File(fp=BytesIO(image_raw), filename=Settings.IMG_NAME)

    async def get_embed(self) -> Embed:
        embed = Embed()
        embed.set_author(name=self.name, url=self.url)
        embed.set_footer(text="Web: " + self.url)
        embed.set_image(url="attachment://" + Settings.IMG_NAME)
        return embed


class SeedMeta:
    """Класс, представляющий всю информацию о генераторе
    NAME - имя генератора
    URL - ссылка на сайт
    SET_SIZE - количество сгенерированных изображений
    MIN_SEED - минимальный сид
    SEED_LEN - длина сида
    SOURCE-URL - ссылка на изображение"""
    NAME: str
    URL: str

    SET_SIZE: int
    MIN_SEED: int
    SEED_LEN: int
    SOURCE_URL: str


class SeedGenerator(GetGenerator):
    """Seed Generator a-like Arfafax's websites (https://github.com/arfafax) or other webs
    https://thisfursonadoesnotexist.com and https://thisponydoesnotexist.net
    :arg meta: Class Like SeedMeta"""
    meta: SeedMeta

    def __init__(self, meta):
        kwargs = {"url": meta.URL, "name": meta.NAME}
        super(SeedGenerator, self).__init__(**kwargs)
        self.meta = meta

    def get_random_seed(self):
        return random.randint(self.meta.MIN_SEED, self.meta.SET_SIZE)

    def get_image_url(self, seed):
        return self.meta.SOURCE_URL.format(seed)

    def get_random_image_url(self):
        return self.get_image_url(self.get_random_seed())

    def get_embed(self, seed=None) -> Embed:
        if seed is None:
            seed = self.get_random_seed()
        embed = discord.Embed()
        embed.set_author(name=self.meta.NAME, url=self.url)
        seed_str = ("Seed: {seed:0" + str(self.meta.SEED_LEN) + "}")
        embed.set_footer(text=f"Web: {self.url} " + seed_str.format(seed=seed))
        embed.set_image(url=self.get_image_url(seed))
        return embed


class CityGenerator(GetGenerator):
    """Just http://thiscitydoesnotexist.com/"""
    async def get_image(self):
        """Получает url картинки через просто парсинг сайта"""
        async with aiohttp.ClientSession() as session:
            async with session.get("http://thiscitydoesnotexist.com/", verify_ssl=False) as resp:
                html = await resp.read()
        html = html.decode("utf-8")
        img_url_start = html.find("<img src=")+11
        img_url = "http://thiscitydoesnotexist.com/" + html[img_url_start:html[img_url_start:].find('"') + img_url_start]
        return img_url

    async def get_embed(self) -> Embed:
        embed = discord.Embed()
        embed.set_author(name="This City Does Not Exist", url="http://thiscitydoesnotexist.com/")
        embed.set_footer(text="Web: http://thiscitydoesnotexist.com/")
        embed.set_image(url=await self.get_image())
        return embed


class EyeGenerator(GetGenerator):
    """Just https://thiseyedoesnotexist.com/"""
    async def get_image(self):
        """Get image url from redirect"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://thiseyedoesnotexist.com/random/", allow_redirects=False) as resp:
                random_img_url = resp.headers["Location"]
        return "https://thiseyedoesnotexist.com/static/imgs/{}.png".format(random_img_url.split("/")[-1])

    async def get_embed(self) -> Embed:
        embed = discord.Embed()
        embed.set_author(name="This Eye Does Not Exist", url="http://thiseyedoesnotexist.com/")
        embed.set_footer(text="Web: http://thiseyedoesnotexist.com/")
        embed.set_image(url=await self.get_image())
        return embed
