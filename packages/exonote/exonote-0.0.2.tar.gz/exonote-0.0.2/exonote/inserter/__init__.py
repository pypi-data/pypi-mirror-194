import tkinter as tk
from exonote.error import Error
from exonote.inserter import util
from exonote.inserter.codeblock import CodeblockInserter
from exonote.inserter.heading import HeadingInserter
from exonote.inserter.attachment import AttachmentInserter
from exonote.inserter.link import LinkInserter
from exonote.inserter.program import ProgramInserter
from exonote.inserter.table import TableInserter


class Inserter:
    def __init__(self, viewer):
        self._viewer = viewer
        self._cache = list()

    @property
    def viewer(self):
        return self._viewer

    @property
    def cache(self):
        return self._cache

    def insert(self, element, index, data):
        name = "insert_{}".format(element.name.lower())
        try:
            method = getattr(self, name)
        except AttributeError as e:
            raise Error("Insert method missing for '{}'.".format(element.name))
        try:
            method(index, data)
        except Exception as e:
            line_1 = "Failed to insert {} at index {} !".format(element, index)
            line_2 = "Data: {}".format(data)
            msg = "{}\n{}".format(line_1, line_2)
            raise Error(msg)

    def insert_anchor(self, index, data):
        self._viewer.register_anchor(data["text"], index)

    def insert_attachment(self, index, data):
        instance = AttachmentInserter(self._viewer)
        instance.insert(index, data)

    def insert_bold(self, index, data):
        editor, text = self._viewer.editor, data["text"]
        editor.insert(index, text, "bold")

    def insert_code(self, index, data):
        editor, text = self._viewer.editor, data["text"]
        editor.insert(index, text, "code")

    def insert_codeblock(self, index, data):
        instance = CodeblockInserter(self._viewer)
        instance.insert(index, data)

    def insert_dinkus(self, index, data):
        editor = self._viewer.editor
        top_gap = data.get("top_gap", "")
        bottom_gap = data.get("bottom_gap", "")
        index = util.insert_top_gap(editor, top_gap)
        editor.insert(index, " * * * ", ("center_alignment", "bold"))
        util.insert_bottom_gap(editor, bottom_gap)

    def insert_gap(self, index, data):
        self._viewer.editor.insert(index, "\n\n", "gap")

    def insert_heading(self, index, data):
        instance = HeadingInserter(self._viewer)
        instance.insert(index, data)

    def insert_italic(self, index, data):
        editor, text = self._viewer.editor, data["text"]
        editor.insert(index, text, "italic")

    def insert_item(self, index, data):
        editor, text = self._viewer.editor, data["text"]
        editor.insert(index, text, "bold")

    def insert_link(self, index, data):
        instance = LinkInserter(self._viewer)
        instance.insert(index, data)

    def insert_monospace(self, index, data):
        editor, text = self._viewer.editor, data["text"]
        editor.insert(index, text, "monospace")

    def insert_notice(self, index, data):
        editor, text = self._viewer.editor, data["text"]
        editor.insert(index, text, "notice")

    def insert_program(self, index, data):
        instance = ProgramInserter(self._viewer)
        instance.insert(index, data)

    def insert_strikethrough(self, index, data):
        editor, text = self._viewer.editor, data["text"]
        editor.insert(index, text, "strikethrough")

    def insert_string(self, index, data):
        editor, text = self._viewer.editor, data["text"]
        editor.insert(index, text)

    def insert_table(self, index, data):
        instance = TableInserter(self._viewer)
        instance.insert(index, data)

    def insert_underline(self, index, data):
        editor, text = self._viewer.editor, data["text"]
        editor.insert(index, text, "underline")

    def insert_warning(self, index, data):
        editor, text = self._viewer.editor, data["text"]
        editor.insert(index, text, "warning")
