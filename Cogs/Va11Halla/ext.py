from discord.ext.commands import Cog
from discord.ext.commands.errors import MaxConcurrencyReached
from discord.ext.commands import command
from discord import Embed
from Utils import CommandArgumentError


class Va11Halla(Cog):
    def __init__(self, common):
        self.common = common
        self.bot = common.bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error.__dict__.get("original"), MaxConcurrencyReached):
            pass
        else:
            ctx.bot.dispatch("command_error", ctx, error)

    async def va11_list(self, ctx, args):
        if not (1 <= len(args) <= 2):
            raise CommandArgumentError("va11halla")
        page = 0
        if len(args) == 2:
            try:
                page = int(args[1]) - 1
            except ValueError:
                raise CommandArgumentError("va11halla")
        return await ctx.send(embed=self.common.va11_list(args[0], page))

    @command(aliases=("va11", "valhalla"))
    async def va11halla(self, ctx, *args):
        if len(args) >= 2:
            if args[0] == "list":
                return await self.va11_list(ctx, args[1:])
            if args[0] == "set":
                if args[1] not in self._data.keys():
                    raise CommandArgumentError("va11halla")
                self.common.lang = args[1]
                await ctx.send("Язык диалогов изменён")
                return
        elif len(args) == 1:
            if args[0] == "list":
                return await ctx.send("Используйте как второй параметр: scripts, characters, langs")

        character = None
        script = None
        line = None
        for arg in args:
            if arg in self._data.keys():
                if self.lang != arg:
                    self.lang = arg
                    await ctx.send("Язык диалогов изменён")
                continue
            elif arg in self.data.scripts:
                script = arg
                continue
            elif arg in self.data.dialogue_grouped.keys():
                character = arg
                continue
            try:
                line = int(arg)
            except ValueError:
                raise CommandArgumentError("va11halla")

        res = await self.common.va11halla(ctx, character, script, line)
        if isinstance(res, Embed):
            return await ctx.send(embed=res)
        elif isinstance(res, str):
            return await ctx.send(res)
        elif isinstance(res[0], Embed):
            msg = await ctx.send(embed=res[0], view=res[1])
            res[1].view_ctx.message = msg
            return
        else:
            await ctx.send(res[0])
            raise res[1]
