import tkinter as tk
import tkutil
from exonote import constant


class StatusBar:
    def __init__(self, viewer):
        self._viewer = viewer

    @property
    def viewer(self):
        return self._viewer

    def show(self, text, tag=None, duration=None,
             delay=None, foreground=None, background=None):
        pass

    def hide(self):
        pass


class DefaultStatusBar(StatusBar):
    def __init__(self, viewer):
        super().__init__(viewer)
        self._editor = viewer.editor
        self._windows = list()
        self._cancel_ids = list()
        self._coords = (0, 0)

    def show(self, text, tag=None,
             duration=constant.DEFAULT_STATUSBAR_DURATION,
             delay=constant.DEFAULT_STATUSBAR_DELAY,
             foreground=constant.DEFAULT_STATUSBAR_FOREGROUND,
             background=constant.DEFAULT_STATUSBAR_BACKGROUND):
        self.hide()
        command = lambda: self._show(text, tag, duration,
                                     foreground, background)
        cancel_id = self._editor.after(delay, command)
        self._cancel_ids.append(cancel_id)

    def hide(self):
        for cancel_id in self._cancel_ids:
            self._editor.after_cancel(cancel_id)
        self._cancel_ids = list()
        for window in self._windows:
            try:
                window.destroy()
            except Exception as e:
                pass
        self._windows = list()

    def _show(self, text, tag, duration, foreground, background):
        self._coords = self._viewer.coords
        tag = tag if tag else None
        window = tk.Toplevel(self._editor)
        self._build_window(window, text, tag, foreground, background)
        self._windows.append(window)
        cancel_id = self._editor.after(duration, self.hide)
        self._cancel_ids.append(cancel_id)

    def _build_window(self, window, text, tag, foreground, background):
        window.overrideredirect(True)
        font_family = self._viewer.style.monospace_font_family
        font_size = self._viewer.style.font_size
        if tag:
            tag_label = tk.Label(window, text=tag,
                                 font=(font_family, font_size, "bold"),
                                 background=background,
                                 foreground=foreground)
            tag_label.pack(side=tk.LEFT)
        text_label = tk.Label(window, text=text,
                              font=(font_family, font_size),
                              background=background,
                              foreground=foreground)
        text_label.pack(side=tk.LEFT)
        self._relocate_window(window)

    def _relocate_window(self, window):
        x, y = self._coords
        #window.withdraw()
        #window.update_idletasks()
        #window.geometry("")
        #window.update_idletasks()
        tkutil.hide_early(window)
        y = y + self._editor.winfo_height() - window.winfo_height()
        window.geometry("+{}+{}".format(x, y))
        window.deiconify()
