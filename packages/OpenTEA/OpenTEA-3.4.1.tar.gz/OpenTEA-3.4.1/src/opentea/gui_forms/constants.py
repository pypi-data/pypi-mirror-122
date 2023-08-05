"""Constants definitions."""
import os
from glob import glob
import inspect
import platform

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msgbox
from tkinter.scrolledtext import ScrolledText
from tkinter import Variable as Tk_Variable
from tkinter import Canvas as Tk_Canvas
from PIL import ImageTk, Image

# BG_COLOR = '#%02x%02x%02x' % (220, 218, 213)
WIDTH_UNIT = 400
LINE_HEIGHT = 22
BASE_DIR = inspect.getfile(inspect.currentframe())
BASE_DIR = os.path.dirname(os.path.abspath(BASE_DIR))


IMAGE_DICT = dict()
PARAMS = dict()
VALIDATE = dict()


class SetException(Exception):
    """Define an exception on the widget setters."""


class GetException(Exception):
    """Define an exception on the widget getters."""


def quit_dialog():
    """Quitting dialog"""
    if msgbox.askokcancel("Quit", "Do you really wish to quit?"):
        PARAMS["top"].destroy()
        print("Get outta here and go back to your boring programs.")


# pylint: disable=global-statement
def set_constants(tksession, calling_dir, theme):
    """Set top Tk objet"""
    global PARAMS
    PARAMS["top"] = tksession
    PARAMS["calling_dir"] = calling_dir

    if theme not in ["alt", "aqua", "clam", "classic", "default"]:
        print(theme + " theme not supported. Fallback to clam...")
        theme = "clam"

    PARAMS["theme"] = theme
    if theme == "alt":
        bgc = (224, 224, 224)
        PARAMS["bg"] = "#%02x%02x%02x" % bgc
        PARAMS["bg_lbl"] = "#%02x%02x%02x" % (
            bgc[0] - 7,
            bgc[1] - 7,
            bgc[2] - 7,
        )
    if theme == "aqua":
        bgc = (240, 240, 240)
        PARAMS["bg"] = "#%02x%02x%02x" % bgc
        PARAMS["bg_lbl"] = "#%02x%02x%02x" % (
            bgc[0] - 7,
            bgc[1] - 7,
            bgc[2] - 7,
        )
    if theme == "clam":
        bgc = (220, 218, 213)
        PARAMS["bg"] = "#%02x%02x%02x" % bgc
        PARAMS["bg_lbl"] = PARAMS["bg"]
    if theme == "classic":
        bgc = (224, 224, 224)
        PARAMS["bg"] = "#%02x%02x%02x" % bgc
        PARAMS["bg_lbl"] = "#%02x%02x%02x" % (
            bgc[0] - 6,
            bgc[1] - 6,
            bgc[2] - 6,
        )
    if theme == "default":
        bgc = (220, 218, 213)
        PARAMS["bg"] = "#%02x%02x%02x" % bgc
        PARAMS["bg_lbl"] = "#%02x%02x%02x" % (
            bgc[0] - 3,
            bgc[1] - 1,
            bgc[2] + 4,
        )

    bgc_dark = tuple([int(0.3 * i) for i in bgc])
    PARAMS["bg_dark"] = "#%02x%02x%02x" % bgc_dark
    PARAMS["hl_bg"] = '#ffe785'  # highlight background color


# pylint: disable=global-statement
def set_root(root):
    """Set root objet"""
    global PARAMS
    PARAMS["root"] = root


def set_system():
    global PARAMS
    PARAMS["sys"] = platform.system()


# pylint: disable=global-statement
def set_tabs(tabs):
    """Set validate shared meory"""
    global VALIDATE
    for tabname in tabs:
        VALIDATE[tabname] = 0


# pylint: disable=global-statement
def tab_validated(tabname, value):
    """Set validate shared meory"""
    global VALIDATE
    VALIDATE[tabname] = value


# pylint: disable=global-statement
def load_icons():
    """Load icons.

    Load all ./otinker_images/*_icon.gif as icons

    Returns :
    ---------
    load_icons : dictionnary of ImageTk objects
    """
    global IMAGE_DICT
    icons_dir = os.path.join(BASE_DIR, "images")
    icons_pattern = "_icon.gif"
    icons_files = glob("%s/*%s" % (icons_dir, icons_pattern))
    icons = dict()
    for k in icons_files:
        key = os.path.basename(k).replace(icons_pattern, "")
        im = Image.open(k).convert('RGBA')
        icons[key] = ImageTk.PhotoImage(im)
        IMAGE_DICT[key] = icons[key]
    return icons


# pylint: disable=too-many-ancestors
class SwitchForm(ttk.Frame):
    """Overriden Frame class to mimick notebooks without tabs."""

    def add(self, item_id, title=None):
        label_frame = ttk.LabelFrame(
            self, text=title, relief="sunken",
        )
        label_frame.id = item_id  # added attribute
        self.sf_raise(item_id)
        return label_frame

    def sf_del(self, item_id):
        """Destroy tab_id tab."""
        for child_widget in self.winfo_children():
            if child_widget.id == item_id:
                child_widget.destroy()

    def sf_raise(self, item_id):
        """Forget current view and repack tab_name tab."""
        for child_widget in self.winfo_children():
            if child_widget.id == item_id:
                child_widget.pack(fill="both")
            else:
                child_widget.pack_forget()


class MouseScrollableFrame(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pack(side="top", fill="both", expand=True)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        self.canvas = Tk_Canvas(
            self,
            background=PARAMS["bg_lbl"],
            highlightbackground=PARAMS["bg_lbl"],
            highlightcolor=PARAMS["bg_lbl"],
        )

        self.canvas.configure(width=1000, height=300)

        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical",
                                         command=self.canvas.yview)
        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal",
                                         command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        self.canvas.grid(row=0, column=0, sticky="news")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x.grid(row=1, column=0, sticky="we")

        # bind frame (allow scroll behavior in all tabs)
        self._bind_scroll_activation()

    def _bind_scroll_activation(self):
        self.canvas.bind('<Enter>', self._bind_scroll)
        self.canvas.bind('<Enter>', self._bind_global_scroll_event, add='+')
        self.canvas.bind('<Leave>', self._unbind_scroll)
        self.canvas.bind('<Leave>', self._unbind_global_scroll_event, add='+')

    def _bind_global_scroll_event(self, *args):
        self.canvas.bind_all('<<bind_global_scroll>>', self._bind_global_scroll)
        self.canvas.bind_all('<<unbind_global_scroll>>', self._unbind_global_scroll)

    def _unbind_global_scroll_event(self, *args):
        self.canvas.unbind_all('<<bind_global_scroll>>')
        self.canvas.unbind_all('<<unbind_global_scroll>>')

    def _bind_global_scroll(self, event):
        if is_hierarchically_above(event.widget, self.canvas):
            self._bind_scroll_y()

    def _unbind_global_scroll(self, event):
        if is_hierarchically_above(event.widget, self.canvas):
            self._unbind_scroll_y()

    def _bind_scroll_y(self):
        if PARAMS['sys'] == 'Linux':
            self.canvas.bind_all("<4>", self._on_mouse_wheel)
            self.canvas.bind_all("<5>", self._on_mouse_wheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _bind_scroll_x(self):
        if PARAMS['sys'] == 'Linux':
            self.canvas.bind_all("<Shift-Button-4>", self._on_shift_mouse_wheel)
            self.canvas.bind_all("<Shift-Button-5>", self._on_shift_mouse_wheel)
        else:
            self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mouse_wheel)

    def _unbind_scroll_y(self):
        if PARAMS['sys'] == 'Linux':
            self.canvas.unbind_all("<4>")
            self.canvas.unbind_all("<5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")

    def _unbind_scroll_x(self):
        if PARAMS['sys'] == 'Linux':
            self.canvas.unbind_all("<Shift-Button-4>")
            self.canvas.unbind_all("<Shift-Button-5>")
        else:
            self.canvas.unbind_all("<Shift-MouseWheel>")

    def _bind_scroll(self, *args):
        self._bind_scroll_y()
        self._bind_scroll_x()

    def _unbind_scroll(self, *args):
        self._unbind_scroll_y()
        self._unbind_scroll_x()

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(self._get_delta(event), "units")

    def _on_shift_mouse_wheel(self, event):
        self.canvas.xview_scroll(self._get_delta(event), "units")

    def _get_delta(self, event):
        delta = -1 * event.delta if PARAMS['sys'] != 'Linux' else -1
        if PARAMS['sys'] == 'Windows':
            delta /= 120

        if PARAMS['sys'] == 'Linux' and event.num == 5:
            delta *= -1

        return delta


# pylint: disable=too-many-arguments
class TextConsole:
    """ Text widget with search and auto -refresh capabilities."""

    def __init__(
        self,
        holder,
        content,
        height=None,
        width=None,
        search=False,
        disabled=True,
    ):
        """Startup class.

        holder : Tkwidget where to pack the text
        content: Tkstring to display in the widget"""
        self.content = content
        self.disabled = disabled
        self.container = ttk.Frame(holder, relief="sunken")
        self.container.pack(fill="both",)
        self.controls = ttk.Frame(self.container)
        self.body = ttk.Frame(self.container,)
        if search:
            self.controls.pack(fill="x", side="top")
        self.body.pack(fill="x", side="bottom", padx=2, pady=2)
        if disabled:
            bg_color = PARAMS["bg"]
        else:
            bg_color = "white"
        self.txt = ScrolledText(
            self.body,
            background=bg_color,
            highlightbackground=PARAMS["bg_lbl"],
        )
        if height is not None:
            self.txt.configure(height=height)
        if width is not None:
            self.txt.configure(width=width)
        self.txt.pack(fill="both")
        self.search_var = Tk_Variable()
        self.search_lbl = ttk.Label(self.controls, text="Search")
        self.search_ent = ttk.Entry(
            self.controls, textvariable=self.search_var
        )
        self.search_lbl.pack(side="right")
        self.search_ent.pack(side="right")

        self.update()
        self.search_var.trace("w", self.highlight_pattern)
        self.content.trace("w", self.update)

    def update(self, *args):
        """Update the content"""
        self.txt.configure(state="normal")
        self.txt.delete(0.0, "end")
        self.txt.insert(0.0, self.content.get())
        if self.disabled:
            self.txt.configure(state="disabled")
        self.highlight_pattern()

    def highlight_pattern(self, *args):
        """Highlight the pattern."""
        self.txt.tag_delete("highlight")
        self.txt.mark_set("insert", 1.0)
        self.txt.mark_set("matchStart", 1.0)
        self.txt.mark_set("matchEnd", 1.0)
        self.txt.mark_set("searchLimit", "end")
        count = tk.StringVar()
        pattern = self.search_var.get()
        if pattern:
            while True:
                index = self.txt.search(
                    self.search_var.get(),
                    "matchEnd",
                    "searchLimit",
                    count=count,
                    regexp=True,
                )
                if index == "":
                    break
                if count.get() == 0:
                    break
                self.txt.mark_set("matchStart", index)
                self.txt.mark_set("insert", index)
                self.txt.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.txt.tag_add("highlight", "matchStart", "matchEnd")
        self.txt.tag_config("highlight", background="yellow")
        self.txt.see("insert")

    def get(self):
        """Get the content"""
        return self.txt.get("1.0", "end")


def is_hierarchically_above(ref_widget, widget):

    found = False
    parent = ref_widget
    while not found:

        if parent is None:
            break

        if parent == widget:
            found = True

        parent = parent.master

    return found


def create_description(parent, description, size=0.9, side='top', **kwargs):
    """Interpret the description to take into account font modifiers.
    """
    text = description
    fontname, fontsize, fonthyphen = None, 13, "normal"

    if "<small>" in text:
        text = text.replace("<small>", "")
        fontsize = 12
    elif "<tiny>" in text:
        text = text.replace("<tiny>", "")
        fontsize = 11

    if "<bold>" in text:
        text = text.replace("<bold>", "")
        fonthyphen = "bold"

    if "<italic>" in text:
        text = text.replace("<italic>", "")
        fonthyphen = "italic"

    desc = ttk.Label(
        parent,
        text=text,
        wraplength=int(size * WIDTH_UNIT),
        font=(fontname, fontsize, fonthyphen))
    desc.pack(side=side, **kwargs)

    return desc


def cmp_dict_values(entry1, entry2):
    """Recursively compares dict values.

    Notes:
        Assumes both dicts have the same keys.
    """
    def cmp_values(val1, val2):
        if entry1 == entry2:
            return True
        else:
            return False

    if type(entry1) is not dict:
        return cmp_values(entry1, entry2)

    for key in entry1.keys():
        if type(entry1[key]) is dict:
            equal = cmp_dict_values(entry1[key], entry2[key])
            if not equal:
                return False
        else:
            return cmp_values(entry1[key], entry2[key])

    return True
