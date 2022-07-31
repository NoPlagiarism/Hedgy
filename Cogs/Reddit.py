from settings import Reddit as Settings, NSFWCheck
from Utils import RedditAIO, SubredditNotFound
from discord.ext import commands
from random import choice
from Utils import morph_numerals
from discord import DMChannel
from loguru import logger


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        reddit_aliases = list()
        for command_name, subreddit in Settings.COMMANDS.items():
            async def func(cls, ctx, sort: str = None, page_num: int = None):
                return await cls._reddit(ctx, subreddit, sort, page_num)
            command = commands.Command(func, name=command_name, cog=self, cog_name="Reddit")
            setattr(self, command_name, command)
            reddit_aliases.append(command)
        self.__cog_commands__ = self.__cog_commands__ + tuple(reddit_aliases)
        if Settings.LAST_REDDIT_URL:
            self.urls = dict()

    if Settings.LAST_REDDIT_URL:
        def cache_url(self, ctx, url):
            self.urls[ctx.channel.id] = url

        @commands.command(aliases=("reddit_last", "last"))
        async def last_reddit(self, ctx):
            if url := self.urls.get(ctx.channel.id):
                return await ctx.send("https://reddit.com" + url)
            return await ctx.reply(f"Сначала используйте комманду {ctx.prefix}reddit")
    else:
        def cache_url(self, ctx, url):
            pass

    async def _reddit(self, ctx, subreddit, sort, page_num):
        async with ctx.channel.typing():
            if subreddit is None:
                subreddit = Settings.DEF_SUBREDDIT
            elif not Settings.ENABLE_ALL_SUBREDDITS:
                if subreddit not in Settings.ENABLED_SUBREDDITS:
                    return await ctx.send("Данный сабреддит запрещён")
            if sort is None:
                sort = Settings.DEF_LISTING
            elif sort.upper() not in RedditAIO.Listings.__dict__:
                sort = Settings.DEF_LISTING

            if page_num is None:
                page_num = 0
            elif page_num <= 1:
                page_num = 0
            elif page_num >= 10:
                page_num = 9
            else:
                page_num -= 1

            if page_num != 0 and sort == RedditAIO.Listings.RANDOM:
                return await ctx.send("Ты ёба-боба?\nЯ не могу так работать\n"
                                      f"Мне тебе {page_num + 1} {morph_numerals(page_num + 1)} рандомную хрень кидать?")

            async with RedditAIO() as rt:
                try:
                    if page_num != 0:
                        page = await rt.get_raw_page_by_num(subreddit, page_num, sort, RedditAIO.TimeFrames.ALL)
                    else:
                        page = await rt.get_raw_page(subreddit, sort, RedditAIO.TimeFrames.ALL)
                except SubredditNotFound:
                    return await ctx.send("Такого сабреддита просто нет")
            if sort == RedditAIO.Listings.RANDOM:
                post_json = page[0]['data']['children'][0]['data']
            else:
                post_json = choice(page['data']['children'])['data']

            # Анти-Хорни
            if NSFWCheck.NSFW_CHECK:
                if post_json['over_18']:
                    if type(ctx.channel) is DMChannel:
                        if not NSFWCheck.ALLOW_NSFW_IN_DM:
                            return await ctx.send("https://i.vgy.me/Vuxpn2.png")
                    elif not NSFWCheck.ALLOW_NSFW_IN_NSFW or not (NSFWCheck.ALLOW_NSFW_IN_NSFW and ctx.channel.is_nsfw()):
                        return await ctx.send("https://i.vgy.me/Vuxpn2.png")

            if post_json.get("gallery_data", False):
                for item in post_json["gallery_data"]["items"]:
                    await ctx.reply(f"https://i.redd.it/{item['media_id']}.jpg")
                return
            self.cache_url(ctx, post_json['permalink'])

            await ctx.send(post_json['url'])

    @commands.command()
    async def reddit(self, ctx, subreddit: str = None, sort: str = None, page_num: int = None):
        return await self._reddit(ctx, subreddit, sort, page_num)


def setup(bot):
    bot.add_cog(Reddit(bot))
