import json
from discord.ext.commands.errors import CommandError
from discord.commands import SlashCommand
from math import ceil


def morph_numerals(num: int):
    """Возвращает правильную строку 'раз' в зависимости от последней цифры числа"""
    last_digit = str(num)[-1]
    if last_digit in "234":
        return "раза"
    return "раз"


def progress_bar(value, max_value, size=10):
    """Просто прогресс бар"""
    progress_string = '▇'
    empty_string = '—'

    progress = round((value / max_value) * size)
    empty = size - progress

    bar = "[" + progress_string * progress + empty_string * empty + "]"
    return bar, progress


class CommandArgumentError(CommandError):
    def __init__(self, command):
        self.command = command


def format_json_file(filename, encoding="utf-8", **kwargs):
    with open(filename, encoding=encoding) as f:
        dicty = json.load(f)
    with open(filename, encoding=encoding, mode="w+") as f:
        json.dump(dicty, f, **kwargs)


def get_aliases(commands=None, bot=None):
    """Получить все сокращения к коммандам"""
    if commands is bot is None:
        return None
    elif bot and not commands:
        commands = bot.all_commands
    command_functions = dict()
    for command in commands.values():
        if isinstance(command, SlashCommand):
            continue
        command_functions[command.name] = command.aliases
    return command_functions


def matrix_transposion(data):
    return list(zip(*data))


def format_string(s, bounds=("<", ">"), **kwargs):
    for k, v in kwargs.items():
        s = s.replace(k.join(bounds), str(v))
    return s


def get_tabled_list(data, cols, _line_separator=" | ", _left_border="", _right_border="", _up_border=None,
                    _down_border=None, _rows_data=None):
    """Получить список с определённым количеством столбцов"""
    _format = _line_separator.join(tuple("{" + str(i) + ":<<col" + str(i) + ">}" for i in range(cols or len(_rows_data))))
    if _rows_data is not None:
        rows_data = list(_rows_data)
        while len(set(map(len, rows_data))) > 1:
            rows_data[min(cols, key=lambda x: len(rows_data[x]))].append("")
        if len(rows_data[-1]) != cols:
            rows_data[-1] = rows_data[-1] + (("", ) * (cols - len(rows_data[-1])))
        data_cols = matrix_transposion(rows_data)
        kwargs = dict()
        for i in range(len(data_cols)):
            kwargs["col" + str(i)] = len(max(data_cols[i], key=len))
        _format = format_string(_format, **kwargs)
        table_content = "\n".join(tuple(_left_border + _format.format(*x) + _right_border for x in rows_data))
    elif len(data) == 0:
        return None
    elif len(data) <= cols:
        table_content = _left_border + _line_separator.join(data) + _right_border
    else:
        rows_data = list()
        for i in range(ceil(len(data) / cols)):
            rows_data.append(list(data[i*cols:(i+1)*cols]))
        if len(rows_data[-1]) != cols:
            rows_data[-1].extend([""] * (cols - len(rows_data[-1])))
        data_cols = matrix_transposion(rows_data)
        kwargs = dict()
        for i in range(len(data_cols)):
            kwargs["col" + str(i)] = len(max(data_cols[i], key=len))
        _format = format_string(_format, **kwargs)
        table_content = "\n".join(tuple(_left_border + _format.format(*x) + _right_border for x in rows_data))
    if _up_border is None:
        _up_border = ""
    else:
        _up_border += "\n"
    if _down_border is None:
        _down_border = ""
    return _up_border + table_content + _down_border
