from discord.ext.commands import Cog, slash_command
from discord.ext.commands.errors import MaxConcurrencyReached


class Va11HallaSlash(Cog):
    async def cog_command_error(self, ctx, error):
        if isinstance(error.__dict__.get("original"), MaxConcurrencyReached):
            pass
        else:
            ctx.bot.dispatch("command_error", ctx, error)
