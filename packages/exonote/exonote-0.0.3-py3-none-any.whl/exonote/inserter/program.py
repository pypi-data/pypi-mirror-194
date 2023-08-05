import tkinter as tk
from exonote import dto
from exonote.inserter import util
from exonote import utils


class ProgramInserter:
    def __init__(self, viewer):
        self._viewer = viewer
        self._editor = viewer.editor

    def insert(self, index, data):
        if self._viewer.restriction:
            caption = data.get("caption", "").strip()
            top_gap = data.get("top_gap", "")
            bottom_gap = data.get("bottom_gap", "")
            if caption:
                index = util.insert_top_gap(self._editor, top_gap)
            text = "${{{}}}".format(data.get("command"))
            self._editor.insert(index, text, "warning")
            if caption:
                self._editor.tag_add("caption", index)
                caption = "" if caption == "..." else caption
                if caption:
                    caption = "  " + caption + "  "
                    self._set_caption(caption)
            if bottom_gap:
                util.insert_bottom_gap(self._editor, bottom_gap)
            return
        self._embed_program(index, data)

    def _embed_program(self, index, data):
        command = data.get("command", "")
        cache = utils.get_callable(command)
        if not cache:
            return
        callable_name, callable_object, arguments = cache
        if is_class(callable_name):
            program_syntax = "${{{}}}".format(command)
            self._embed_gui(index, callable_object, arguments, data,
                            program_syntax)
        else:
            self._embed_program_output(index, callable_object, arguments)

    def _embed_gui(self, index, callable_object, arguments, data, program_syntax):
        caption = data.get("caption", "").strip()
        top_gap = data.get("top_gap", "")
        bottom_gap = data.get("bottom_gap", "")
        container = tk.Frame(self._editor)
        context = dto.ProgramContext(self._viewer, arguments)
        component = callable_object(context)
        body = component.build(container)
        if not body:
            container.destroy()
            return
        body.pack(expand=1, fill=tk.BOTH)
        # manage caption
        if caption:
            index = util.insert_top_gap(self._editor, top_gap)
        # create window
        self._editor.insert(index, program_syntax, "hidden")
        self._editor.window_create(index, window=container)
        if caption:
            self._editor.tag_add("caption", index)
            caption = "" if caption == "..." else caption
            if caption:
                caption = "  " + caption + "  "
                self._set_caption(caption)
        if bottom_gap:
            util.insert_bottom_gap(self._editor, bottom_gap)

    def _embed_program_output(self, index, callable_object, arguments):
        context = dto.ProgramContext(self._viewer, arguments)
        computed_text = callable_object(context)
        self._viewer.render(computed_text, index=index)
        self._viewer.enable_edit_mode()

    def _set_caption(self, caption):
        #self._viewer.enable_edit_mode()
        self._editor.insert(tk.INSERT, "\n")
        index = self._editor.index(tk.INSERT)
        self._viewer.render(caption, index=index)
        self._viewer.enable_edit_mode()
        #self._editor.mark_set(tk.INSERT, index)
        self._editor.tag_add("center_alignment", index)


def is_class(callable_name):
    if callable_name[0].isupper():
        return True
    return False
