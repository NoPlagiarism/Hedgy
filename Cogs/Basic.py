from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound, DisabledCommand
from settings import Basic as Settings, Logs
from collections import defaultdict
from Utils import morph_numerals, CommandArgumentError
import time
from loguru import logger


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.not_found_count = defaultdict(int)
        self.bad_argument_count = defaultdict(lambda: defaultdict(lambda: Settings.FAIL_ARGUMENT_START))

    @commands.Cog.listener()
    async def on_ready(self, *args):
        logger.info("READY")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        if type(ex) is CommandNotFound:
            self.not_found_count[ctx.author.id] += 1
            if not self.not_found_count[ctx.author.id] % Settings.FAIL_NOT_FOUND_FREQ:
                return await ctx.reply(
                    "Ты ежанулся уже {} {}. Начни использовать {}help".format(self.not_found_count[ctx.author.id],
                                                                               morph_numerals(
                                                                                   self.not_found_count[ctx.author.id]),
                                                                               ctx.prefix))
            return
        elif type(ex) is DisabledCommand:
            return await ctx.reply("Данная комманда была выключенна")
        elif type(ex.__dict__.get("original", None)) is CommandArgumentError:
            ex = ex.original
            self.bad_argument_count[ctx.author.id][ex.command] += 1
            if not self.bad_argument_count[ctx.author.id][ex.command] % Settings.FAIL_ARGUMENT_FREQ:
                return await ctx.reply(f"Был введён неправильный аргумент. Проверьте {ctx.prefix}help {ex.command}")
        logger.exception(ex)
        logger.exception(f"Message: {ctx.message.content}")
        # breakpoint()

    @commands.command()
    async def error(self, ctx):
        logger.debug(f"{ctx.author.display_name} ({ctx.author.id}) raised an error")
        raise CommandArgumentError("error")

    if Logs.TRACE_COMMANDS:
        @commands.Cog.listener()
        async def on_command(self, ctx):
            logger.trace(f"{ctx.author.display_name} ({ctx.author.id}) invoked command with {ctx.message.content} ({ctx.message.id})")

        @commands.Cog.listener()
        async def on_application_command(self, ctx):
            logger.trace(
                f"{ctx.author.display_name} ({ctx.author.id}) invoked {ctx.command}")

    @commands.command(name="ping")
    async def ping(self, ctx):
        start_time = time.time()
        message = await ctx.send("Пингуем...")
        end_time = time.time()
        await message.edit(content=f"Дзынь! {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms")


def setup(bot):
    bot.add_cog(Basic(bot))
