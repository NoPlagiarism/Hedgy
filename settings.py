import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # settings.py should be in one folder with main.py
DATA_DIR = os.path.join(ROOT_DIR, 'data')
COGS_DIR = os.path.join(ROOT_DIR, "Cogs")  # should be in root folder
COGS_MODULE_NAME = "Cogs"

COMMAND_PREFIX = "!!"
DISCORD_BOT_TOKEN = "<ВСТАВЬТЕ ДИСКОРД ТОКЕН БОТА>"
EXCLUDED_COGS = ("__init__.py", )
# EXCLUDED_COMMANDS = ()


class Logs:
    FORMAT = "<green>{time:DD-MM-YYYY HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    # Вывод в консоль
    STDERR_OUTPUT = True
    STDERR_COLOR = True
    STDERR_LEVEL = "TRACE"

    # Вывод в файл
    FILE_OUTPUT = True
    FILE_NAME = r"logs\Lodgy.log"
    FILE_PATH = os.path.join(ROOT_DIR, FILE_NAME)
    FILE_LEVEL = "TRACE"
    FILE_ENCODING = "utf-8"
    FILE_ROTATION = "1 day"
    FILE_RETENTION = "1 week"

    # Отслеживать все комманды
    TRACE_COMMANDS = True


class Help:
    EXCLUDED_COMMANDS = ("error", "ping")
    FIELD_SEPARATOR = "%ANOTHER_FIELD%"
    FIELD_NAME = ""


class Exists:
    ART = 'OneImageGenerator(name="This Artwork Does Not Exist", url="https://thisartworkdoesnotexist.com/")'
    CAT = 'OneImageGenerator(name="This Cat Does Not Exist", url="https://thiscatdoesnotexist.com/")'
    HORSE = 'OneImageGenerator(name="This Horse Does Not Exist", url="https://thishorsedoesnotexist.com/")'
    PERSON = 'OneImageGenerator(name="This Person Does Not Exist", url="https://thispersondoesnotexist.com", img_url="https://thispersondoesnotexist.com/image")'

    """class SeedGenerator: NAME, URL, SET_SIZE, MIN_SEED, SEED_LEN, SOURCE_URL"""

    class Fursona:
        NAME = "This Fursona Does Not Exists"
        URL = "https://thisfursonadoesnotexist.com/"

        SET_SIZE: int = 99999
        MIN_SEED: int = 0
        SEED_LEN: int = 5
        SOURCE_URL: str = "https://thisfursonadoesnotexist.com/v2/jpgs-2x/seed{0:0" + str(SEED_LEN) + "n}.jpg"

    class Pony:
        NAME = "This Pony Does Not Exists"
        URL = "https://thisponydoesnotexist.net/"

        SET_SIZE: int = 75000
        MIN_SEED: int = 0
        SEED_LEN: int = 5
        SOURCE_URL: str = "https://thisponydoesnotexist.net/v1/w2x-redo/jpgs/seed{0:0" + str(SEED_LEN) + "n}.jpg"

    class NightSky:
        NAME = "This Night Sky Does Not Exist"
        URL = "https://arthurfindelair.com/thisnightskydoesnotexist/"

        SET_SIZE: int = 5000
        MIN_SEED: int = 1
        SEED_LEN: int = 4
        SOURCE_URL: str = "https://firebasestorage.googleapis.com/v0/b/thisnightskydoesnotexist.appspot.com/o/images%2Fseed{0:0" + str(SEED_LEN) + "n}.jpg?alt=media"

    class Map:
        NAME = "This Map Does Not Exists"
        URL = "http://thismapdoesnotexist.com"

        SET_SIZE: int = 9999
        MIN_SEED: int = 0
        SEED_LEN: int = 4
        SOURCE_URL: str = "https://raw.githubusercontent.com/iboates/thismapdoesnotexist-images/master/img/seed{0:0" + str(SEED_LEN) + "n}.png"

    class Waifu:
        NAME = "This Waifu Does Not Exists"
        URL = "https://thiswaifudoesnotexist.net/"

        SET_SIZE: int = 99999
        MIN_SEED: int = 0
        SEED_LEN: int = None
        SOURCE_URL: str = "https://www.thiswaifudoesnotexist.net/example-{}.jpg"

    class Beach:
        NAME = "This Beach Does Not Exists"
        URL = "https://thisbeachdoesnotexist.com"

        SET_SIZE: int = 9999
        MIN_SEED: int = 1
        SEED_LEN: int = 4
        SOURCE_URL = "https://thisbeachdoesnotexist.com/data/seeds-075/{}.jpg"

    IMG_NAME = "not_a_hedgehog.png"  # OneImageGenerator and e.t.c


class Youtube:
    VALIDATE_API_KEY = True
    # API ключ от Youtube Data Api https://rapidapi.com/blog/how-to-get-youtube-api-key/
    API_KEY = "<API ключ от Youtube Data Api>"
    DEFAULT_PLAYLIST_RYTP = "PLVUKS5caoZkYb1N8RDyy9HLMRKZHqvuGE"  # Hedgehog playlist by Anitavia

    ENABLED_PLAYLISTS = ("PLVUKS5caoZkYb1N8RDyy9HLMRKZHqvuGE", )
    ENABLE_ALL = True


class Reddit:
    DEF_LISTING = "random"
    DEF_TIMEFRAME = "all"
    DEF_LIMIT = 50

    ENABLED_SUBREDDITS = ["HedgehogMemes", "Hedgehog"]
    ENABLE_ALL_SUBREDDITS = True
    # Всё об NSFW
    NSFW_CHECK = True
    ALLOW_NSFW_IN_NSFW = True
    ALLOW_NSFW_IN_DM = True

    DEF_SUBREDDIT = "HedgehogMemes"

    COMMANDS = {"hedge": "Hedgehog",
                "hedgememe": "HedgehogMemes"}

    # Кэш последнего рандомного реддита
    LAST_REDDIT_URL = True


class Basic:
    FAIL_NOT_FOUND_FREQ = 4
    FAIL_ARGUMENT_FREQ = 5
    FAIL_ARGUMENT_SEND_FIRST = True
    if FAIL_ARGUMENT_SEND_FIRST:
        FAIL_ARGUMENT_START = FAIL_ARGUMENT_FREQ - 1
    else:
        FAIL_ARGUMENT_START = 0


class Va11Halla:
    VALIDATE_PATHS = True
    # Тупо все пути
    PATHS = {"en": (os.path.join(ROOT_DIR, "data\\va11halla\\en\\dialogue_scripts.json"),
                    os.path.join(ROOT_DIR, "data\\va11halla\\en\\dialogue_grouped.json"),
                    os.path.join(ROOT_DIR, "data\\va11halla\\en\\names.json")),
             "ru": (os.path.join(ROOT_DIR, "data\\va11halla\\ru\\dialogue_scripts.json"),
                    os.path.join(ROOT_DIR, "data\\va11halla\\ru\\dialogue_grouped.json"),
                    os.path.join(ROOT_DIR, "data\\va11halla\\ru\\names.json"))}
    CONFIG = os.path.join(ROOT_DIR, "data\\va11halla\\config.json")
    # Стандартный язык. Выберите en или ru
    DEF_LANG = "ru"
    EMBED_COLOR = 0xfd1a63
    CHARACTERS_PER_PAGE = 10
    SCRIPTS_PER_PAGE = 15
    ENABLE_ALL = True  # init all on start (НЕ СНИМАТЬ! это уже полная константа)

    USE_REACTIONS = True
    REACTIONS = ("⏪", "⏺", "⏩")
    REACTIONS_TIMEOUT = 60

    DISABLE_DOGS_LIST = True
    CHARACTERS_PER_PAGE_FILTERED = 9
    CAMEO_DOGS = ["Lord Pumplerump", "Arial Wienerton", "Lady Banner", "Dragon Fucker", "Satan's Hellper",
                  "Pesky Furball", "Wyrm Frigger", "Bangkok Bastard", "Tortilla Pope", "Cou Rage", "Dog 5",
                  "Mister Puff", "Third Barkday", "Poop-eater", "Money Shredder", "Gruff Bucket", "Wyvern Lover"]
