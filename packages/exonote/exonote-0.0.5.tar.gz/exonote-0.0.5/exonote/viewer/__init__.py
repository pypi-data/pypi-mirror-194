import os
import os.path
import sys
import tkinter as tk
from tkinter.font import Font, families as get_font_families
from collections import OrderedDict
from exonote import dto
from exonote import error
from exonote.style import Style
from exonote.parser import parse
from exonote.inserter import Inserter
from exonote.statusbar import DefaultStatusBar
from exonote.element import Element
from exonote import constant
from exonote.viewer import util
from exonote import utils


class Viewer:
    def __init__(self, editor, dossier=None, style=Style(), inserter=Inserter,
                 scroll_step=25, restriction=constant.ZERO,
                 statusbar=DefaultStatusBar, on_open=None, on_press_left=None,
                 on_press_right=None, on_press_up=None, on_press_down=None,
                 update_sys_path=True):
        self._editor = editor
        self._dossier = dossier if dossier else os.getcwd()
        self._style = style
        self._inserter = inserter(self)
        self._scroll_step = scroll_step
        self._restriction = restriction
        self._statusbar = statusbar(self) if statusbar else None
        self._on_open = on_open
        self._on_press_left = on_press_left
        self._on_press_right = on_press_right
        self._on_press_up = on_press_up
        self._on_press_down = on_press_down
        self._update_sys_path = update_sys_path
        self._sections = dict()
        self._new = True
        self._i = 0
        self._history = list()
        self._filename = None
        self._data = dict()
        self._scrollable = util.Scrollable(self._editor, scroll_step)
        self._cache = OrderedDict()
        self._anchors = list()
        self._pages = OrderedDict()
        self._root = editor.nametowidget(".")
        self._setup()

    @property
    def editor(self):
        return self._editor

    @property
    def dossier(self):
        return self._dossier
    
    @property
    def style(self):
        return self._style

    @property
    def inserter(self):
        return self._inserter

    @property
    def scroll_step(self):
        return self._scroll_step

    @property
    def restriction(self):
        return self._restriction

    @property
    def statusbar(self):
        return self._statusbar

    @property
    def on_open(self):
        return self._on_open

    @on_open.setter
    def on_open(self, val):
        self._on_open = val

    @property
    def update_sys_path(self):
        return self._update_sys_path

    @property
    def filename(self):
        return self._filename

    @property
    def history(self):
        return self._history.copy()

    @property
    def sids(self):
        """Ordered list of SIDs (Section IDs)"""
        return [sid for _, sid in util.order_sids(self._editor, self._sections)]

    @property
    def anchors(self):
        """List of anchors"""
        return self._anchors

    @property
    def data(self):
        return self._data

    @property
    def cache(self):
        return self._cache

    @property
    def readonly(self):
        state = str(self._editor.cget("state"))
        return True if state == tk.DISABLED else False

    @property
    def root(self):
        return self._root

    @property
    def coords(self):
        if not self._editor.winfo_exists():
            return
        x, y = self._editor.winfo_rootx(), self._editor.winfo_rooty()
        return x, y
        
    @property
    def pages(self):
        return self._pages

    # ==== OPEN & RENDER ====

    def open(self, target):
        """target shouldn't be an absolute filesystem path but relative to the dossier"""
        if self._statusbar:
            self._statusbar.hide()
        if self._on_open:
            target = self._on_open(self, target)
        if not target:
            return
        filename, sid = utils.split_target(target)
        if os.path.isabs(filename):
            msg = "The filename shouldn't be an absolute path: {}"
            raise error.Error(msg.format(filename))
        absolute_path = util.abspath(filename, self._dossier)
        if not os.path.isfile(absolute_path):
            return False
        with open(absolute_path, "r") as file:
            data = file.read()
        self.clear()
        self._filename = filename
        self.render(data)
        # update self._history
        self._history.append(filename)
        # goto
        if sid:
            self.goto(sid)
        return True

    def refresh(self):
        if self._filename:
            return self.open(self._filename)
        return False

    def render(self, source, index=tk.INSERT):
        """
        Render and insert the source at a specific index inside the viewer widget
        source = text or structure returned by parser"""
        if self._statusbar:
            self._statusbar.hide()
        if isinstance(source, str):
            structure = parse(source)
        else:
            structure = source
        if self._new:
            # define tags
            self._define_tags()
            # bind events handlers to tags
            self._bind_handlers_to_tags()
            self._new = False
        self.enable_edit_mode()
        self._render(structure, index)
        self.disable_edit_mode()
        return True

    # ==== READ AND WRITE HEADINGS ====

    def get_heading(self, sid, include_text=False):
        data = self._sections.get(sid)
        if data is None:
            return None
        index, level = self._editor.index(sid), data["level"]
        index_end = self.compute_index(index, char_spec="=end")
        text = self._editor.get(index, index_end) if include_text else None
        info = dto.HeadingInfo(sid, index, index_end, level, text.strip())
        return info

    def read_heading(self, sid):
        info = self.get_heading(sid)
        if info is None:
            return None
        index, index_end = info.index, info.index_end
        text = self._editor.get(index, index_end)
        return text

    def edit_heading(self, sid, text):
        info = self.get_heading(sid)
        if info is None:
            return False
        index, index_end = info.index, info.index_end
        tags = self._sections.get(sid).get("tags")
        self.enable_edit_mode()
        self._editor.delete(index, index_end)
        self._editor.insert(index, text, tags)
        self.disable_edit_mode()
        return True

    def del_heading(self, sid):
        data = self._sections.get(sid)
        if not data:
            return False
        index = self._editor.index(sid)
        index_begin = self.compute_index(index, line_spec="-1", char_spec="=0")
        index_end = self.compute_index(index, char_spec="=end+1c")
        self.enable_edit_mode()
        self._editor.delete(index_begin, index_end)
        del self._sections[sid]
        self._editor.mark_unset(sid)
        self.disable_edit_mode()
        return True

    # ==== READ AND WRITE SECTIONS ====

    def get_section(self, sid, include_text=False):
        """return a tuple (heading, body)"""
        info = self.get_heading(sid, include_text)
        if not info:
            return None
        index, heading, level = info.index, info.text, info.level
        index_begin = self.compute_index(index, line_spec="+1", char_spec="=0")
        index_end = self._get_section_end(sid)
        body = None
        if include_text:
            body = self._editor.get(index_begin, index_end)
        info = dto.SectionInfo(sid, index, index_end, heading, level, body)
        return info

    def read_section(self, sid):
        info = self.get_section(sid, include_text=True)
        if not info:
            return None
        return info.text

    def edit_section(self, sid, source):
        info = self.get_section(sid, include_text=False)
        if not info:
            return None
        index = info.index
        index = self.compute_index(index, line_spec="+1", char_spec="=0")
        index_end = self._get_section_end(sid)
        self.enable_edit_mode()
        self._editor.delete(index, index_end)
        self.render(source, index)
        self.disable_edit_mode()

    def extend_section(self, sid, source, side=constant.BOTTOM):
        """ Position is either top or bottom """
        data = self._sections.get(sid)
        if not data:
            return False
        if side == constant.TOP:
            index = self._editor.index(sid)
            index = self.compute_index(index, line_spec="+1", char_spec="=0")
        elif side == constant.BOTTOM:
            index = self._get_section_end(sid)
        else:
            msg = ("The 'side' argument should be either",
                   "exonote.constant.TOP or exonote.constant.BOTTOM.")
            raise error.Error(" ".join(msg))
        return self.render(source, index)

    def clear_section(self, sid):
        data = self._sections.get(sid)
        if not data:
            return False
        index = self._editor.index(sid)
        index_begin = self.compute_index(index, line_spec="+1", char_spec="=0")
        index_end = self._get_section_end(sid)
        index_end = self.compute_index(index_end, line_spec="+1", char_spec="=0")
        self.enable_edit_mode()
        self._editor.delete(index_begin, index_end)
        self.disable_edit_mode()
        return True

    def del_section(self, sid):
        if sid not in self._sections:
            return False
        index_begin = self._editor.index(sid)
        index_end = self._get_section_end(sid)
        index_end = self.compute_index(index_end, line_spec="+3", char_spec="=0")
        self.enable_edit_mode()
        self._editor.delete(index_begin, index_end)
        del self._sections[sid]
        self._editor.mark_unset(sid)
        self.disable_edit_mode()
        return True

    # ==== INDEX MANIPULATION ====

    def goto(self, index):
        if index in ("<TOP>", "<BOTTOM>"):
            pass
        elif index.startswith("<"):
            if index not in self._anchors:
                return False
        try:
            self._editor.see(index)
        except Exception as e:
            return False
        info = self._editor.dlineinfo(index)
        if not info:
            return False
        y_coord = info[1]
        vertical_margin = self._style.vertical_margin
        y_coord -= vertical_margin
        self._editor.yview_scroll(y_coord, "pixels")
        return True

    def get_index(self, anchor):
        index = None
        try:
            index = self._editor.index(anchor)
        except Exception as e:
            pass
        return index

    def compute_index(self, index, line_spec=None, char_spec=None):
        """ Example: char_spec='+1' or '-1' or '=1' or None """
        index = self._editor.index(index)
        line, char = index.split(".")
        line = self._compute_single_index(int(line), line_spec)
        char = self._compute_single_index(int(char), char_spec)
        cache = "{}.{}".format(line, char)
        return self._editor.index(cache)

    def look_ahead(self, sid, level_spec=None, maxcount=None):
        """
        the argument 'levels' is either an integer or None.
        Examples:
             levels=None (look for sids without caring about their levels)
             levels=">" (look for sids with levels > to the reference sid)
             levels="<" (look for sids with levels < to the reference sid)
             levels="=" (look for sids with levels = to the reference sid)
             levels="=3" (look for sids with levels = to 3)
             levels="<=3" (look for sids with levels <= to 3)
        """
        data = self._sections.get(sid)
        if not data:
            return None
        return self._look(sid, level_spec, maxcount, backward=False)

    def look_behind(self, sid, level_spec=None, maxcount=None):
        """
        the argument 'levels' is either a string or None.
        Examples:
             levels=None (look for sids without caring about their levels)
             levels=">" (look for sids with levels > to the reference sid)
             levels="<" (look for sids with levels < to the reference sid)
             levels="=" (look for sids with levels < to the reference sid)
             levels="=3" (look for sids with levels = to 3)
             levels="<=3" (look for sids with levels <= to 3)
        """
        data = self._sections.get(sid)
        if not data:
            return None
        return self._look(sid, level_spec, maxcount, backward=True)

    # ==== MISC ====

    def register_section(self, sid, index, level, tags):
        if sid in self._sections:
            i = 0
            success = False
            while i < 65536:
                new_sid = "{}_{}".format(sid, i+1)
                if new_sid not in self._sections:
                    sid = new_sid
                    success = True
                    break
            if not success:
                msg = "The section '{}' is already defined.".format(sid)
                raise error.Error(msg)
        self.register_anchor(sid, index)
        self._sections[sid] = {"level": level, "tags": tags, "mark": sid}

    def register_anchor(self, name, index):
        self._editor.mark_set(name, index)
        self._editor.mark_gravity(name, tk.LEFT)
        self._anchors.append(name)

    def next_id(self):
        """Generate ID ! Generate and return a unique identifier (int)"""
        self._i += 1
        return self._i

    def make_scrollable(self, widget):
        self._scrollable.set(widget)

    def disable_edit_mode(self):
        self._editor.config(state=tk.DISABLED)

    def enable_edit_mode(self):
        self._editor.config(state=tk.NORMAL)

    def clear(self):
        self.enable_edit_mode()
        for tag in self._editor.tag_names():
            self._editor.tag_delete(tag)
        self._editor.delete("1.0", tk.END)
        self._sections = dict()
        self.disable_edit_mode()
        self._new = True

    def _setup(self):
        if not isinstance(self._editor, tk.Text):
            raise error.Error("Only tk.Text widget and subclasses are allowed as Editor.")
        # update sys.path
        if self._update_sys_path:
            sys.path.insert(1, self._dossier)
        # update style
        self._update_style()
        # set editor config
        self._set_editor_config()
        # padding
        #self._editor.config(padx=10)
        # create <TOP> and <BOTTOM> anchors
        self._create_top_bottom_anchors()
        # readonly
        self.disable_edit_mode()
        # get pages
        self._pages = util.get_pages(self._dossier)
        
    def _set_editor_config(self):
        self._editor.bind("<Button-1>",
                          lambda e, editor=self._editor: editor.focus_set())
        self._editor.bind("<Up>", self._on_key_up, True)
        self._editor.bind("<Down>", self._on_key_down, True)
        self._editor.bind("<Left>", self._on_key_left, True)
        self._editor.bind("<Right>", self._on_key_right, True)
        self._editor.bind("<MouseWheel>", self._on_mouse_wheel, True)
        self._editor.bind("<Button-4>", self._on_mouse_wheel, True)
        self._editor.bind("<Button-5>", self._on_mouse_wheel, True)
        # set editor config
        font = Font(family=self._style.font_family,
                    size=self._style.font_size,
                    weight=self._style.font_weight,
                    slant=self._style.font_slant)
        spacing1 = spacing3 = self._style.spacing
        spacing2 = spacing1 + spacing3
        self._editor.config(wrap="word", font=font, cursor="arrow",
                            background=self._style.background_color,
                            spacing1=spacing1, spacing2=spacing2, spacing3=spacing3,
                            foreground=self._style.foreground_color,
                            selectbackground=self._style.selection_background_color,
                            selectforeground=self._style.foreground_color,
                            inactiveselectbackground=self._style.selection_background_color,
                            padx=self._style.horizontal_margin,
                            pady=self._style.vertical_margin)

    def _create_top_bottom_anchors(self):
        # top
        top_anchor = "<TOP>"
        self._editor.mark_set(top_anchor, 1.0)
        self._editor.mark_gravity(top_anchor, tk.LEFT)
        # bottom
        bottom_anchor = "<BOTTOM>"
        self._editor.mark_set(bottom_anchor, 1.0)
        self._editor.mark_gravity(bottom_anchor, tk.RIGHT)

    def _render(self, structure, index):
        index = self._editor.index(index)
        self._editor.mark_set(tk.INSERT, index)
        cache = list()
        for element, data in structure:
            if element in (Element.ATTACHMENT,
                           Element.PROGRAM, Element.TABLE):
                mark = "<_{}{}_>".format(element.name, self.next_id())
                self._editor.mark_set(mark, index)
                self._editor.mark_gravity(mark, tk.LEFT)
                cache.append((element, mark, data))
                continue
            self._inserter.insert(element, index, data)
            index = self._editor.index(tk.INSERT)
        self._editor.update_idletasks()
        self._finalize_rendering(cache)

    def _finalize_rendering(self, cache):
        programs_cache = list()
        for element, mark, data in cache:
            index = self._editor.index(mark)
            self._editor.mark_set(tk.INSERT, index)
            if element == Element.PROGRAM:
                programs_cache.append((element, index, data))
                continue
            self._inserter.insert(element, index, data)
        for element, index, data in programs_cache:
            self._editor.mark_set(tk.INSERT, index)
            self._inserter.insert(element, index, data)
        self.disable_edit_mode()

    def _define_tags(self):
        self._define_headings_tags()
        self._define_emphasis_tags()
        self._define_alignment_tags()
        self._define_codeblock_tag()
        self._define_link_tags()
        self._define_gap_tag()
        self._define_caption_tag()
        self._define_centered_component_tags()
        self._define_hidden_tag()
        self._define_highlighting_tags()

    def _define_headings_tags(self):
        text_font_size = self._style.font_size
        # Heading
        heading_1_font = Font(size=text_font_size + 12)
        heading_2_font = Font(size=text_font_size + 10)
        heading_3_font = Font(size=text_font_size + 8)
        heading_4_font = Font(size=text_font_size + 6)
        heading_5_font = Font(size=text_font_size + 4)
        heading_6_font = Font(size=text_font_size + 2)
        # font config
        for font in (heading_1_font, heading_2_font,
                     heading_3_font, heading_4_font,
                     heading_5_font, heading_6_font):
            font.config(family=self._style.font_family,
                        weight=self._style.heading_font_weight)
        # tag config
        extra_space = 3
        spacing3 = self._style.spacing
        spacing3 += extra_space
        for tag, font in (("heading_1", heading_1_font),
                          ("heading_2", heading_2_font),
                          ("heading_3", heading_3_font),
                          ("heading_4", heading_4_font),
                          ("heading_5", heading_5_font),
                          ("heading_6", heading_6_font)):
            self._editor.tag_configure(tag, font=font,
                                       foreground=self._style.heading_foreground_color,
                                       spacing3=spacing3)

    def _define_emphasis_tags(self):
        # code
        font = Font(family=self._style.monospace_font_family,
                    size=self._style.font_size)
        self._editor.tag_configure("code", font=font,
                                   background=self._style.code_background_color)
        # monospace
        font = Font(family=self._style.monospace_font_family,
                    size=self._style.font_size)
        self._editor.tag_configure("monospace", font=font)
        # bold
        bold_font = Font(family=self._style.font_family,
                         size=self._style.font_size,
                         weight=self._style.bold_font_weight)
        self._editor.tag_configure("bold", font=bold_font)
        # bold_monospace
        bold_monospace_font = Font(family=self._style.monospace_font_family,
                                   size=self._style.font_size,
                                   weight=self._style.bold_font_weight)
        self._editor.tag_configure("bold_monospace", font=bold_monospace_font)
        # underline
        underline_font = Font(family=self._style.font_family,
                              size=self._style.font_size,
                              underline=True)
        self._editor.tag_configure("underline", font=underline_font)
        # italic
        italic_font = Font(family=self._style.font_family,
                           size=self._style.font_size,
                           slant=self._style.italic_font_slant)
        self._editor.tag_configure("italic", font=italic_font)
        # warning
        warning_font = Font(family=self._style.font_family,
                            size=self._style.font_size)
        self._editor.tag_configure("warning", font=warning_font,
                                   foreground=self._style.warning_color)
        # notice
        notice_font = Font(family=self._style.font_family,
                           size=self._style.font_size)
        self._editor.tag_configure("notice", font=notice_font,
                                   foreground=self._style.notice_color)
        # strikethrough
        strikethrough_font = Font(overstrike=True,
                                  family=self._style.font_family,
                                  size=self._style.font_size)
        self._editor.tag_configure("strikethrough", font=strikethrough_font)

    def _define_alignment_tags(self):
        self._editor.tag_configure("center_alignment", justify="center")
        self._editor.tag_configure("left_alignment", justify="left")
        self._editor.tag_configure("right_alignment", justify="right")

    def _define_codeblock_tag(self):
        # codeblock
        codeblock_font = Font(family=self._style.monospace_font_family,
                              size=self._style.font_size)
        self._editor.tag_configure("codeblock", font=codeblock_font,
                                   foreground=self._style.codeblock_foreground_color)

    def _define_link_tags(self):
        # link
        font = Font(family=self._style.font_family, size=self._style.font_size)
        self._editor.tag_configure("link", font=font,
                                   foreground=self._style.link_foreground_color)
        # executable link
        font = Font(family=self._style.monospace_font_family,
                    size=self._style.font_size)
        self._editor.tag_configure("executable_link", font=font,
                                   foreground=self._style.executable_link_foreground_color)


    def _define_gap_tag(self):
        self._editor.tag_configure("gap", spacing1=0,
                                   spacing2=0, spacing3=0,)

    def _define_caption_tag(self):
        extra_space = 3
        spacing = self._style.spacing
        spacing += extra_space
        self._editor.tag_configure("caption", justify="center",
                                   spacing1=spacing, spacing3=spacing)

    def _define_centered_component_tags(self):
        extra_space = 3
        spacing1 = self._style.spacing
        spacing1 += extra_space
        spacing3 = self._style.spacing
        spacing3 += extra_space
        self._editor.tag_configure("centered_component",
                                   justify="center",
                                   spacing1=spacing1,
                                   spacing3=spacing3)

    def _define_hidden_tag(self):
        # 'hidden' tag
        self._editor.tag_configure("hidden", elide=True)

    def _define_highlighting_tags(self):
        color = self._style.highlight_color
        self._editor.tag_configure("highlight", background=color)
        color = self._style.active_highlight_color
        self._editor.tag_configure("active_highlight", background=color)

    def _bind_handlers_to_tags(self):
        # on_enter and on_leave event handlers
        on_enter = lambda event, editor=self._editor: editor.config(cursor="hand1")
        on_leave = lambda event, editor=self._editor: editor.config(cursor="")
        # bind hand icon to codeblock (enter vs leave)
        self._editor.tag_bind("codeblock", "<Enter>", on_enter, True)
        self._editor.tag_bind("codeblock", "<Leave>", on_leave, True)
        # bind hand icon to link (enter vs leave)
        self._editor.tag_bind("link", "<Enter>", on_enter, True)
        self._editor.tag_bind("link", "<Leave>", on_leave, True)
        # bind hand icon to headings (enter vs leave)
        for tag in ("heading_1", "heading_2", "heading_3",
                    "heading_4", "heading_5", "heading_6"):
            self._editor.tag_bind(tag, "<Enter>", on_enter, True)
            self._editor.tag_bind(tag, "<Leave>", on_leave, True)

    def _update_style(self):
        font_family = self._style.font_family
        monospace_font_family = self._style.monospace_font_family
        available_fonts = get_font_families()
        if font_family not in available_fonts:
            self._style.font_family = utils.get_standard_font_family("TkTextFont")
        if monospace_font_family not in available_fonts:
            self._style.monospace_font_family = utils.get_standard_font_family("TkFixedFont")

    def _on_mouse_wheel(self, event):
        # scroll down   (value: 1)   <-  event.num = 5   or  event.delta < 0
        # scroll up     (value: -1)  <-  event.num = 4   or  event.delta >= 0
        util.on_mouse_wheel(event, self._editor, self._scroll_step)
        return "break"

    def _look(self, sid, level_spec, maxcount, backward=False):
        sids, comparison, comparison_target = self._look_part_1(sid,
                                                                level_spec,
                                                                backward)
        results = self._look_part_2(sid, sids, comparison,
                                   comparison_target, maxcount)
        return results

    def _look_part_1(self, sid, level_spec, backward):
        sids = self.sids
        if backward:
            sids = reversed(sids)
        comparison = None
        comparison_target = self._sections[sid]["level"]
        if not level_spec:
            pass
        elif level_spec in ("<", ">", "=", ">=", "<="):
            comparison = level_spec
        else:
            right_side = level_spec.lstrip("<=>")
            left_side = level_spec.rstrip(right_side)
            comparison = left_side
            comparison_target = int(right_side)
        return sids, comparison, comparison_target

    def _look_part_2(self, sid, sids, comparison, comparison_target, maxcount):
        # ===
        results = list()
        reference_reached = False
        i = 0
        for x in sids:
            if x == sid:
                reference_reached = True
                continue
            if not reference_reached:
                continue
            x_level = self._sections[x]["level"]
            matched = False
            if comparison is None:
                matched = True
            elif comparison == "<" and x_level < comparison_target:
                matched = True
            elif comparison == ">" and x_level > comparison_target:
                matched = True
            elif comparison == "=" and x_level == comparison_target:
                matched = True
            elif comparison == "<=" and x_level <= comparison_target:
                matched = True
            elif comparison == ">=" and x_level >= comparison_target:
                matched = True
            if not matched:
                continue
            results.append(x)
            i += 1
            if maxcount and maxcount == i:
                break
        return results

    def _get_section_end(self, sid):
        sids_ahead = self.look_ahead(sid, maxcount=1)
        index_end = "end-1c"
        if sids_ahead:
            mark = self._sections[sids_ahead[0]]["mark"]
            index = self._editor.index(mark)
            index_end = self.compute_index(index, line_spec="-3",
                                           char_spec="=end")
        return self._editor.index(index_end)

    def _compute_single_index(self, index, spec):
        if not spec:
            return index
        command = spec[0]
        val = spec[1:]
        if command == "+":
            index += int(val)
        elif command == "-":
            index -= int(val)
        elif command == "=":
            index = val
        else:
            msg = "Unknown index computation command {}".format(command)
            raise error.Error(msg)
        return index

    def _on_key_up(self, event):
        util.scroll_up(self._editor, self._scroll_step)
        if self._on_press_up:
            self._on_press_up()
        return "break"

    def _on_key_down(self, event):
        util.scroll_down(self._editor, self._scroll_step)
        if self._on_press_down:
            self._on_press_down()
        return "break"

    def _on_key_left(self, event):
        if self._on_press_left:
            self._on_press_left()
        return "break"


    def _on_key_right(self, event):
        if self._on_press_right:
            self._on_press_right()
        return "break"
