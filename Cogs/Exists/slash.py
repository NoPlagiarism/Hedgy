from discord.ext.commands import Cog, slash_command
from discord.commands import Option, ApplicationContext
from .meta import Exists as Settings
from .generators import OneImageGenerator, SeedGenerator, CityGenerator, EyeGenerator
from settings import NSFWCheck


class GeneratorTypes:
    ONE_IMAGE = 0
    SEED = 1
    CITY = 2
    EYE = 3


EXISTS_DICT = {
    "Sky": GeneratorTypes.SEED,
    "Fursona": GeneratorTypes.SEED,
    "Waifu": GeneratorTypes.SEED,
    "Pony": GeneratorTypes.SEED,
    "Beach": GeneratorTypes.SEED,
    "City": GeneratorTypes.CITY,
    "Map": GeneratorTypes.SEED,
    "Person": GeneratorTypes.ONE_IMAGE,
    "Cat": GeneratorTypes.ONE_IMAGE,
    "Art": GeneratorTypes.ONE_IMAGE,
    "Horse": GeneratorTypes.ONE_IMAGE,
    "Tits": GeneratorTypes.ONE_IMAGE,
    "Sneaker": GeneratorTypes.SEED,
    "Eye": GeneratorTypes.EYE
}
EXISTS_LIST = tuple(EXISTS_DICT.keys())
EXISTS_META = {
    "Sky": Settings.NightSky,
    "Fursona": Settings.Fursona,
    "Waifu": Settings.Waifu,
    "Pony": Settings.Pony,
    "Beach": Settings.Beach,
    "City": None,
    "Map": Settings.Map,
    "Person": Settings.PERSON,
    "Cat": Settings.CAT,
    "Art": Settings.ART,
    "Horse": Settings.HORSE,
    "Tits": Settings.TITS,
    "Sneaker": Settings.Sneaker,
    "Eye": None
}


class ExistsSlash(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def one_image_generator(self, ctx, generator_eval):
        generator = eval(generator_eval)
        if generator.nsfw:
            if not self.bot.check_if_nsfw_enabled(ctx=ctx):
                return await ctx.respond(NSFWCheck.DEFAULT_ANTI_HORNY_IMG_URL, ephemeral=True)
        return await ctx.respond(embed=await generator.get_embed(), file=await generator.get_image())

    async def seed_generator(self, ctx, meta, seed):
        if seed is not None:
            if not (meta.MIN_SEED <= seed <= meta.SET_SIZE):
                return await ctx.respond("Отправьте число от {} до {}".format(meta.MIN_SEED, meta.SET_SIZE),
                                         ephemeral=True)
        generator = SeedGenerator(meta)
        return await ctx.respond(embed=generator.get_embed(seed))

    @slash_command(name="exists", description="That Does Not Exists")
    async def doesnotexists(self,
                      ctx: ApplicationContext,
                      generator: Option(str, name="generator", description="Name of x", required=True, choices=EXISTS_LIST),
                      seed: Option(int, name="seed", description="Internal seed of ing in generator", required=False) = None):
        gen_type = EXISTS_DICT[generator]
        if gen_type == 0:
            return await self.one_image_generator(ctx, EXISTS_META[generator])
        elif gen_type == 1:
            return await self.seed_generator(ctx, EXISTS_META[generator], seed)
        elif gen_type == 2:
            return await ctx.respond(embed=await CityGenerator().get_embed())
        elif gen_type == 3:
            return await ctx.respond(embed=await EyeGenerator().get_embed())
