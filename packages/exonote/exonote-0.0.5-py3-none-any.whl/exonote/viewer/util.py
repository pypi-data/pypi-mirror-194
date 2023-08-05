import os
import os.path
import pathlib
from tkinter.font import Font
from exonote.utils import IndexParser
from collections import OrderedDict



def scroll_up(editor, step):
    editor.yview_scroll(-1*step, "pixels")


def scroll_down(editor, step):
    editor.yview_scroll(step, "pixels")


def update_index(index, text):  # TODO: delete me ?
    """ index should respect the form "x.y" """
    lines = text.splitlines()
    if text.endswith("\n"):
        lines.append("")
    n_lines = len(lines)
    if not n_lines:
        return index
    a, b = index.split(".")
    if n_lines == 1:
        b = int(b) + len(lines[0])
    elif n_lines > 1:
        a = int(a) + n_lines -1
        b = len(lines[-1])
    index = "{}.{}".format(a, b)
    return index


def on_mouse_wheel(event, editor, step):
    # scroll down   (value: 1)   <-  event.num = 5   or  event.delta < 0
    # scroll up     (value: -1)  <-  event.num = 4   or  event.delta >= 0
    if event.num == 5 or event.delta < 0:
        scroll_down(editor, step)
    else:
        scroll_up(editor, step)


def order_sids(editor, sections):
    cache = list()
    for sid, data in sections.items():
        index = editor.index(data["mark"])
        line, _ = index.split(".")
        cache.append((int(line), sid))
    return sorted(cache, key=lambda x: x[0])


def abspath(path, dossier=os.getcwd()):
    """Returns absolute path. Here, path is a canonical exonote path, i.e. a slash separated path
    that doesn't start with a slash"""
    if os.path.isabs(path):
        return path
    # note that canonical paths starting with "./" are ok !
    parts = path.split("/")
    p = pathlib.Path(dossier, *parts).resolve()
    return str(p)


def get_pages(dossier):
    pages = OrderedDict()
    index_filename = os.path.join(dossier, "index")
    if not os.path.exists(index_filename):
        return pages
    index = IndexParser.parse(index_filename)
    if not index:
        return pages
    for item in index:
        pages[item.filename] = item
    return pages


def get_monospace_height(style):
    font = Font(family=style.font_family,
                size=style.font_size)
    return font.metrics("linespace")


class Scrollable:
    def __init__(self, editor, step):
        self._editor = editor
        self._step = step
        self._handler = None
        self._setup()

    def set(self, widget):
        self._apply(widget)

    def _setup(self):
        self._handler = (lambda e, self=self:
                         self._on_mouse_wheel(e))

    def _apply(self, widget):
        widget.bind("<MouseWheel>", self._handler, True)
        widget.bind("<Button-4>", self._handler, True)
        widget.bind("<Button-5>", self._handler, True)
        for child in widget.children.values():
            self._apply(child)

    def _on_mouse_wheel(self, event):
        on_mouse_wheel(event, self._editor, self._step)
