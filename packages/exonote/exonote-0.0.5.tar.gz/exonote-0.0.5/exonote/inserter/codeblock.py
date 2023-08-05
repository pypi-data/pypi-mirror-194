import tkinter as tk
from tkinter.font import Font
from exonote import utils
from exonote.inserter import util


class CodeblockInserter:
    def __init__(self, viewer):
        self._viewer = viewer
        self._editor = viewer.editor

    def insert(self, index, data):
        # expand data
        title, text = data["title"], data["text"]
        top_gap = data.get("top_gap", "")
        bottom_gap = data.get("bottom_gap", "")
        # tag
        tag = "codeblock_{}".format(self._viewer.next_id())
        # define tag
        self._editor.tag_configure(tag)
        # bind events handlers
        # - bind on hover link
        statusbar = self._viewer.statusbar
        status_info = {"text": title, "tag": "(block)"}
        # - bind on hover link
        self._bind_on_hover_codeblock(status_info, tag, statusbar)
        # - bind on click link
        self._bind_on_click_codeblock(text, tag)
        # insert
        index = util.insert_top_gap(self._editor, top_gap)
        self._editor.insert(index, text, ("codeblock", tag))
        util.insert_bottom_gap(self._editor, bottom_gap)

    # ===== CODEBLOCK - ON HOVER =====

    def _bind_on_hover_codeblock(self, status_info, tag, statusbar):
        # on pointer enters codeblock
        """
        handler = (lambda e, editor=editor, h=h, hover_info=hover_info:
                   _on_enter_codeblock(editor, h, hover_info))
        editor.tag_bind(tag, "<Enter>", handler, True)
        # on pointer leaves codeblock
        handler = (lambda e, editor=editor, h=h:
                   _on_leave_codeblock(editor, h))
        editor.tag_bind(tag, "<Leave>", handler, True)
        """
        # on pointer enters link
        handler = (lambda e:
                   self._on_enter_codeblock(statusbar, status_info))
        self._editor.tag_bind(tag, "<Enter>", handler, True)
        # on pointer leaves link
        handler = (lambda e:
                   self._on_leave_codeblock(statusbar))
        self._editor.tag_bind(tag, "<Leave>", handler, True)

    def _on_enter_codeblock(self, statusbar, status_info):
        """
        h.enter_event("hover", **hover_info)
        editor.config(cursor="hand1")
        """
        self._editor.config(cursor="hand1")
        text = status_info.get("text")
        tag = status_info.get("tag")
        statusbar.show(text, tag=tag)

    def _on_leave_codeblock(self, statusbar):
        self._editor.config(cursor="")
        statusbar.hide()

    # ===== CODEBLOCK - ON CLICK =====

    def _bind_on_click_codeblock(self, text, tag):
        # button-3 press
        handler = (lambda e, tag=tag:
                   self._on_button_3_press_codeblock(tag))
        self._editor.tag_bind(tag, "<ButtonPress-3>", handler, True)
        # button-3 release
        handler = (lambda e, text=text, tag=tag:
                   self._on_button_3_release_codeblock(text, tag))
        self._editor.tag_bind(tag, "<ButtonRelease-3>", handler, True)

    def _on_button_3_press_codeblock(self, tag):
        font = Font(font=self._editor.tag_cget("codeblock", "font"))
        actual = font.actual()
        actual["underline"] = True
        font = Font(**actual)
        self._editor.tag_configure(tag, font=font)

    def _on_button_3_release_codeblock(self, text, tag):
        utils.update_clipboard(text, self._editor)
        font = Font(font=self._editor.tag_cget("codeblock", "font"))
        actual = font.actual()
        actual["underline"] = False
        font = Font(**actual)
        self._editor.tag_configure(tag, font=font)
