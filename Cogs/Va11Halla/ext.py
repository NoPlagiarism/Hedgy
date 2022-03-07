# from __future__ import absolute_import
import json
from math import ceil
import discord
from settings import Va11Halla as Va11Halla_settings
from Utils import Va11HallaJSON, CharacterNotFound, progress_bar, CommandArgumentError, ScriptLineDoesNotExists
from discord.ext.commands import command, Cog
from discord.ext.commands.errors import MaxConcurrencyReached
from discord.ui import View
from discord import ButtonStyle

# try:

from core.ui import Button
from core.utils.predicates import ReactionsPredicate
from core.utils.utils import lambda_awaited
# except ImportError:
#     import sys
#     import os
#
#     sys.path.append(os.path.dirname(os.path.realpath(__file__)))
#     from core.ui import Button
#     from core.utils.predicates import ReactionsPredicate
#     from core.utils.utils import lambda_awaited
from time import time
import random
from loguru import logger
from os.path import exists
from asyncio import TimeoutError

random.seed(int(time()))


# TODO: как-то хреново.. рефакторнуть весь код
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
        if str(self.dial) == "":
            self.dial.text = "..."
        self.add_field(name=self.dial.character, value=str(self.dial), inline=False)
        progress_bar_str, percent = progress_bar(dial.line, dial.script.lines)
        self.set_footer(text=f"{repr(dial.script)} {progress_bar_str} {dial.line}/{dial.script.lines}")
        self.set_thumbnail(url=character_uri)

    @property
    def line(self) -> int:
        return self.dial.line


class ViewCtx(dict):
    @property
    def embed(self) -> DialEmbed:
        return self[0]

    @embed.setter
    def embed(self, val):
        self[0] = val

    @property
    def ctx(self) -> discord.ext.commands.Context:
        return self[1]

    @ctx.setter
    def ctx(self, val):
        self[1] = val

    @property
    def message(self):
        return self[2]

    @message.setter
    def message(self, val):
        self[2] = val


class Va11HallaView(View):
    def __init__(self, callback, view_ctx=None):
        self._callback = callback
        self.view_ctx = view_ctx

        self.backward = Button(emoji="⏪", style=ButtonStyle.primary,
                               callback=lambda _: lambda_awaited(await self.callback(0) for _ in '_'))
        self.random = Button(emoji="⏺", style=ButtonStyle.success,
                             callback=lambda _: lambda_awaited(await self.callback(1) for _ in '_'))
        self.forward = Button(emoji="⏩", style=ButtonStyle.primary,
                              callback=lambda _: lambda_awaited(await self.callback(2) for _ in '_'))

        super(Va11HallaView, self).__init__(self.backward, self.random, self.forward,
                                            timeout=Va11Halla_settings.VIEW_TIMEOUT)

    @property
    def message(self):
        return self.view_ctx.message

    async def on_timeout(self) -> None:
        return await self.message.edit(view=None)

    async def callback(self, button_index):
        return await self._callback(self, button_index)

    async def switching_buttons(self, n_dial=None, max_line=None):
        if n_dial is None or max_line is None:
            n_dial = self.view_ctx.embed.dial.line
            max_line = self.view_ctx.embed.dial.script.lines
        not_changed = False
        if n_dial == max_line:
            self.forward.disabled = True
        elif n_dial == max_line - 1:
            self.forward.disabled = False
        elif n_dial == 1:
            self.backward.disabled = True
        elif n_dial == 2:
            self.backward.disabled = False
        else:
            not_changed = True
        return not_changed


class Va11Halla(Cog):
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

    async def cog_command_error(self, ctx, error):
        if isinstance(error.__dict__.get("original"), MaxConcurrencyReached):
            pass
        else:
            ctx.bot.dispatch("command_error", ctx, error)

    @property
    def data(self) -> Va11HallaJSON:
        return self._data[self.lang]

    def _list_characters(self, page=None):
        pages = ceil(len(self.data.characters) / self.CHARACTERS_PER_PAGE)
        if page is None:
            page = 0
        elif not (0 <= page <= pages - 1):
            page = 0
        characters_slice = self.data.characters[self.CHARACTERS_PER_PAGE * page:self.CHARACTERS_PER_PAGE * (page + 1)]
        icon = random.choice(tuple(self.config['char_icons'].values()))
        return characters_slice, icon, pages

    def _list_scripts(self, page=None):
        scripts = self.data.scripts
        pages = ceil(len(scripts) / Va11Halla_settings.SCRIPTS_PER_PAGE)
        if page is None:
            page = 0
        elif not (0 <= page <= pages - 1):
            page = 0
        scripts_slice = scripts[
                        Va11Halla_settings.SCRIPTS_PER_PAGE * page:Va11Halla_settings.SCRIPTS_PER_PAGE * (page + 1)]
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
        embed.add_field(name=f"Page {page + 1}", value='\n'.join(listing), inline=False)
        embed.set_footer(text=f"{page + 1}/{total_pages}", icon_url=icon)
        return await ctx.send(embed=embed)

    @command(aliases=("va11", "valhalla"))
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
                    return await ctx.send("Выберите линию входящую в диапозон от 2 до " + str(e.script.lines))
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

        if Va11Halla_settings.USE_VIEW:
            view_ctx = ViewCtx()
            view_ctx.embed = embed
            view_ctx.ctx = ctx
            view = Va11HallaView(await self._get_buttons_callback(), view_ctx)
            message = await ctx.send(embed=embed, view=view)
            view.view_ctx.message = message
        else:
            return await ctx.send(embed=embed)

    async def _get_buttons_callback(self):
        async def button_callback(view, index):
            if index == 0:
                dial = self.data.get_script_line(view.view_ctx.embed.line - 1, meta=view.view_ctx.embed.dial.script)
            elif index == 1:
                dial = self.data.random_from_scripts()
            elif index == 2:
                dial = self.data.get_script_line(view.view_ctx.embed.line + 1, meta=view.view_ctx.embed.dial.script)
            else:
                dial = view.view_ctx.embed.dial
            view.view_ctx.embed.update_embed(dial, self.config["char_icons"][self.data.names[dial.character]])
            await view.switching_buttons()
            await view.view_ctx.message.edit(embed=view.view_ctx.embed, view=view)

        return button_callback


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
