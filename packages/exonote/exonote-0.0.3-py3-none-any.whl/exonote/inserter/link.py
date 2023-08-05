import webbrowser
from tkinter.font import Font
from exonote import utils
from exonote import dto
from exonote import constant


class LinkInserter:
    def __init__(self, viewer):
        self._viewer = viewer
        self._editor = viewer.editor

    def insert(self, index, data):
        editor = self._viewer.editor
        statusbar = self._viewer.statusbar
        # define tag
        tag = "link_{}".format(self._viewer.next_id())
        editor.tag_configure(tag)
        tags = (tag, "link")
        is_executable = data["executable"]
        if is_executable:
            tags = (tag, "executable_link")
            self._handle_program_link(data, tag, statusbar)
        else:
            self._handle_link(data, tag, statusbar)
        # insert
        text = data.get("text")
        editor.insert(index, text, tags)

    def _handle_link(self, data, tag, statusbar):
        # expand data
        text, target = data["text"], data["target"]
        if not target:
            return
        # bind events handlers
        if target.startswith("http://") or target.startswith("https://"):
            element = "(web)"
        elif target.startswith("<") and target.endswith(">"):
            element = "(anchor)"
        else:
            filename, anchor = utils.split_target(target)
            page_info = self._viewer.pages.get(filename)
            if not page_info:
                return
            element = "[{}]".format(page_info.page)
        status_info = {"text": target, "tag": element}
        # - bind on hover link
        self._bind_on_hover_link(status_info, tag, statusbar)
        # - bind on click link
        self._bind_on_click_link(target, tag)

    def _handle_program_link(self, data, tag, statusbar):
        # expand data
        text, target = data["text"], data["target"]
        # bind events handlers
        status_info = {"text": target, "tag": "(exec)"}
        # - bind on hover link
        self._bind_on_hover_link(status_info, tag, statusbar)
        # - bind on click link
        if self._viewer.restriction != constant.HIGH:
            self._bind_on_click_link(target, tag, is_executable=True)

    # ===== LINK - ON HOVER =====

    def _bind_on_hover_link(self, status_info, tag, statusbar):
        # on pointer enters link
        handler = (lambda e:
                   self._on_enter_link(statusbar, status_info))
        self._editor.tag_bind(tag, "<Enter>", handler, True)
        # on pointer leaves link
        handler = (lambda e:
                   self._on_leave_link(statusbar))
        self._editor.tag_bind(tag, "<Leave>", handler, True)

    def _on_enter_link(self, statusbar, status_info):
        text = status_info.get("text")
        tag = status_info.get("tag")
        self._editor.config(cursor="hand1")
        if tag == "(exec)":
            foreground = "#5E3C5E"
            background = "#FFDDFF"
        else:
            foreground = "#2E3749"
            background = "#E4EDFF"
        statusbar.show(text, tag=tag, foreground=foreground,
                       background=background)

    def _on_leave_link(self, statusbar):
        self._editor.config(cursor="")
        statusbar.hide()

    # ===== LINK - ON CLICK =====

    def _bind_on_click_link(self, target,
                            tag, is_executable=False):
        # button-1 press
        handler = (lambda e:
                   self._on_button_1_press_link(tag))
        self._editor.tag_bind(tag, "<ButtonPress-1>", handler, True)
        # button-1 release
        handler = (lambda e:
                   self._on_button_1_release_link(target, tag, is_executable))
        self._editor.tag_bind(tag, "<ButtonRelease-1>", handler, True)

        # button-3 press
        handler = (lambda e:
                   self._on_button_3_press_link(tag))
        self._editor.tag_bind(tag, "<ButtonPress-3>", handler, True)
        # button-3 release
        handler = (lambda e:
                   self._on_button_3_release_link(target, tag))
        self._editor.tag_bind(tag, "<ButtonRelease-3>", handler, True)

    def _on_button_1_press_link(self, tag):
        font = Font(font=self._editor.tag_cget("link", "font"))
        actual = font.actual()
        actual["underline"] = True
        font = Font(**actual)
        self._editor.tag_configure(tag, font=font)

    def _on_button_1_release_link(self, target, tag, is_executable):
        font = Font(font=self._editor.tag_cget("link", "font"))
        actual = font.actual()
        actual["underline"] = False
        font = Font(**actual)
        self._editor.tag_configure(tag, font=font)
        if is_executable:
            self._run_program(target)
        else:
            self._editor.config(cursor="")
            self._open_link(target)

    def _run_program(self, target):
        target = target.lstrip("${").rstrip("}")
        cache = utils.get_callable(target)
        if not cache:
            return
        callable_name, callable_object, arguments = cache
        program_context = dto.ProgramContext(self._viewer, arguments)
        callable_object(program_context)

    def _open_link(self, target):
        target = target.strip()
        if target.startswith("http://") or target.startswith("https://"):
            open_url(target, self._editor)
        elif target.startswith("<") and target.endswith(">"):
            self._viewer.goto(target)
        else:
            self._viewer.open(target)

    def _on_button_3_press_link(self, tag):
        font = Font(font=self._editor.tag_cget("link", "font"))
        actual = font.actual()
        actual["underline"] = True
        font = Font(**actual)
        self._editor.tag_configure(tag, font=font)

    def _on_button_3_release_link(self, target, tag):
        utils.update_clipboard(target, self._editor)
        font = Font(font=self._editor.tag_cget("link", "font"))
        actual = font.actual()
        actual["underline"] = False
        font = Font(**actual)
        self._editor.tag_configure(tag, font=font)


def open_url(url, widget):
    command = lambda: webbrowser.open(url, new=0)
    widget.after(1, command)
