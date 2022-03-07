from discord.ext import commands
from discord import Embed
from Utils import get_aliases, get_tabled_list
from settings import Help as Settings


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="commands")
    async def _commands(self, ctx):
        all_commands = tuple(filter(lambda x: x not in Settings.EXCLUDED_COMMANDS, get_aliases(bot=self.bot).keys()))
        embed = Embed()
        embed.add_field(name="All Commands", value="```" + get_tabled_list(all_commands, 3) + "```", inline=True)
        return await ctx.send(embed=embed)

    @commands.command()
    async def aliases(self, ctx):
        aliases = {k: ", ".join(v) for k, v in get_aliases(bot=self.bot).items() if k not in Settings.EXCLUDED_COMMANDS and len(v) != 0}
        embed = Embed()
        embed.add_field(name="All aliases", value="```" + get_tabled_list(None, 2, _rows_data=aliases.items()) + "```")
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
