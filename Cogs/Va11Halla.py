import json
from math import ceil
import discord
from settings import Va11Halla as Va11Halla_settings
from Utils import Va11HallaJSON, CharacterNotFound, progress_bar, CommandArgumentError, ScriptLineDoesNotExists
from discord.ext import commands
from time import time
import random
from loguru import logger
from os.path import exists
from asyncio import TimeoutError
from core.utils.predicates import ReactionsPredicate

random.seed(int(time()))


class DialEmbed(discord.Embed):
    def __init__(self, dial=None, character_uri=None):
        super(DialEmbed, self).__init__(colour=Va11Halla_settings.EMBED_COLOR)
        if dial is not None and character_uri is not None:
            self.update_embed(dial, character_uri)
        else:
            self.dial = dial
            self.character_uri = character_uri

    def update_embed(self, dial=None, character_uri=None, _clear=True):
        if _clear:
            self.clear_fields()
        if dial is not None and character_uri is not None:
            self.dial, self.character_uri = dial, character_uri
        self.add_field(name=self.dial.character, value=str(self.dial), inline=False)
        progress_bar_str, percent = progress_bar(dial.line, dial.script.lines)
        self.set_footer(text=f"{repr(dial.script)} {progress_bar_str} {dial.line}/{dial.script.lines}")
        self.set_thumbnail(url=character_uri)


class Va11Halla(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lang = Va11Halla_settings.DEF_LANG
        self._data = dict()
        with open(Va11Halla_settings.CONFIG, mode="r") as f:
            self.config = json.load(f)
        for lang, paths in Va11Halla_settings.PATHS.items():
            self._data[lang] = Va11HallaJSON(paths)
        if Va11Halla_settings.ENABLE_ALL:
            logger.debug("VA11HALLA - ALL ENABLED")
            tuple(map(Va11HallaJSON.init_all, tuple(self._data.values())))
        if Va11Halla_settings.DISABLE_DOGS_LIST:
            self.CHARACTERS_PER_PAGE = Va11Halla_settings.CHARACTERS_PER_PAGE_FILTERED
        else:
            self.CHARACTERS_PER_PAGE = Va11Halla_settings.CHARACTERS_PER_PAGE

    @property
    def data(self) -> Va11HallaJSON:
        return self._data[self.lang]

    def _list_characters(self, page=None):
        pages = ceil(len(self.data.characters) / self.CHARACTERS_PER_PAGE)
        if page is None:
            page = 0
        elif not (0 <= page <= pages-1):
            page = 0
        characters_slice = self.data.characters[self.CHARACTERS_PER_PAGE * page:self.CHARACTERS_PER_PAGE * (page+1)]
        icon = random.choice(tuple(self.config['char_icons'].values()))
        return characters_slice, icon, pages

    def _list_scripts(self, page=None):
        scripts = self.data.scripts
        pages = ceil(len(scripts) / Va11Halla_settings.SCRIPTS_PER_PAGE)
        if page is None:
            page = 0
        elif not (0 <= page <= pages-1):
            page = 0
        scripts_slice = scripts[Va11Halla_settings.SCRIPTS_PER_PAGE * page:Va11Halla_settings.SCRIPTS_PER_PAGE * (page+1)]
        icon = random.choice(tuple(self.config['char_icons'].values()))
        return scripts_slice, icon, pages

    def _list_langs(self, *args):
        icon = random.choice(tuple(self.config['char_icons'].values()))
        return tuple(self._data.keys()), icon, 1

    async def va11_list(self, ctx, args):
        if not (1 <= len(args) <= 2):
            raise CommandArgumentError("va11halla")
        page = 0
        if len(args) == 2:
            try:
                page = int(args[1]) - 1
            except ValueError:
                raise CommandArgumentError("va11halla")
        list_type = args[0]
        try:
            func = {"characters": self._list_characters,
                    "scripts": self._list_scripts,
                    "langs": self._list_langs}[list_type]
        except KeyError:
            raise CommandArgumentError("va11halla")
        if list_type == "langs":
            list_type = "languages"
        listing, icon, total_pages = func(page)
        if page > total_pages or 0 > page:
            page = 0
        embed = discord.Embed(colour=Va11Halla_settings.EMBED_COLOR, title="list of " + list_type)
        embed.add_field(name=f"Page {page+1}", value='\n'.join(listing), inline=False)
        embed.set_footer(text=f"{page+1}/{total_pages}", icon_url=icon)
        return await ctx.send(embed=embed)

    @commands.command(aliases=("va11", "valhalla"))
    async def va11halla(self, ctx, *args):
        """Комманда для случайного диалога из VA-11 HALL-A
        доступно -
        va11 list [characters/langs/scripts] [страница] - перечислить персонажей/языки/файлы (дни)
        va11 set [lang] - поменять язык без случайного диалога
        va11 [script/character] - случайный диалог из определённого дня/определённого персонажа
        va11 [script] [line] - определённая линия из скрипта
        va11 [script] [character] - случайный диалог персонажа из определённого скрипта"""
        if len(args) >= 2:
            if args[0] == "list":
                return await self.va11_list(ctx, args[1:])
            if args[0] == "set":
                if args[1] not in self._data.keys():
                    raise CommandArgumentError("va11halla")
                self.lang = args[1]
                await ctx.send("Язык диалогов изменён")
                return
        elif len(args) == 1:
            if args[0] == "list":
                return await ctx.send("Используйте как второй параметр: scripts, characters, langs")

        async with ctx.channel.typing():
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
            if character and line:
                await ctx.send("Пожалуйста, не ищите линию и персонажа одновременно")
                raise CommandArgumentError("va11halla")
            elif line and not script:
                await ctx.send("Пожалуйста, введите скрипт для начала")
                raise CommandArgumentError("va11halla")
            if script and line:
                try:
                    dial = self.data.get_script_line(line_num=line, script_name=script)
                except ScriptLineDoesNotExists as e:
                    return await ctx.send("Выберите линию входящую в диапозон от 2 до " + str(e.script['lines']))
            elif script and character:
                try:
                    dial = self.data.random_from_scripts(script, character)
                except CharacterNotFound as e:
                    await ctx.reply(str(e))
            elif script:
                dial = self.data.random_from_scripts(script)
            elif character:
                dial = self.data.random_from_characters(character)
            else:
                dial = self.data.random_from_scripts()

            embed = DialEmbed(dial, self.config["char_icons"][self.data.names[dial.character]])

        message = await ctx.send(embed=embed)
        return await self.handle_reactions(message, embed, ctx)

    if Va11Halla_settings.USE_REACTIONS:
        async def handle_reactions(self, message, embed, ctx):
            await message.add_reaction(Va11Halla_settings.REACTIONS[0]) if embed.dial.line > 0 else None
            await message.add_reaction(Va11Halla_settings.REACTIONS[1])
            await message.add_reaction(Va11Halla_settings.REACTIONS[2]) if embed.dial.line <= embed.dial.script.lines else None

            while True:
                try:
                    checker = ReactionsPredicate.emojis(Va11Halla_settings.REACTIONS, message=message, user=ctx.author)
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=Va11Halla_settings.REACTIONS_TIMEOUT,
                                                             check=checker)

                    if str(reaction.emoji) == Va11Halla_settings.REACTIONS[0]:
                        dial = self.data.get_script_line(embed.dial.line-1, meta=embed.dial.script)
                        if dial.line == 1:
                            await message.remove_reaction(Va11Halla_settings.REACTIONS[0])
                        elif dial.line == dial.script.lines-1:
                            await message.add_reaction(Va11Halla_settings.REACTIONS[2])
                    elif str(reaction.emoji) == Va11Halla_settings.REACTIONS[1]:
                        dial = self.data.random_from_scripts()
                    elif str(reaction.emoji) == Va11Halla_settings.REACTIONS[2]:
                        dial = self.data.get_script_line(embed.dial.line+1, meta=embed.dial.script)
                        if dial.line == 2:
                            await message.add_reaction(Va11Halla_settings.REACTIONS[0])
                        elif dial.line == dial.script.lines:
                            await message.remove_reaction(Va11Halla_settings.REACTIONS[2])
                    else:
                        continue
                    embed.update_embed(dial, self.config["char_icons"][self.data.names[dial.character]])
                    await message.remove_reaction(reaction, user)
                    await message.edit(embed=embed)
                except TimeoutError:
                    for reaction in Va11Halla_settings.REACTIONS:
                        try:
                            await message.clear_reaction(reaction)
                        except discord.NotFound:
                            pass
    else:
        async def handle_reactions(self, message, embed, ctx):
            pass

if Va11Halla_settings.VALIDATE_PATHS:
    def check():
        paths = list()
        for lang in Va11Halla_settings.PATHS.values():
            for path in lang:
                paths.append(path)
        paths_exists = tuple(map(exists, paths))
        if not all(paths_exists):
            paths_not_exists = tuple(paths[i] for i in range(len(paths)) if not paths_exists[i])
            logger.error("DISABLING VA11HALLA MODULE. {} not exist".format(', '.join(paths_not_exists)))
            return False
        return True
else:
    def check():
        return True


def setup(bot):
    if check():
        bot.add_cog(Va11Halla(bot))
