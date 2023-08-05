import tkinter as tk
from tkinter.font import Font
from exonote import utils
from exonote.element import Element


class HeadingInserter:
    def __init__(self, viewer):
        self._viewer = viewer
        self._editor = viewer.editor

    def insert(self, index, data):
        # expand data
        level, text = data["level"], data["text"]
        # generic tag
        generic_tag = "heading_{}".format(level)
        # tag
        tag = "{}_{}".format(generic_tag, self._viewer.next_id())
        # sid (heading id)
        sid = data["id"]
        # define tag
        self._editor.tag_configure(tag)
        # bind events handlers
        hover_info = {"element": Element.HEADING.name, "sid": sid}
        # - bind on hover link
        self._bind_on_hover_heading(hover_info, tag)
        # - bind on click link
        self._bind_on_click_heading(sid, generic_tag, tag)
        # alignment
        center = data.get("center", False)
        # insert
        index = self._insert_top_margin()
        tags = [generic_tag, tag]
        if center:
            text = " " + text + " "
            tags.append("center_alignment")
        self._viewer.register_section(sid, index, level, tags)
        self._editor.insert(index, text, tags)
        self._insert_bottom_margin()

    def _insert_top_margin(self):
        index = self._editor.index(tk.INSERT)
        if index == "1.0":
            return index
        _, col = index.split(".")
        newlines = "\n"
        #if col != "0":
        #    newlines = "\n\n\n"
        self._editor.insert(index, "\n\n\n", "gap")
        return self._editor.index(tk.INSERT)

    def _insert_bottom_margin(self):
        self._editor.insert(tk.INSERT, "\n", "gap")

    # ===== HEADING - ON HOVER =====

    def _bind_on_hover_heading(self, hover_info, tag):
        # on pointer enters link
        """
        handler = (lambda e, editor=editor, h=h, hover_info=hover_info:
                   _on_enter_heading(editor, h, hover_info))
        editor.tag_bind(tag, "<Enter>", handler, True)
        # on pointer leaves link
        handler = (lambda e, editor=editor, h=h:
                   _on_leave_heading(editor, h))
        editor.tag_bind(tag, "<Leave>", handler, True)
        """

    def _on_enter_heading(self, hover_info):
        """
        h.enter_event("hover", **hover_info)
        editor.config(cursor="hand1")
        """

    def _on_leave_heading(self, h):
        h.leave_event("hover")
        self._editor.config(cursor="")

    # ===== HEADING - ON CLICK =====

    def _bind_on_click_heading(self, sid, generic_tag, tag):
        # button-1 press
        handler = (lambda e:
                   self._on_button_1_press_heading(generic_tag, tag))
        self._editor.tag_bind(tag, "<ButtonPress-1>", handler, True)
        # button-1 release
        handler = (lambda e:
                   self._on_button_1_release_heading( sid, generic_tag, tag))
        self._editor.tag_bind(tag, "<ButtonRelease-1>", handler, True)
        # button-3 press
        handler = (lambda e, tag=tag:
                   self._on_button_3_press_heading(generic_tag, tag))
        self._editor.tag_bind(tag, "<ButtonPress-3>", handler, True)
        # button-3 release
        handler = (lambda e, sid=sid, tag=tag:
                   self._on_button_3_release_heading(sid, generic_tag, tag))
        self._editor.tag_bind(tag, "<ButtonRelease-3>", handler, True)

    def _on_button_1_press_heading(self, generic_tag, tag):
        font = Font(font=self._editor.tag_cget(generic_tag, "font"))
        actual = font.actual()
        actual["underline"] = True
        font = Font(**actual)
        self._editor.tag_configure(tag, font=font)

    def _on_button_1_release_heading(self, sid, generic_tag, tag):
        utils.update_clipboard(sid, self._editor)
        font = Font(font=self._editor.tag_cget(generic_tag, "font"))
        actual = font.actual()
        actual["underline"] = False
        font = Font(**actual)
        self._editor.tag_configure(tag, font=font)
        self._viewer.goto(sid)

    def _on_button_3_press_heading(self, generic_tag, tag):
        font = Font(font=self._editor.tag_cget(generic_tag, "font"))
        actual = font.actual()
        actual["underline"] = True
        font = Font(**actual)
        self._editor.tag_configure(tag, font=font)

    def _on_button_3_release_heading(self, sid, generic_tag, tag):
        utils.update_clipboard(sid, self._editor)
        font = Font(font=self._editor.tag_cget(generic_tag, "font"))
        actual = font.actual()
        actual["underline"] = False
        font = Font(**actual)
        self._editor.tag_configure(tag, font=font)
