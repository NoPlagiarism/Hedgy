class Exists:
    ART = 'OneImageGenerator(name="This Artwork Does Not Exist", url="https://thisartworkdoesnotexist.com/")'
    CAT = 'OneImageGenerator(name="This Cat Does Not Exist", url="https://thiscatdoesnotexist.com/")'
    HORSE = 'OneImageGenerator(name="This Horse Does Not Exist", url="https://thishorsedoesnotexist.com/")'
    PERSON = 'OneImageGenerator(name="This Person Does Not Exist", url="https://thispersondoesnotexist.com", img_url="https://thispersondoesnotexist.com/image")'
    TITS = 'OneImageGenerator(name="these tits do not exist", url="https://thesetitsdonotexist.com/", img_url="https://thesetitsdonotexist.com/img.png", nsfw=True)'

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
        SOURCE_URL: str = "https://firebasestorage.googleapis.com/v0/b/thisnightskydoesnotexist.appspot.com/o/images%2Fseed{0:0" + str(
            SEED_LEN) + "n}.jpg?alt=media"

    class Map:
        NAME = "This Map Does Not Exists"
        URL = "http://thismapdoesnotexist.com"

        SET_SIZE: int = 9999
        MIN_SEED: int = 0
        SEED_LEN: int = 4
        SOURCE_URL: str = "https://raw.githubusercontent.com/iboates/thismapdoesnotexist-images/master/img/seed{0:0" + str(
            SEED_LEN) + "n}.png"

    class Waifu:
        NAME = "This Waifu Does Not Exists"
        URL = "https://thiswaifudoesnotexist.net/"

        SET_SIZE: int = 99999
        MIN_SEED: int = 0
        SEED_LEN: int = 5
        SOURCE_URL: str = "https://www.thiswaifudoesnotexist.net/example-{}.jpg"

    class Beach:
        NAME = "This Beach Does Not Exists"
        URL = "https://thisbeachdoesnotexist.com"

        SET_SIZE: int = 9999
        MIN_SEED: int = 1
        SEED_LEN: int = 4
        SOURCE_URL = "https://thisbeachdoesnotexist.com/data/seeds-075/{}.jpg"

    class Sneaker:
        NAME = "This Sneaker Does Not Exists"
        URL = "https://thissneakerdoesnotexist.com"

        SET_SIZE: int = 2000
        MIN_SEED: int = 0
        SEED_LEN: int = 1
        SOURCE_URL = "https://thissneakerdoesnotexist.com/wp-content/plugins/sneaker-plugin/imsout2/3-3-2-{}.jpg"

    IMG_NAME = "not_a_hedgehog.png"  # OneImageGenerator and e.t.c
