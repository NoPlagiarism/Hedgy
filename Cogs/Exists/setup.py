from .ext import Exists
from .slash import ExistsSlash


def setup(bot):
    bot.add_cog(Exists(bot))
    bot.add_cog(ExistsSlash(bot))
