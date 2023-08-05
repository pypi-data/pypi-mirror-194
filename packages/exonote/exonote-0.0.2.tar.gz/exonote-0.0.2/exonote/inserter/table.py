import tkinter as tk
from exonote.inserter import util


class TableInserter:
    def __init__(self, viewer):
        self._viewer = viewer
        self._editor = viewer.editor

    def insert(self, index, data):
        rows = data.get("rows", "")
        caption = data.get("caption", "").strip()
        top_gap = data.get("top_gap", "")
        bottom_gap = data.get("bottom_gap", "")
        cache = Table.parse(rows)
        if not cache:
            text = "[] {}\n{}(inconsistent table)\n".format(caption, rows)
            self._editor.insert(index, text, "warning")
            return
        headers_tag = ("bold_monospace", "center_alignment")
        rows_tag = ("monospace", "center_alignment")
        if not caption:
            headers_tag = "bold_monospace"
            rows_tag = "monospace"
        headers, rows = cache
        sizes = [len(header) for header in headers]
        util.insert_top_gap(self._editor, top_gap)
        headers = self._update_row(headers)
        border = self._create_border(sizes)
        self._editor.insert(tk.INSERT, border, rows_tag)
        self._editor.insert(tk.INSERT, "\n")
        self._editor.insert(tk.INSERT, headers, headers_tag)
        self._editor.insert(tk.INSERT, "\n")
        self._editor.insert(tk.INSERT, border, rows_tag)
        for row in rows:
            self._editor.insert(tk.INSERT, "\n")
            row = self._update_row(row)
            self._editor.insert(tk.INSERT, row, rows_tag)
        self._editor.insert(tk.INSERT, "\n")
        self._editor.insert(tk.INSERT, border, rows_tag)
        if caption:
            caption = "  " + caption + "  "
            self._set_caption(caption)
        util.insert_bottom_gap(self._editor, bottom_gap)

    def _update_row(self, row):
        row = " | ".join(row)
        row = "| {} |".format(row)
        return row

    def _create_border(self, sizes):
        row = ["-" * x for x in sizes]
        row = "-+-".join(row)
        row = "+-{}-+".format(row)
        return row

    def _set_caption(self, caption):
        self._editor.insert(tk.INSERT, "\n")
        index = self._editor.index(tk.INSERT)
        self._viewer.render(caption, index=index)
        self._viewer.enable_edit_mode()
        self._editor.tag_add("caption", index)


class Table:

    @staticmethod
    def parse(text):
        cache = Table.interpret(text)
        if not cache:
            return
        headers, rows, sizes = cache
        if not Table.is_consistent(headers, rows):
            return
        Table.update_sizes(headers, sizes)
        Table.pad_headers(headers, sizes)
        Table.pad_rows(rows, sizes)
        return headers, rows

    @staticmethod
    def interpret(text):
        lines = text.strip().split("\n")
        if not lines:
            return
        rows = list()
        sizes = list()
        for line in lines:
            row = Table.interpret_line(line, sizes)
            rows.append(row)
        headers = rows.pop(0)
        return headers, rows, sizes

    @staticmethod
    def interpret_line(line, sizes):
        line = line.strip(" |").split("|")
        row = list()
        for i, col in enumerate(line):
            col = col.strip()
            row.append(col)
            n = len(col)
            try:
                if sizes[i] < n:
                    sizes[i] = n
            except IndexError as e:
                sizes.append(n)
        return row

    @staticmethod
    def update_sizes(headers, sizes):
        for i, header in enumerate(headers):
            size = sizes[i]
            if (len(header) % 2) != (size % 2):
                sizes[i] = size + 1

    @staticmethod
    def pad_headers(headers, sizes):
        for i, header in enumerate(headers):
            max_size = sizes[i]
            header_size = len(header)
            if max_size == header_size:
                continue
            x = (max_size - header_size) // 2
            pad = " " * x
            header = "{}{}{}".format(pad, header, pad)
            headers[i] = header

    @staticmethod
    def pad_rows(rows, sizes):
        for row in rows:
            for i, col in enumerate(row):
                max_size = sizes[i]
                col_size = len(col)
                if max_size == col_size:
                    continue
                x = max_size - col_size
                pad = " " * x
                col = "{}{}".format(col, pad)
                row[i] = col
        return rows

    @staticmethod
    def is_consistent(headers, rows):
        size = len(headers)
        for row in rows:
            if len(row) != size:
                return False
        return True
