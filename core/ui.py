from discord.ui import Button as _Button


__all__ = [
    "Button"
]


class Button(_Button):
    def __init__(self, *args, callback=None, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        if callback is not None:
            self.callback = callback
