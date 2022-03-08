from .ext import Va11Halla
from .common import Va11Halla as Common


def setup(bot):
    common = Common(bot)
    bot.add_cog(Va11Halla(common))
