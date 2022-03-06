import sys
import time
try:
    from .core.bot import Hedgy
except ImportError:
    from core.bot import Hedgy
from settings import Logs, os, COMMAND_PREFIX, COGS_DIR, EXCLUDED_COGS, COGS_MODULE_NAME, DISCORD_BOT_TOKEN
from Utils import get_aliases
from loguru import logger
from pprint import pformat
from discord import http

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

    http.API_VERSION = 9
    bot = Hedgy(command_prefix=COMMAND_PREFIX)

    for filename in os.listdir(COGS_DIR):
        if filename in EXCLUDED_COGS:
            continue
        path = os.path.join(COGS_DIR, filename)
        if os.path.isfile(path) and filename.endswith(".py"):
            bot.load_extension(f'{COGS_MODULE_NAME}.{filename[:-3]}')
        elif os.path.isdir(path) and filename[0] not in (".", "_"):
            bot.load_extension(f'{COGS_MODULE_NAME}.{filename}.setup')

    all_commands = get_aliases(bot=bot)
    logger.trace("ALL COMMANDS: \n" + pformat(all_commands))
    bot.run(DISCORD_BOT_TOKEN)


if __name__ == '__main__':
    main()
