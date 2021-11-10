from typing import Optional, Union, Sequence
import discord


class ReactionsPredicate:
    def __init__(self, predicate):
        self._predicate = predicate
        self.result = None

    def __call__(self, reaction, user):
        return self._predicate(self, reaction, user)

    @classmethod
    def same_ctx(cls,
                 message: Optional[discord.Message] = None,
                 user: Optional[discord.abc.User] = None):
        """Anti self-bot + check if needed message + check if needed user"""
        me_id = message._state.self_id
        return cls(
            lambda self, reaction, h_user: h_user.id != me_id
            and (message is None or reaction.message.id == message.id)
            and (user is None or h_user.id == user.id)
        )

    @classmethod
    def emojis(cls,
               emojis: Sequence[Union[str, discord.Emoji, discord.PartialEmoji]],
               message: Optional[discord.Message] = None,
               user: Optional[discord.abc.User] = None):
        """Match if reaction in specified emojis"""
        same_ctx = cls.same_ctx(message, user)

        def predicate(self: ReactionsPredicate, reaction: discord.Reaction, h_user: discord.abc.User):
            if not same_ctx(reaction, h_user):
                return False
            try:
                self.result = emojis.index(reaction.emoji)
            except ValueError:
                return False
            else:
                return True

        return cls(predicate)
