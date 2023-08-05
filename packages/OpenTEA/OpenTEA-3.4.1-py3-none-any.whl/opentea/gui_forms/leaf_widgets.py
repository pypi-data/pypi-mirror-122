"""
Leaf widgets :
==============

Leaves are the lower part to the graph,
at the tip of the branches.
Most of these widget are entries.

Entries:
--------

The generic node EntryNode is the basis for all
single line inputs:

 - numbers
 - integers
 - strings

Additionnal content can be shown to give info
in the case of validation rules.

Booleans:
---------

This is tranlated to a single Checkbox

Choices:
--------

The choice widget corresponds to the Schema enum property.
This is tranlated to radiobuttons in the form.

FleBrowser:
-----------

This special entry check that the content is a file,
and add a browsing dialog to select the file.

Documentation and Description (DEPRECATED):
-------------------------------------------

Kept fo backward compatibility,
docuementation and descriptions are wats to display strings
in the forms.

Prefer now the documentation and description attributes
in the blocks.

Comments:
---------

Comments are multiline textfields
They can also be usefull for feedbach in disabled mode.

Lists:
------

List corresponds to arrays of parameters,
shown aslist of entries.
These list cannot take dependency links for the moments.

Without a fixed dimension,
specified with "MaxItemns" and "MinItems" attributes in the SCHEMA,
a +/- dialog is shown to extend or crop the list.

"""

import os
import operator
import abc

import tkinter
from tkinter import (ttk,
                     Variable,
                     StringVar,
                     BooleanVar,
                     Toplevel,
                     Text,
                     Entry,
                     Listbox,
                     filedialog,
                     Menu)

from nob import Nob

from opentea.gui_forms.constants import (
    PARAMS,
    WIDTH_UNIT,
    LINE_HEIGHT,
    IMAGE_DICT,
    GetException,
    SetException,
    TextConsole,
    create_description)


# pylint: disable=too-few-public-methods
class LeafWidget():
    """Factory for OpenTea Widgets."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        holder_nlines : integer
            custom number of lines for holder
        """
        self.tree = dict()
        self.status = 1
        self.schema = schema

        self._title = schema.get("title", f'#{name}')
        self.state = schema.get("state", "normal")

        self._holder = ttk.Frame(root_frame,
                                 name=name,
                                 width=WIDTH_UNIT,
                                 height=LINE_HEIGHT)
        if self.state != "hidden":
            self._holder.pack(side="top", fill="x")

        self._label = ttk.Label(self._holder, text=self._title,
                                wraplength=int(0.5 * WIDTH_UNIT))
        self._label.place(relx=0.5, rely=1., anchor="se")

        if "description" in schema:
            self._desc = create_description(root_frame, schema['description'],
                                            size=1, side='top')

    def get_status(self):
        """Return current attribute self.status."""
        return self.status


class OTHidden(LeafWidget):

    def __init__(self, schema, root_frame, name):
        if "description" in schema:
            del schema['description']
        super().__init__(schema, root_frame, name)
        self._holder.forget()

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


# pylint: disable=no-member
class _OTEntry(LeafWidget):
    """Factory for OpenTea Entries."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        self._inits_entry()

    def _inits_entry(self):
        """Initialise entry."""
        self.tkvar = Variable()
        self._entry = Entry(self._holder,
                            textvariable=self.tkvar,
                            borderwidth=0,
                            exportselection=False)

        if self.state == "disabled":
            self._entry.configure(
                highlightbackground=PARAMS["bg"],
                disabledbackground=PARAMS["bg"],
                disabledforeground=PARAMS["bg_dark"],
                state="disabled")

        self._entry.bind('<KeyRelease>', self.memory_change)
        self._entry.bind('<FocusIn>', self.on_focus)

        self._entry.place(relx=0.5, rely=1., anchor="sw")

    def on_focus(self, *args):
        self.previous_value = self.tkvar.get()

    def memory_change(self, *args):
        """Trigger virtual event on mermory change."""
        cur_value = self.tkvar.get()

        if self.state == "normal" and self.previous_value != cur_value:
            self.previous_value = cur_value
            self.highlight_background_color()
            self._entry.event_generate('<<mem_change>>')

    def highlight_background_color(self):
        self._entry.configure(background=PARAMS['hl_bg'])

    def reset_background_color(self):
        self._entry.configure(background='white')


class _OTNumericEntry(_OTEntry):
    def __init__(self, schema, root_frame, name):
        super().__init__(schema, root_frame, name)
        if self.state != "disabled":
            self._config_status_label()

    def _config_status_label(self):
        # change size and re-place
        self._holder.config(height=2 * LINE_HEIGHT)
        self._entry.place(relx=0.5, rely=0.5, anchor="sw")
        self._label.place(relx=0.5, rely=0.5, anchor="se")

        self._status_lbl = ttk.Label(self._holder, text="no status yet",
                                     style='Status.TLabel', compound='left')

        self.tkvar.trace('w', self._update_status_callback)
        self._bounds = [None] * 2
        self._exclusive_bounds = [False] * 2

        if "maximum" in self.schema:
            self._bounds[1] = self.schema['maximum']
            if "exclusiveMaximum" in self.schema:
                self._exclusive_bounds[1] = self.schema["exclusiveMaximum"]
        if "minimum" in self.schema:
            self._bounds[0] = self.schema['minimum']
            if "exclusiveMinimum" in self.schema:
                self._exclusive_bounds[0] = self.schema["exclusiveMinimum"]

        self._status_lbl.place(relx=1., rely=0.5, anchor="ne")

    def _update_status_callback(self, *args):
        """Redirect upon status callback."""
        self.status = 1
        self._status_lbl.config(text='', image='')
        status = ""
        try:
            status = self._boundedvalue()
            if status:
                raise GetException

        except GetException:
            if not status:
                status = 'Invalid input "%s"' % (self._entry.get())
            self._status_lbl.config(
                text=status, image=IMAGE_DICT['invalid'])
            self.status = -1

    def _boundedvalue(self):
        """Validate rules on entries."""
        value = self.get()
        error_msg = str()

        str_operators = ['>', '<']
        operators = [operator.ge, operator.le]
        for i in range(2):
            if self._bounds[i] is not None:
                if operators[i](value, self._bounds[i]):
                    if self._exclusive_bounds[i]:
                        if value == self._bounds[i]:
                            error_msg = (
                                'Invalid :%s %s' % (str_operators[i],
                                                    str(self._bounds[i])))
                else:
                    error_msg = (
                        'Invalid:%s= %s' % (str_operators[i],
                                            str(self._bounds[i])))
                    if self._exclusive_bounds[i]:
                        error_msg = (
                            'Invalid %s %s' % (str_operators[i],
                                               str(self._bounds[i])))
        return error_msg


class OTInteger(_OTNumericEntry):
    """OTinteger variable."""

    def get(self):
        """Return python integer."""
        try:
            out = int(self.tkvar.get())
        except ValueError:
            raise GetException()
        return out

    def set(self, value):
        """Set integer to widget."""
        try:
            int_val = int(value)
            self.tkvar.set(int_val)
            # self._entry.event_generate('<<mem_change>>')
        except ValueError:
            raise SetException()


class OTString(_OTEntry):
    """OTinteger variable."""

    def get(self):
        """Return python integer."""
        try:
            out = str(self.tkvar.get())
        except ValueError:
            raise GetException()
        return out

    def set(self, value):
        """Set integer to widget."""
        try:
            str_val = str(value)
            self.tkvar.set(str_val)
            # self._entry.event_generate('<<mem_change>>')
        except ValueError:
            raise SetException()


class OTNumber(_OTNumericEntry):
    """OTNumber floats."""

    def get(self):
        """Return python integer."""
        try:
            out = float(self.tkvar.get())
        except ValueError:
            raise GetException()
        return out

    def set(self, value):
        """Set integer to widget."""
        try:
            float_val = float(value)
            self.tkvar.set(float_val)
            # self._entry.event_generate('<<mem_change>>')
        except ValueError:
            raise SetException()


class OTBoolean(LeafWidget):
    """OT booleans."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        self.tkvar = BooleanVar()
        self._label.place(relx=0.5, rely=0.5, anchor="e")
        self._cbutt = ttk.Checkbutton(self._holder,
                                      variable=self.tkvar,
                                      command=self._callback_bool)
        self._cbutt.place(relx=0.5, rely=0.5, anchor="w")

    def get(self):
        """Return python boolean."""
        try:
            value = int(self.tkvar.get())
            out = bool(value)
        except ValueError:
            raise GetException()
        return out

    def set(self, value):
        """Set boolean to widget."""
        try:
            self.tkvar.set(value)
        except ValueError:
            raise SetException()

    def _callback_bool(self):
        """Event emission on radio change."""
        self._cbutt.event_generate('<<mem_change>>')
        self.highlight_background_color()

    def highlight_background_color(self):
        self._label.configure(style='Highlighted.TLabel')

    def reset_background_color(self):
        self._label.configure(style='TLabel')


class OTChoiceAbstract(LeafWidget, metaclass=abc.ABCMeta):

    def __init__(self, schema, root_frame, name):
        super().__init__(schema, root_frame, name)
        self.tkvar = StringVar()
        self._label.place(relx=0.5, rely=1, anchor="se")
        self.previous_value = None

    def _callback_choice(self, *args):
        """Reaction to option change."""
        value = self.get()
        if value != self.previous_value:
            self.highlight_background_color()
            self.previous_value = value
            self._holder.event_generate('<<mem_change>>')

    def get(self):
        """Return python string."""
        out = self.tkvar.get()
        return out

    def set(self, value):
        """Set choice to widget."""
        self.previous_value = value
        self.tkvar.set(value)


class OTChoiceRadio(OTChoiceAbstract):
    """OT choices widget."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        self.rad_btns = {}
        self._pack_with_radiobuttons()

    def _pack_with_radiobuttons(self):
        """Radiobutton version of the widget"""
        n_lines = max(len(self.schema["enum"]), 1)
        self._holder.config(height=n_lines * LINE_HEIGHT)
        rel_step = 1. / n_lines
        current_rely = 1 * rel_step

        self._label.place(relx=0.5, rely=current_rely, anchor="se")

        titles = self.schema.get('enum_titles', self.schema["enum"])

        for value, title in zip(self.schema["enum"], titles):
            rad_btn = ttk.Radiobutton(
                self._holder,
                text=title,
                value=value,
                variable=self.tkvar,
                command=self._callback_choice)
            rad_btn.place(
                relx=0.5,
                rely=current_rely,
                anchor="sw")
            self.rad_btns[value] = rad_btn
            current_rely += rel_step

    def highlight_background_color(self):
        val = self.get()
        for name, rad_btn in self.rad_btns.items():
            if name == val:
                rad_btn.configure(style='Highlighted.TRadiobutton')
            else:
                rad_btn.configure(style='TRadiobutton')

    def reset_background_color(self):
        for rad_btn in self.rad_btns.values():
            rad_btn.configure(style='TRadiobutton')


class OTChoiceCombo(OTChoiceAbstract):
    """OT choices widget."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        options = schema.get("enum", None)
        if options:  # in case it is dynamic
            self._pack_with_combobox(options)

    def _pack_with_combobox(self, option):
        """Combobox version of the widget"""
        self.combo = ttk.Combobox(
            self._holder,
            values=option,
            textvariable=self.tkvar,
            state='readonly')
        self.combo.place(relx=0.5, rely=1, anchor="sw")
        self.combo.bind('<<ComboboxSelected>>', self._callback_choice)

    def highlight_background_color(self):
        self.combo.configure(style='Highlighted.TCombobox')

    def reset_background_color(self):
        self.combo.configure(style='TCombobox')


class OTChoiceDynamic(OTChoiceCombo):

    def set(self, value):
        """Set choice to widget."""
        tree = Nob(PARAMS["root"].get())
        key = self.schema["ot_dyn_choice"]
        options = tree[key][:]
        self._pack_with_combobox(options)

        super().set(value)


class OTFileBrowser(LeafWidget):
    """OT file/folder browser widget."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        self.tkvar = StringVar()
        self._filter = []
        self._isdirectory = False
        if 'ot_filter' in schema:
            filters = schema['ot_filter']
            if 'directory' in filters:
                self._isdirectory = True
            else:
                for ext in filters:
                    filetype = ("%s files" % ext, "*.%s" % (ext))
                    self._filter.append(filetype)

        self._label.place(relx=0.5, rely=0.5, anchor="e")

        self._path = ttk.Entry(self._holder,
                               textvariable=self.tkvar,
                               state='disabled',
                               foreground='black')
        self._path.place(relx=0.5, rely=0.5, relwidth=0.4, anchor="w")

        self._btn = ttk.Button(self._holder,
                               image=IMAGE_DICT['load'],
                               width=0.1 * WIDTH_UNIT,
                               compound='left',
                               style='clam.TLabel',
                               command=self._browse)

        self._btn.place(relx=0.9, rely=0.5, anchor="w")

    def _browse(self, event=None):
        """Browse directory or files."""
        cur_path = self.tkvar.get()
        if self._isdirectory:
            path = filedialog.askdirectory(title=self._title)
        else:
            path = filedialog.askopenfilename(title=self._title,
                                              filetypes=self._filter)

        if path == "":
            return

        path = os.path.relpath(path)
        if path != cur_path:
            self.tkvar.set(path)
            self.memory_change()

    def memory_change(self):
        self.highlight_background_color()
        self._holder.event_generate('<<mem_change>>')

    def highlight_background_color(self):
        self._path.configure(style='Highlighted.TEntry')

    def reset_background_color(self):
        self._path.configure(style='TEntry')

    def get(self):
        """Return data."""
        return self.tkvar.get()

    def set(self, value):
        """Set content."""
        self.tkvar.set(value)


class OTDocu(LeafWidget):
    """OTinteger variable."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        self.tkvar = StringVar()
        self._btn = ttk.Button(self._holder,
                               width=0.01 * WIDTH_UNIT,
                               compound='center',
                               image=IMAGE_DICT['docu'],
                               style='clam.TLabel',
                               command=self._popup_dialog)
        self._btn.place(relx=0.9, rely=0.5, anchor="center")
        self._holder.pack_configure(side="bottom", fill="x")

        self.parent = root_frame

        while self.parent.master is not None:
            self.parent = self.parent.master

        self._dialog = None

    def _popup_dialog(self):
        """Display content of documentation string."""
        self._dialog = Toplevel(self.parent)
        self._dialog.transient(self.parent)
        self._dialog.title('Documentation')
        self._dialog.grab_set()

        self._dialog.bind("<Control-w>", self._destroy_dialog)
        self._dialog.bind("<Escape>", self._destroy_dialog)
        self._dialog.protocol("WM_DELETE_WINDOW", self._destroy_dialog)

        dlg_frame = ttk.Frame(self._dialog,
                              width=3 * WIDTH_UNIT,
                              height=3 * WIDTH_UNIT)
        dlg_frame.pack(side="top", fill="both", expand=True)
        dlg_frame.grid_propagate(False)
        dlg_frame.grid_rowconfigure(0, weight=1)
        dlg_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(dlg_frame)
        scrollbar.pack(side='right', fill='y')

        text_wd = Text(
            dlg_frame,
            wrap='word',
            yscrollcommand=scrollbar.set,
            borderwidth=0.02 * WIDTH_UNIT,
            relief="sunken")

        # Example of formatting
        text_wd.tag_configure('bold', font=('Times', 14, 'normal'))
        text_wd.insert("end", self.tkvar, 'bold')
        text_wd.config(state='disabled')
        text_wd.pack()
        scrollbar.config(command=text_wd.yview)

    def _destroy_dialog(self, event=None):
        """Destroying dialog."""
        self.parent.focus_set()
        self._dialog.destroy()
        self._dialog = None

    def get(self):
        """Void return."""
        return None

    def set(self, value):
        """Set value to documentation content."""
        self.tkvar.set(value)


class OTDescription(LeafWidget):
    """OT descriptin field."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        self.tkvar = StringVar()
        self._holder.pack_configure(side="bottom", fill="x")

        self._label.config(justify="left",
                           textvariable=self.tkvar,
                           wraplength=WIDTH_UNIT * 0.8)
        self._label.pack(side="bottom")

    def get(self):
        """Return data."""
        return None

    def set(self, value):
        """Set content."""
        self.tkvar.set(value)


class OTComment(LeafWidget):
    """OT Comment field."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        self.tkvar = StringVar()
        self._holder.pack_configure(side="top", fill="x")
        disabled = False
        height = 6
        if "state" in schema:
            if schema["state"] == "disabled":
                disabled = True

        if "height" in schema:
            height = schema["height"]

        self.txt = TextConsole(self._holder,
                               self.tkvar,
                               height=height,
                               width=10,
                               disabled=disabled)
        self._holder.bind('<Enter>', self._unbind_global_scroll)
        self._holder.bind('<Leave>', self._bind_global_scroll)

    def _bind_global_scroll(self, *args):
        self._holder.event_generate('<<bind_global_scroll>>')

    def _unbind_global_scroll(self, *args):
        self._holder.event_generate('<<unbind_global_scroll>>')

    def get(self):
        """Return data."""
        # self.tkvar.set(self.txt.get())
        return self.tkvar.get()

    def set(self, value):
        """Set content."""
        self.tkvar.set(value)
        self.txt.update()


class OTEmpty(LeafWidget):
    """OT widget for unimplemented types."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)

        info = []
        for item in ["name", "title", "type", "ot_type"]:
            if item in schema:
                info.append(item + " = " + str(schema[item]))

        self._label.configure(text="\n".join(info))
        self._label.pack(side="top", padx=2, pady=2)
        # hide void strings for empty objects
        if "ot_type" in schema:
            if schema["ot_type"] == "void":
                self._holder.forget()

    def get(self):
        """Return data."""
        return None

    def set(self, *args, **kwargs):
        """Set content."""
        pass


class OTAbstractList(LeafWidget, metaclass=abc.ABCMeta):

    def __init__(self, schema, root_frame, name):
        super().__init__(schema, root_frame, name)
        self.variable = list()
        self.entrylistholder = ttk.Frame(self._holder)
        self.entrylistholder.place(relwidth=0.5,
                                   relx=0.5,
                                   rely=0.0, anchor="nw")
        self._configure_popup_menu()

    def _configure_popup_menu(self):
        self.popup_menu = Menu(self.entrylistholder, tearoff=False)  # binding in tv bindings

        self._add_popup_commands()

        self.entrylistholder.bind('<Enter>', self._activate_popup)
        self.entrylistholder.bind('<Leave>', self._deactivate_popup)

    @abc.abstractmethod
    def _add_popup_commands(self):
        pass

    def _activate_popup(self, *args):
        self.entrylistholder.bind_all("<Button-2>", self.on_right_click)

    def _deactivate_popup(self, *args):
        self.entrylistholder.unbind_all("<Button-2>")

    def on_right_click(self, event):
        self.popup_menu.tk_popup(event.x_root, event.y_root)

    def on_copy(self, *args):
        copy_str = ', '.join([str(value) for value in self.get()])
        PARAMS['root']._root.clipboard_clear()
        PARAMS['root']._root.clipboard_append(copy_str)

    def get(self):
        """Return data."""
        return self.variable

    def set(self, value):
        """Set content."""
        self.variable = list(value)
        self._update_entrylist()

    def _resize_holder(self, n_lines):
        self._holder.config(height=n_lines * LINE_HEIGHT)

    def _update_entrylist(self):
        pass


class OTList(OTAbstractList):
    """Factory for OpenTea Lists."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        self.empty_widget = None
        self.entrywidgets = list()
        self.entrywidgets_tkvars = list()
        self.item_type = schema["items"]["type"]
        self.item_default = schema["items"]["default"]
        self.resizable = self._is_resizable()
        self._config_status_label()

        if self.resizable:
            self._config_buttons()

    def _is_resizable(self):
        if "minItems" in self.schema or "maxItems" in self.schema:
            return False

        return True

    def _config_status_label(self):
        self._status_lbl = ttk.Label(
            self._holder, text="no status yet", style='Status.TLabel',
            compound='left')
        relx = 0.9 if self.resizable else 1.
        self._status_lbl.place(relx=relx, rely=1.0, anchor="se")

    def _config_buttons(self):
        """Initialise entry."""
        self.additem_bt = ttk.Button(self._holder,
                                     text="+",
                                     command=self.on_additem)
        self.delitem_bt = ttk.Button(self._holder,
                                     text="-",
                                     command=self.on_delitem)

        self.additem_bt.place(relwidth=0.05,
                              relx=0.95,
                              rely=1.0, anchor="se")
        self.delitem_bt.place(relwidth=0.05,
                              relx=1,
                              rely=1.0, anchor="se")

    def _add_popup_commands(self):
        self.popup_menu.add_command(label='Copy', command=self.on_copy)
        self.popup_menu.add_command(label='Paste', command=self.on_paste)

    def on_paste(self, *args):
        changed = False
        try:
            paste_str = PARAMS['root']._root.clipboard_get()
        except tkinter._tkinter.TclError:
            print('Nothing to paste')
            return

        paste_ls = [value.strip() for value in paste_str.split(',')]

        if not self.resizable and len(paste_ls) != len(self.entrywidgets):
            print('Sizes do not match')
            return

        if not self.resizable:
            changed = self._update_items(paste_ls)

        else:
            n_vars = len(self.variable)
            n_paste_elems = len(paste_ls)

            # delete excess items
            if n_vars > n_paste_elems:
                changed = True
                for _ in range(n_vars - n_paste_elems):
                    self._delete_item()

            # update existing items
            updated = self._update_items(paste_ls)
            if updated:
                changed = True

            # add new items
            for value in paste_ls[n_vars:]:
                changed = True
                self._add_item(value)

        if changed:
            self._trigger_mem_change()

    def _resize_holder(self):
        n_lines = max(2, 1 + len(self.variable))
        if self.resizable:
            n_lines += 0.5  # otherwise buttons overlap last entry
        super()._resize_holder(n_lines)

    def _update_entrylist(self):
        self._resize_holder()

        self.clear_entrywidgets()
        if len(self.variable) == 0:
            self.create_void_entry()
        else:
            self.clear_empty_widget()
            for value in self.variable:
                self.add_new_entry(value)

    def add_new_entry(self, value):
        tkvar = Variable()
        tkvar.trace('w', self._single_entry_callback)

        entry = ttk.Entry(self.entrylistholder, textvariable=tkvar,
                          exportselection=False)
        entry.pack(side="top")
        entry.bind("<KeyRelease>", self.memory_change)
        entry.bind('<FocusIn>', self.on_entry_focus)

        self.entrywidgets.append(entry)
        self.entrywidgets_tkvars.append(tkvar)

        tkvar.set(value)  # update only after list updates

    def create_void_entry(self):
        if self.empty_widget is not None:
            return

        label = ttk.Label(self.entrylistholder, text="void")
        label.pack(side="top")
        self.empty_widget = label

    def clear_empty_widget(self):
        if self.empty_widget is None:
            return

        self.empty_widget.destroy()
        self.empty_widget = None

    def clear_entrywidgets(self, n_items=None):
        if n_items is None:
            n_items = len(self.entrywidgets)
        i = 0
        while i < n_items:
            self.entrywidgets.pop().destroy()
            self.entrywidgets_tkvars.pop()
            i += 1

    def _trigger_mem_change(self):
        self.entrylistholder.event_generate('<<mem_change>>')

    def memory_change(self, event):
        """Trigger virtual event on memory change."""
        cur_value = event.widget.get()

        if cur_value != self.previous_value:
            self.previous_value = cur_value
            self.highlight_background_color(event.widget)
            self._trigger_mem_change()

    def on_entry_focus(self, event):
        value = event.widget.get()
        self.previous_value = value
        self._update_status(value)

    def highlight_background_color(self, widget):
        # color comes back to normal automalically (new widgets are created)
        widget.configure(style='Highlighted.TLabel')

    def on_additem(self):
        """Add an item at the end of the array."""
        value = self.item_default
        self._add_item(value)
        self._trigger_mem_change()

    def on_delitem(self):
        """Delete item at the end of the array"""
        self._delete_item()

        self._trigger_mem_change()

    def _add_item(self, value):
        self.variable.append(value)
        self._resize_holder()
        self.clear_empty_widget()
        self.add_new_entry(value)

        self.highlight_background_color(self.entrywidgets[-1])

    def _delete_item(self):
        if not self.variable:
            return

        self._status_lbl.config(text='', image='')
        self.clear_entrywidgets(1)
        self.variable.pop()
        self._resize_holder()
        if len(self.variable) == 0:
            self.create_void_entry()

    def _update_items(self, new_items):
        changed = False
        for widget, tkvar, previous_value, value in zip(
                self.entrywidgets, self.entrywidgets_tkvars,
                self.variable, new_items):
            if str(previous_value) != str(value):
                changed = True
                tkvar.set(value)
                self.highlight_background_color(widget)

        return changed

    def _get_entry_tkvar_index(self, var_name):
        var_names = [var._name for var in self.entrywidgets_tkvars]
        return var_names.index(var_name)

    def _validate_single_entry(self, value):
        try:
            if self.item_type == "number":
                value = float(value)
            elif self.item_type == "integer":
                value = int(value)
            return value, True
        except ValueError:
            return value, False

    def _single_entry_callback(self, var_name, *args):
        """Send the content of the list bact to the variable."""
        entry_index = self._get_entry_tkvar_index(var_name)
        value = self.entrywidgets_tkvars[entry_index].get()

        value, valid = self._validate_single_entry(value)

        # if valid repeat validation for other cases (for multiple errors)
        value = self._update_status(value)

        # update variables
        if len(self.variable) < entry_index - 1:
            self.variable.append(value)
        else:
            self.variable[entry_index] = value

    def _update_status(self, value):
        value, valid = self._validate_single_entry(value)

        # first validation here to ensure updated msg for selected entry
        if not valid:
            self.status = -1
            self._status_lbl.config(
                text=f'Invalid input "{value}"',
                image=IMAGE_DICT['invalid'])
            return value

        # check other entries for errors (for multiple errors)
        n_err = self._get_number_of_errors()
        if n_err == 0:
            self.status = 1
            self._status_lbl.config(text='', image='')
        else:
            self.status = -1
            self._status_lbl.config(
                text=f'Contains {n_err} invalid input(s)',
                image=IMAGE_DICT['invalid'])

        return value

    def _get_number_of_errors(self):
        c = 0
        for tkvar in self.entrywidgets_tkvars:
            value = tkvar.get()
            value, valid = self._validate_single_entry(value)
            if not valid:
                c += 1
        return c


class OTListStatic(OTAbstractList):

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        self._configure_listbox()

    def _configure_listbox(self):
        nlines = 6
        self._resize_holder(nlines)

        scrollbar = ttk.Scrollbar(self.entrylistholder, orient='vertical')

        self.lbx = Listbox(
            self.entrylistholder,
            height=nlines,
            yscrollcommand=scrollbar.set)
        self.lbx.configure(
            state="disabled",
            highlightbackground=PARAMS["bg"],
            background=PARAMS["bg"],
            disabledforeground=PARAMS["bg_dark"])

        scrollbar.config(command=self.lbx.yview)
        scrollbar.pack(side='right', fill='y')
        self.lbx.pack(side="top", fill="both", pady=2)
        self.lbx.bind('<Enter>', self._unbind_global_scroll)
        self.lbx.bind('<Leave>', self._bind_global_scroll)

    def _bind_global_scroll(self, *args):
        self.lbx.event_generate('<<bind_global_scroll>>')

    def _unbind_global_scroll(self, *args):
        self.lbx.event_generate('<<unbind_global_scroll>>')

    def _add_popup_commands(self):
        self.popup_menu.add_command(label='Copy', command=self.on_copy)

    def _update_entrylist(self):
        self.lbx.configure(state="normal")

        self.lbx.delete(0, 'end')
        for item in self.variable:
            self.lbx.insert("end", item)

        self.lbx.configure(state="disabled")
