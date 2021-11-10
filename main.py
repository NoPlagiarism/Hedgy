import sys
import time
from discord.ext import commands
from settings import Logs, os, COMMAND_PREFIX, COGS_DIR, EXCLUDED_COGS, COGS_MODULE_NAME, DISCORD_BOT_TOKEN
from Utils import get_aliases
from loguru import logger
from pprint import pformat

logger.remove()

if Logs.STDERR_OUTPUT:
    logger.add(sys.stderr, level=Logs.STDERR_LEVEL, colorize=Logs.STDERR_COLOR)
if Logs.FILE_OUTPUT:
    logger.add(Logs.FILE_NAME, level=Logs.FILE_LEVEL, rotation=Logs.FILE_ROTATION, retention=Logs.FILE_RETENTION,
               encoding=Logs.FILE_ENCODING)


@logger.catch()
def main():
    time.time()
    logger.info(f"Program has been started")

    bot = commands.Bot(command_prefix=COMMAND_PREFIX)

    for filename in os.listdir(COGS_DIR):
        if filename.endswith(".py") and filename not in EXCLUDED_COGS:
            bot.load_extension(f'{COGS_MODULE_NAME}.{filename[:-3]}')
    all_commands = get_aliases(bot=bot)
    logger.trace("ALL COMMANDS: \n" + pformat(all_commands))
    bot.run(DISCORD_BOT_TOKEN)


if __name__ == '__main__':
    main()
