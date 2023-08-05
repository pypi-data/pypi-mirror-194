import importlib
import shlex
import os.path
from tkinter import font
from exonote import dto


def get_standard_font_family(name="TkDefaultFont"):
    return font.nametofont(name).actual()["family"]


def split_target(target):
    filename, sid = target, str()
    if "<" in target and target.endswith(">"):
        cache = target.rstrip(">").split("<")
        if len(cache) == 2:
            filename, sid = cache
            sid = "<{}>".format(sid)
    return filename, sid


def update_clipboard(text, widget):
    widget.clipboard_clear()
    widget.clipboard_append(text)


def get_callable(command):
    left, right = "", ""
    cache = command.split(maxsplit=1)
    n = len(cache)
    if n == 2:
        left, right = cache
    elif n == 1:
        left = cache[0]
    else:
        return None
    cache = left.split(":")
    n = len(cache)
    arguments = shlex.split(right, posix=True) if right else list()
    if n == 2:
        module_name, callable_name = cache
    elif n == 1:
        module_name, callable_name = cache[0], "main"
    else:
        return None
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as e:
        return None
    try:
        callable_object = getattr(module, callable_name)
    except AttributeError as e:
        return None
    return callable_name, callable_object, arguments
    
    
class IndexParser:

    @staticmethod
    def parse(filename):
        if not os.path.exists(filename):
            return
        data = list()
        cache = list()
        with open(filename, "r") as file:
            page = 0
            for line in file.readlines():
                line = line.strip()
                if line:
                    cache.append(line)
                    continue
                if not cache:
                    continue
                page += 1
                info = IndexParser._interpret(page, cache)
                data.append(info)
                cache = list()
        info = IndexParser._interpret(page+1, cache)
        if info:
            data.append(info)
        return data

    @staticmethod
    def _interpret(page, data):
        if not data:
            return
        filename = data[0]
        title, tags = "", list()
        for line in data[1:]:
            if line.startswith("#"):
                for item in line.split():
                    tag = item.strip("#")
                    tags.append(tag)
            else:
                title = line.strip()
        return dto.PageInfo(filename, page, title, tags)
