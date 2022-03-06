from discord.ext import commands
from .meta import Exists as Settings
from .generators import OneImageGenerator, SeedGenerator, CityGenerator, EyeGenerator


class Exists(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def one_image_generator(self, ctx, generator_eval):
        generator = eval(generator_eval)
        return await ctx.send(embed=await generator.get_embed(), file=await generator.get_image())

    @commands.command(aliases=("thiscatdoesnotexist", ))
    async def cat(self, ctx):
        return await self.one_image_generator(ctx, Settings.CAT)

    @commands.command(aliases=("thishorsedoesnotexist", ))
    async def horse(self, ctx):
        return await self.one_image_generator(ctx, Settings.HORSE)

    @commands.command(aliases=("artwork", "thisartworkdoesnotexist"))
    async def art(self, ctx):
        return await self.one_image_generator(ctx, Settings.ART)

    @commands.command(aliases=("human", "thispersondoesnotexist"))
    async def person(self, ctx):
        return await self.one_image_generator(ctx, Settings.PERSON)

    async def seed_generator(self, ctx, seed, meta):
        if seed is not None:
            if not (meta.MIN_SEED <= seed <= meta.SET_SIZE):
                return await ctx.reply("Отправьте число от {} до {}".format(meta.MIN_SEED, meta.SET_SIZE))
        generator = SeedGenerator(meta)
        return await ctx.send(embed=generator.get_embed(seed))

    @commands.command(aliases=("furry", "thisfursonadoesnotexist"))
    async def fursona(self, ctx,  seed: int = None):
        return await self.seed_generator(ctx, seed, Settings.Fursona)

    @commands.command(aliases=("thisponydoesnotexist", ))
    async def pony(self, ctx,  seed: int = None):
        return await self.seed_generator(ctx, seed, Settings.Pony)

    @commands.command(aliases=("sky", "night", "nightsky"))
    async def night_sky(self, ctx, seed: int = None):
        return await self.seed_generator(ctx, seed, Settings.NightSky)

    @commands.command(aliases=("thismapdoesnotexist", ))
    async def map(self, ctx, seed: int = None):
        return await self.seed_generator(ctx, seed, Settings.Map)

    @commands.command(aliases=("satellite", "thiscitydoesnotexist"))
    async def city(self, ctx):
        return await ctx.send(embed=await CityGenerator().get_embed())

    @commands.command(aliases=("wife", "thiswaifudoesnotexist"))
    async def waifu(self, ctx, seed: int = None):
        return await self.seed_generator(ctx, seed, Settings.Waifu)

    @commands.command(aliases=("thisbeachdoesnotexist", ))
    async def beach(self, ctx, seed: int = None):
        return await self.seed_generator(ctx, seed, Settings.Beach)

    @commands.command(aliases=("thissneakerdoesnotexist", ))
    async def sneaker(self, ctx, seed: int = None):
        return await self.seed_generator(ctx, seed, Settings.Sneaker)

    @commands.command(aliases=("thiseyedoesnotexist", ))
    async def eye(self, ctx):
        return await ctx.send(embed=await EyeGenerator().get_embed())
