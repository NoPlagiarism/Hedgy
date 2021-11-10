from discord.ext import commands
from Utils import YoutubeDataApi
from settings import Youtube as Settings
from urllib import request as req
from urllib.error import HTTPError
from loguru import logger


class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=("randomytplaylist", "randyt", "randomyt", "rytp"))
    async def randomyoutubeplaylist(self, ctx, url=None):
        if url is None:
            url = Settings.DEFAULT_PLAYLIST_RYTP
        if '/' in url:
            try:
                url = url.split('list=')[1]
            except:
                pass
        if not Settings.ENABLE_ALL:
            if url not in Settings.ENABLED_PLAYLISTS:
                return ctx.send("Данный плейлист не разрешён")
        async with YoutubeDataApi(Settings.API_KEY) as yt:
            playlist = await yt.get_playlist(id=url)
            if not playlist:
                return await ctx.send("Ошибка! Проверьте валидность ссылки")
            video = await yt.random_from_playlist(playlist)
            return await ctx.send("https://www.youtube.com/watch?v=" + video['contentDetails']['videoId'])


if Settings.VALIDATE_API_KEY:
    def check():
        try:
            req.urlopen(f"https://www.googleapis.com/youtube/v3/videos?key={Settings.API_KEY}&part=id&id=dQw4w9WgXcQ")
        except HTTPError as e:
            logger.error("YOUTUBE DISABLING! Something went wrong")
            return False
        return True
else:
    def check():
        return True


def setup(bot):
    if check():
        bot.add_cog(Youtube(bot))
