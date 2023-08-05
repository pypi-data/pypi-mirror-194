import os
import os.path
import tkinter as tk
import pathlib
from exonote.inserter import util


class AttachmentInserter:
    def __init__(self, viewer):
        self._viewer = viewer
        self._editor = viewer.editor

    def insert(self, index, data):
        target = data.get("target")
        if is_image(target):
            self._insert_image(index, data)

    def _insert_image(self, index, data):
        dossier = self._viewer.dossier
        target = data.get("target", "").strip()
        caption = data.get("caption", "").strip()
        top_gap = data.get("top_gap", "")
        bottom_gap = data.get("bottom_gap", "")
        target_parts = target.split("/")
        p = pathlib.Path(dossier, *target_parts)
        path = str(p.resolve())
        # default image title (if file missing)
        attachment_syntax = "@[{}]({})".format(data.get("title"), target)
        if not os.path.isfile(path):
            self._editor.insert(index, attachment_syntax, "notice")
            return
        # manage caption
        if caption:
            index = util.insert_top_gap(self._editor, top_gap)
        # open and insert image
        self._editor.insert(index, attachment_syntax, "hidden")
        photo_image = create_image(path, index, self._editor)
        self._cache_image(photo_image)
        if caption:
            caption = "  " + caption + "  "
            self._editor.tag_add("centered_component", index)
            #if caption and caption != "...":
            self._set_caption(caption)
        if bottom_gap:
            util.insert_bottom_gap(self._editor, bottom_gap)

    def _cache_image(self, photo_image):
        if not self._viewer.cache.get("images"):
            self._viewer.cache["images"] = list()
        self._viewer.cache["images"].append(photo_image)

    def _set_caption(self, caption):
        self._editor.insert(tk.INSERT, "\n")
        index = self._editor.index(tk.INSERT)
        self._viewer.render(caption, index=index)
        self._viewer.enable_edit_mode()
        #self._editor.mark_set(tk.INSERT, index)
        self._editor.tag_add("caption", index)


def is_image(path):
    _, ext = os.path.splitext(path)
    if ext.lower() in (".jpg", ".jpeg", ".gif",
                       ".png", ".pgm", ".ppm"):
        return True
    return False


def create_image(path, index, editor):
    with open(path, "rb") as file:
        img = file.read()
    photo_image = tk.PhotoImage(data=img)
    editor.image_create(index, image=photo_image)
    return photo_image
