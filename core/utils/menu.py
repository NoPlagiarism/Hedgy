import discord
from discord.ext import commands
from typing import Union, Optional, Sequence, Dict, Iterable, Coroutine
import asyncio
from .predicates import ReactionsPredicate


def start_adding_reactions(message: discord.Message,
                           emojis: Iterable[Union[str, discord.Emoji, discord.PartialEmoji]]):
    async def task():
        try:
            for emoji in emojis:
                await message.add_reaction(emoji)
        except discord.NotFound:
            return

    return asyncio.create_task(task())


async def handle_reactions(
        bot: commands.Bot,
        message: discord.Message,
        emojis: Optional[Sequence[Union[str, discord.Emoji, discord.PartialEmoji]]] = None,
        callback: Optional[Coroutine] = None,
        controls: Optional[Union[Iterable, Dict[Union[str, discord.Emoji, discord.PartialEmoji], Coroutine]]] = None,
        timeout: int = 60,
        user: Optional[discord.User] = None,
        loops: int = -1
):
    if controls is None and not (emojis is None or callback is None):
        controls = dict()
        for i, emoji in enumerate(emojis):
            def _callback(*args, **kwargs):
                async def func(*args, **kwargs):
                    return await callback(*args, index=i, **kwargs)
                return func
            controls[emoji] = _callback()
    elif not isinstance(controls, dict) and emojis is not None and controls is not None:
        controls = dict(zip(emojis, controls))
    else:
        raise ValueError("Give emojis and callback else give dict controls")
    start_adding_reactions(message, controls.keys())
    while True:
        if loops == 0:
            break
        try:
            reaction, user = await bot.wait_for(
                "reaction_add",
                check=ReactionsPredicate.emojis(tuple(controls.keys()), message, user),
                timeout=timeout
            )
            await controls[reaction.emoji]()
        except asyncio.TimeoutError:
            loops = 0
        except discord.NotFound:
            return
    try:
        if message.channel.permissions_for(message._state.user).manage_messages:
            await message.clear_reactions()
        else:
            raise RuntimeError
    except (discord.Forbidden, RuntimeError):
        for emoji in controls.keys():
            try:
                await message.remove_reaction(emoji, bot.user)
            except discord.Forbidden:
                return
            except discord.HTTPException:
                return
