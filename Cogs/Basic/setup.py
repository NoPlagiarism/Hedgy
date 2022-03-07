from .ext import Basic


def setup(bot):
    bot.add_cog(Basic(bot))