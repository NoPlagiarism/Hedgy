import random
import json
from settings import Va11Halla as Va11Halla_settings
from loguru import logger


class Script:
    """Класс, описывающий скрипт
    lines - кол-во линий в дне
    name - название"""
    dict: dict

    def __init__(self, raw_dict):
        self.dict = raw_dict

    def __repr__(self):
        return "Script " + self.dict['filename']

    @property
    def lines(self) -> int:
        return self.dict['lines']

    @property
    def name(self) -> str:
        return self.dict["filename"]


class Dialogue:
    """Диалог.
    script - Script
    character - имя персонажа
    text - содержимое диалога
    line - линия в скрипте"""
    script: Script
    character: str
    text: str
    line: int

    def __init__(self, script, character, line, text):
        if type(script) is not Script:
            self.script = Script(script)
        else:
            self.script = script
        self.character, self.line, self.text = character, line, text

    def __repr__(self):
        return f'"{self.character}: {self.text}" on line: {self.line}'

    def __str__(self):
        return self.text

    @staticmethod
    def from_grouped_dial(raw_dict, character):
        return Dialogue(raw_dict['script'], character, raw_dict['line'], raw_dict['text'])

    @staticmethod
    def from_scripts_dial(raw_dict, script):
        return Dialogue(script, raw_dict['character'], raw_dict['line'], raw_dict['text'])


class CharacterNotFound(Exception):
    def __init__(self, name, script=None):
        self.name = name
        self.script = None if script is None else script

    def __repr__(self):
        if self.script:
            return f"Персонаж {self.name} в скрипте {self.script} не найден"
        return f"Персонаж {self.name} не найден"


class ScriptNotFound(Exception):
    def __init__(self, filename):
        self.filename = filename

    def __repr__(self):
        return f"Скрипт {self.filename} не найден"


class ScriptLineDoesNotExists(Exception):
    def __init__(self, script_info=None, error_line=None):
        self.script = script_info
        self.error_line = error_line

    def __repr__(self):
        return f"{self.script['filename']} имеет {self.script['lines']} линий"


class Va11HallaJSON:
    def __init__(self, paths=None):
        if paths is None:
            paths = Va11Halla_settings.PATHS['en']
        self.paths = paths
        # dialogue_scripts.json
        self._dialogue_scripts = None
        self._scripts = None
        # dialogue_grouped.json
        self._dialogue_grouped = None
        # names.json
        self.names = None
        self.init_names()
        self._names_filtered = None
        self.init_names_filtered()
        self.characters = None
        if Va11Halla_settings.DISABLE_DOGS_LIST:
            self.characters = tuple(self.names_filtered.keys())
        else:
            self.characters = tuple(self.names.keys())

    def init_names(self, path=None):
        if self.names is not None:
            return
        if path is None:
            path = self.paths[2]
        with open(path, mode="r", encoding="utf-8") as f:
            self.names = json.load(f)

    def init_names_filtered(self, exclude=None):
        if exclude is None:
            exclude = Va11Halla_settings.CAMEO_DOGS
        self._names_filtered = dict(filter(lambda x: x[1] not in exclude, self.names.items()))

    def init_scripts(self, path=None):
        if self._dialogue_scripts is not None:
            return
        if path is None:
            path = self.paths[0]
        with open(path, mode="r", encoding="utf-8") as f:
            self._dialogue_scripts = json.load(f)

    def init_grouped(self, path=None):
        if self._dialogue_grouped is not None:
            return
        if path is None:
            path = self.paths[1]
        with open(path, mode="r", encoding="utf-8") as f:
            self._dialogue_grouped = json.load(f)

    def init_scripts_list(self, dialogue_scripts=None):
        if dialogue_scripts is None:
            dialogue_scripts = self.dialogue_scripts
        self._scripts = tuple(map(lambda script: script[0]["filename"], dialogue_scripts))

    def init_all(self):
        self.init_grouped()
        self.init_scripts()
        self.init_scripts_list()

    @property
    def dialogue_scripts(self) -> list:
        if self._dialogue_scripts is None:
            self.init_scripts()
        return self._dialogue_scripts

    @property
    def dialogue_grouped(self) -> dict:
        if self._dialogue_grouped is None:
            self.init_grouped()
        return self._dialogue_grouped

    @property
    def scripts(self):
        if self._scripts is None:
            self.init_scripts_list()
        return self._scripts

    @property
    def names_filtered(self):
        if self._names_filtered is None:
            self.init_names_filtered()
        return self._names_filtered

    def clear_all(self):
        self._dialogue_scripts = None
        self._dialogue_grouped = None

    def get_script(self, script_name=None):
        try:
            return self.dialogue_scripts[self.scripts.index(script_name)]
        except ValueError:
            raise ScriptNotFound(script_name)

    def get_script_line(self, line_num: int, script=None, script_name: str = None, meta: Script = None):
        if script is script_name is None:
            script_name = meta.name
        if script is None:
            script = self.get_script(script_name)
        try:
            line = script[line_num-1]
            return Dialogue.from_scripts_dial(line, script[0])
        except IndexError:
            pass

    def random_from_scripts(self, script_name=None, character=None) -> Dialogue:
        if script_name is not None:
            script = self.get_script(script_name)
        else:
            script = random.choice(self.dialogue_scripts)
        script_info = script[0]
        if character is not None:
            character_lines = tuple(filter(lambda line: line["character"] == character, script[1:]))
            if not character_lines:
                raise CharacterNotFound(character, script_name)
            dialogue = random.choice(character_lines)
        else:
            dialogue = random.choice(script[1:])
        return Dialogue.from_scripts_dial(dialogue, script_info)

    def random_from_characters(self, character=None) -> Dialogue:
        if character is None:
            character = random.choice(tuple(self.dialogue_grouped.keys()))
        try:
            dialogues = self.dialogue_grouped[character]
        except KeyError:
            raise CharacterNotFound(character)
        dialogue = random.choice(dialogues)
        return Dialogue.from_grouped_dial(dialogue, character)
