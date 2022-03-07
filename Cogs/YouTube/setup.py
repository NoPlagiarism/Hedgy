from .ext import Youtube


def setup(bot):
    bot.add_cog(Youtube(bot))
