import tkinter as tk


def insert_top_gap(editor, gap):
    index = editor.index(tk.INSERT)
    if index == "1.0":
        return index
    return insert_gap(editor, gap)


def insert_bottom_gap(editor, gap):
    return insert_gap(editor, gap)


def insert_gap(editor, gap):
    n = gap.count("\n")
    if n == 1:
        editor.insert(tk.INSERT, "\n", "gap")
    elif n > 1:
        editor.insert(tk.INSERT, "\n\n", "gap")
    return editor.index(tk.INSERT)
