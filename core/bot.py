from discord.ext.commands import Bot
from discord import DMChannel
from settings import NSFWCheck


class Hedgy(Bot):
    if NSFWCheck.NSFW_CHECK:
        @staticmethod
        def check_if_nsfw_enabled(ctx=None, channel=None):
            if channel is None and ctx is None:
                raise AttributeError("Ctx or channel needed for NSFW check")
            if channel is None:
                channel = ctx.channel
            if isinstance(channel, DMChannel) and NSFWCheck.ALLOW_NSFW_IN_DM:
                return True
            elif channel.nsfw and NSFWCheck.ALLOW_NSFW_IN_NSFW:
                return True
            return False
    else:
        @staticmethod
        def check_if_nsfw_enabled(*args, **kwargs):
            return True

    # def load_cog_package(self, pkg_name):
    #     return self.load_extension(pkg_name + ".setup")
