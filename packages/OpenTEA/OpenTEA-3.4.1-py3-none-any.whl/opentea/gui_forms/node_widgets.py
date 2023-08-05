"""
Recursive edicrection according to SCHEMA type
==============================================
This module staets with the recursive redirection
according to SCHEMA types.

Module for containers widgets
=============================

This module take care of all the node elements of the graph,
which correspond to containers in the Form.
At least the three first level of the SCHEMA must be objects,
 and are treated as containers.
 Oll the containers derive from the generic Node-Widget.

The root level:
---------------

The inital node, Not treted here, see root_widget.

The Tab level:
--------------

The second node level. Treated here, see Tabs_widgets.
This one can support two types of callbacks,
either for editing the memory,
or for updating the 3D view.

The Block level :
-----------------

The Thirl level gather parameters into families.
This one can support descriptions, images and documentation.


Special container : The Multiple widget :
-----------------------------------------

This container correspont to an SCHEMA array of objet items.
See it as a list (free or dependent) of similar containers.

Mutliple can be use freely or with a dependency.
In the last case, the items of the multiple is linked to the value
of a string array somewhere else in the SCHEMA.
For exeample, in CFD, This is usefoull for a
set of boundary conditions, found by reading a MESH.


Special container : the XOR widget :
------------------------------------

This is merely a selector between several blocks.
This marks a bifurcation in your graph.
For example in CFD, this is usefull for the selection between
different models taking different parameters.

:warning exception here: XOR is the only node element storing a Value.
The value is implicit : it is *the name of the only child
of the XOR in the memory*.

It could have been designed otherwise, keeping all the children inthe memory,
and a real leaf value to know which one must be taken.
However, thos is impractical here. For example in CFD,
you can have a Multiple of 100 boundary conditions,
with a XOR for each selecting between 30 models of BCs.
Such a graph would be a hassle to read and hack for humans.

"""

# pylint: disable=too-many-lines

import os
import warnings
import copy
from collections import OrderedDict
import yaml

import tkinter as tk
from tkinter import ttk

# from tkinter import Canvas as Tk_Canvas
from tkinter import Menu
from tkinter import Entry, Frame, StringVar, LEFT, filedialog, Toplevel
from tkinter import messagebox
from PIL import ImageTk, Image
import tkhtmlview as tkhtml
import markdown
from nob import Nob

from opentea.noob.inferdefault import nob_complete
from opentea.noob.noob import nob_pprint

# from opentea.gui_forms.wincanvas import redirect_canvas_items
from opentea.gui_forms.constants import (
    IMAGE_DICT,
    WIDTH_UNIT,
    VALIDATE,
    PARAMS,
    tab_validated,
    GetException,
    SetException,
    SwitchForm,
    MouseScrollableFrame,
    is_hierarchically_above,
    create_description,
    cmp_dict_values
)
from opentea.gui_forms.leaf_widgets import (
    OTInteger,
    OTNumber,
    OTEmpty,
    OTList,
    OTListStatic,
    OTChoiceRadio,
    OTChoiceCombo,
    OTChoiceDynamic,
    OTComment,
    OTBoolean,
    OTFileBrowser,
    OTString,
    OTDocu,
    OTDescription,
    LeafWidget,
    OTHidden,
)


def redirect_widgets(schema, root_frame, name, tab):
    """Redirect to widgets.

    The schema attributes trigger which widget will be in use.

    Inputs :
    --------
    schema :  a schema object
    root_frame :  a Tk object were the widget will be grafted
    name : name of the element
    tab:  the tab holding this widget

    Outputs :
    --------
    none
    """

    if schema is None:
        out = OTEmpty(dict(), root_frame, name)
    else:
        if "properties" in schema:
            out = OTContainerWidget(schema, root_frame, name, tab)
        elif "oneOf" in schema:
            out = OTXorWidget(schema, root_frame, name, tab)
        elif "enum" in schema:
            if len(schema["enum"]) > 3:
                out = OTChoiceCombo(schema, root_frame, name)
            else:
                out = OTChoiceRadio(schema, root_frame, name)
        elif "ot_dyn_choice" in schema:
            out = OTChoiceDynamic(schema, root_frame, name)
        elif "type" in schema:
            if schema["type"] == "array":
                if "properties" in schema["items"]:
                    out = OTMultipleWidget(schema, root_frame, name, tab)
                else:
                    state = schema.get('state', 'normal')
                    if state == 'disabled':
                        out = OTListStatic(schema, root_frame, name)
                    else:
                        out = OTList(schema, root_frame, name)
            elif schema["type"] == "integer":
                out = OTInteger(schema, root_frame, name)
            elif schema["type"] == "number":
                out = OTNumber(schema, root_frame, name)
            elif schema["type"] == "boolean":
                out = OTBoolean(schema, root_frame, name)
            elif schema["type"] == "string":
                out = redirect_string(schema, root_frame, name)
            else:
                out = OTEmpty(schema, root_frame, name)
        else:
            out = OTEmpty(schema, root_frame, name)
    return out


def redirect_string(schema, root_frame, name):
    """Redirect to string widgets.

    The schema attributes trigger which string widget will be in use.

    Inputs :
    --------
    schema :  a schema object
    root_frame :  a Tk object were the widget will be grafted
    name : name of the element

    Outputs :
    --------
    none
    """
    if "ot_type" in schema:
        if schema["ot_type"] == "desc":
            wng = " at: " + name + "> attribute"
            wng += "\n ot_type : desc is deprecated"
            wng += "\n prefer description attribute on blocks"
            warnings.warn(wng, DeprecationWarning)
            out = OTDescription(schema, root_frame, name)
        elif schema["ot_type"] == "docu":
            wng = " at: " + name + "> attribute"
            wng += "\n ot_type : docu is deprecated"
            wng += "\n prefer documentation attribute on blocks"
            warnings.warn(wng, DeprecationWarning)
            out = OTDocu(schema, root_frame, name)
        elif schema["ot_type"] == "void":
            out = OTEmpty(schema, root_frame, name)
        elif schema["ot_type"] == "comment":
            out = OTComment(schema, root_frame, name)
        elif schema["ot_type"] == "file":
            out = OTFileBrowser(schema, root_frame, name)
        elif schema["ot_type"] == "hidden":
            out = OTHidden(schema, root_frame, name)
        else:
            raise NotImplementedError(
                "At node"
                + name
                + ": cannot resolve ot_type="
                + schema["ot_type"]
            )
    else:
        out = OTString(schema, root_frame, name)

    return out


class OTNodeWidget:
    """Factory for OpenTea Widgets Containers."""

    def __init__(self, schema):
        """Startup class."""
        self.tree = dict()
        self.sch = schema
        try:
            self.properties = schema["properties"]
        except:
            msg_err = "properties missing in schema:\n" + nob_pprint(schema)
            raise RuntimeError(msg_err)

    def get(self):
        """Get the data of children widgets.

        Returns :
        ---------
        a dictionnary with the get result of childrens
        """
        out = {}
        for child in self.properties:
            try:
                found = self.tree[child].get()
                if found is not None:
                    out[child] = found
            except GetException:
                pass
        if out == {}:
            out = None
        return out

    def set(self, dict_):
        """Get the data of children widgets.

        Input :
        -------
        a dictionnary with the value of the childrens"""
        for child in self.properties:
            try:
                if child in dict_:
                    try:
                        self.tree[child].set(dict_[child])
                    except SetException:
                        pass
            except TypeError:
                print("==========================")
                print("Child not set", child, nob_pprint(self.sch, max_lvl=2))

    def get_status(self):
        """Return the minimal status of children."""
        status = 1
        for child in self.properties:
            status = min(status, self.tree[child].get_status())
        return status


# pylint: disable=too-many-arguments
class OTContainerWidget(OTNodeWidget):
    """OT container widget."""

    def __init__(
        self,
        schema,
        root_frame,
        name,
        tab,
        n_width=1,
        relief="ridge",
        show_title=True,
    ):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        name: string naming the widget
        n_width : float
             relative size of the widget

        """
        super().__init__(schema)
        self.name = name
        title = schema.get('title', "")
        self.tab = tab
        self._holder = ttk.Frame(
            root_frame, relief=relief, width=n_width * WIDTH_UNIT
        )
        self._holder.pack(side="top", padx=0, pady=10)

        if show_title and title:
            self.head = ttk.Label(self._holder, text=title)
            self.head.pack(side="top", fill="x", padx=0, pady=5)
        self.body = ttk.Frame(self._holder, width=n_width * WIDTH_UNIT)

        """Forcing the widget size"""
        self._forceps = ttk.Frame(
            self._holder, width=n_width * WIDTH_UNIT, height=1
        )
        self._forceps = ttk.Frame(self._holder, width=WIDTH_UNIT, height=1)
        self._forceps.pack(side="top", padx=2, pady=2)

        self.expert = False
        self.packed = True
        if "expert" in schema:
            self.expert = schema["expert"]

        if self.expert:
            self.packed = False
            self.head.configure(compound=LEFT, image=IMAGE_DICT["plus"])
            self.head.bind("<Button-1>", self.pack_unpack_body)

        if self.packed:
            self.body.pack(side="top", fill="x", expand=False, padx=2, pady=2)

        if "image" in schema:
            self._img = create_image(schema, self.body)

        if "documentation" in schema:
            self._docu = create_documentation(schema, self.body)

        if "description" in schema:
            self._desc = create_description(self.body, schema["description"],
                                            side='top')

        # CHILDREN
        for name_child in self.properties:
            schm_child = self.properties[name_child]
            self.tree[name_child] = redirect_widgets(
                schm_child, self.body, name_child, tab
            )

    def pack_unpack_body(self, event):
        """swtich on or off the packing of the body"""
        if self.packed:
            self.packed = False
            self.body.pack_forget()
            self.head.configure(compound=LEFT, image=IMAGE_DICT["plus"])
        else:
            self.packed = True
            self.body.pack(
                side="top", fill="x", expand=False, padx=2, pady=2,
            )
            self.head.configure(compound=LEFT, image=IMAGE_DICT["minus"])

        PARAMS["top"].update_idletasks()
        self.tab.smartpacker()


class OTTabWidget(OTNodeWidget):
    """OT Tab widget container.

    Called for the 1st layer of nodes in the global schema
    """

    def __init__(self, schema, root, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root :  the parent
        name: string naming the widget
        """
        super().__init__(schema)
        self.root = root
        self.icon = None
        self.name = name
        self.title = schema.get('title', f'#{name}')

        self._tab = ttk.Frame(self.root.toptabs.nb, name=name)
        self.root.toptabs.nb.add(self._tab, text=self.title)

        self.tabid = self.root.toptabs.nb.index("end") - 1

        # SCROLL FORM
        sframe = MouseScrollableFrame(self._tab)
        self.scan = sframe.canvas
        self.holder = ttk.Frame(self.scan)
        self.scan.create_window((0, 0), window=self.holder, anchor="nw")
        # FOOTER
        _footer_f = ttk.Frame(self._tab)
        _footer_f.pack(side="top", fill="both", padx=2, pady=3)
        self.button_text = StringVar()
        self.button_lb = ttk.Label(
            _footer_f, textvariable=self.button_text, wraplength=2 * WIDTH_UNIT
        )

        self.process = None
        self.update_scene_3d = None

        # self.validated = False

        actions = list()
        if "process" in schema:
            self.process = schema["process"]
            actions.append("Process")
        if "update_scene_3d" in schema:
            self.update_scene_3d = schema["update_scene_3d"]
            actions.append("Update 3D")

        if not actions:
            txt_btn = "Validate"
        else:
            txt_btn = "/".join(actions)

        _button_bt = ttk.Button(
            _footer_f, text=txt_btn, command=self.process_button
        )

        _button_bt.pack(side="right", padx=2, pady=2)
        self.button_lb.pack(side="right", padx=2, pady=2)
        if "description" in schema:
            self._desc = create_description(
                _footer_f, schema["description"], size=1.0, side='left'
            )

        # CHILDREN
        for name_ in schema["properties"]:
            self.tree[name_] = redirect_widgets(
                schema["properties"][name_], self.holder, name_, self
            )

        self.holder.bind("<Configure>", self.smartpacker)

        self.root.toptabs.nb.bind_all(
            "<<mem_check>>", self.on_memory_check, add="+"
        )
        self.root.toptabs.nb.bind_all(
            "<<mem_change>>", self.on_memory_change, add="+"
        )
        self.root.toptabs.nb.bind_all(
            "<<icon_update>>", self.on_icon_update, add="+"
        )
        self.update_tab_icon()

    def smartpacker(self, event=None):
        """Smart grid upon widget size.

        Regrid the object according to the width of the window
        from the inside
        """
        self.scan.configure(scrollregion=self.scan.bbox("all"))
        ncols = max(
            int(self.root.toptabs.nb.winfo_width() / WIDTH_UNIT + 0.5), 1
        )

        large_children = list()
        normal_children = list()
        for child in self.holder.winfo_children():
            if child.winfo_width() > 1.1 * WIDTH_UNIT:
                large_children.append(child)
            else:
                normal_children.append(child)

        height = 0
        x_pos = 10
        y_pos = 10

        max_depth = y_pos

        # Normal children
        max_width = WIDTH_UNIT
        for child in normal_children:
            height += child.winfo_height() + 2
            max_width = max(max_width, child.winfo_width())

        limit_depth = height / ncols

        for child in normal_children:
            child.place(x=x_pos, y=y_pos, anchor="nw")
            y_pos += child.winfo_height() + 10

            max_depth = max(y_pos, max_depth)
            # jump to next column il multicolumn
            if ncols > 1 and y_pos > limit_depth:
                x_pos += max_width + 20
                y_pos = 10

        # Large children
        x_pos = 0
        y_pos = max_depth
        for child in large_children:
            height = child.winfo_height()
            child.place(x=x_pos, y=y_pos, anchor="nw")
            y_pos += height + 2
        max_depth = y_pos

        self.holder.configure(
            height=max_depth + 200, width=ncols * (max_width + 20) + 20
        )

    def process_button(self):
        """Procees the main tab button."""
        self.button_text.set("")
        tab_validated(self.name, 0)

        if self.get_status() == -1:
            self.button_text.set("Cannot process with errors in tabs")
            return

        self.root.toptabs.nb.event_generate("<<mem_check>>")

        # Surprisingly this does not work on all platforms
        # hence the try/except
        # (CCRT COBALT using remote desktop)
        try:
            PARAMS["top"].config(cursor="wait")
            PARAMS["top"].update()
        except tk.TclError:
            pass

        if self.process is None:
            tab_validated(self.name, 1)
        else:
            success, duration, returnstr = self.root.execute(self.process)
            if success:
                self.button_lb.configure(foreground="black")
                self.button_text.set(
                    "Done in " + duration + ", successful"
                )
                self.root.toptabs.nb.event_generate("<<mem_change>>")
                tab_validated(self.name, 1)
            else:
                self.button_lb.configure(foreground="red")
                self.button_text.set(
                    "Failed after " + duration + ", " + returnstr
                )
                tab_validated(self.name, -1)
        self.root.toptabs.nb.event_generate("<<mem_check>>")

        if self.update_scene_3d is None:
            pass
        else:
            self.root.update_3d_view(self.update_scene_3d)
        # Save after update
        self.root.save_project()

        try:
            PARAMS["top"].config(cursor="")
            PARAMS["top"].update()
        except tk.TclError:
            pass

        if VALIDATE[self.name] == 1:
            self.reset_highlighted_bg()

    def update_tab_icon(self):
        """Update the Tab icon upon status."""
        state = self.get_status()

        state_icon = "unknown"

        if state == 1:
            state_icon = "valid"
        if state == -1:
            state_icon = "invalid"

        if self.icon != state_icon:
            self.root.toptabs.nb.tab(
                self.tabid, image=IMAGE_DICT[state_icon], compound="left"
            )
            self.icon = state_icon

    def on_memory_change(self, event):
        """Check if the sender is child of this tab.process.
        set to unknown if so"""
        if is_hierarchically_above(event.widget, self._tab):
            tab_validated(self.name, 0)
            self.update_tab_icon()

    def on_memory_check(self, event):
        """Update content upon status of children."""
        self.update_tab_icon()

    def on_icon_update(self, event):
        """Updates tab icone.

        In some cases it is useful to have a different mean of changing the
        tab icon that is not a <<mem_change>>, as <<mem_change>> also triggers
        other actions.
        """
        self.on_memory_change(event)

    def reset_highlighted_bg(self):
        nodes = []
        get_nodes_with_method(self.tree, 'reset_background_color', nodes)
        for node in nodes:
            node.reset_background_color()

    def get_status(self):
        """Return the minimal status of children."""

        status = 1
        for child in self.properties:
            status = min(status, self.tree[child].get_status())

        status = min(status, VALIDATE[self.name])

        return status


class OTMultipleWidget:
    """OT multiple widget."""

    def __init__(self, schema, root_frame, name, tab):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        name: string naming the widget
        """
        self.tree = dict()  # order is not kept here
        self.tab = tab
        self.status = 1
        self.item_schema = schema["items"]
        # self.item_schema['properties']['name']['state'] = 'disabled'  # disable name
        self.item_schema['properties']['name']['ot_type'] = 'hidden'
        self.schema = schema
        self.name = name
        self.clipboard = None

        title = schema.get('title', f"#{name}")

        self.holder = ttk.LabelFrame(root_frame, text=title, name=name,
                                     relief="sunken", width=2 * WIDTH_UNIT)
        self.holder.pack(side="top", fill="x", padx=2, pady=2, expand=False)
        forceps = ttk.Frame(self.holder, width=2.0 * WIDTH_UNIT, height=1)
        self.tvw = MultipleTreeview(self, self.holder, selectmode="extended",
                                    height=15)

        self.switchform = SwitchForm(
            self.holder, width=WIDTH_UNIT, name="tab_holder")

        self._config_ctrl_panel()

        # grid the main layout
        forceps.grid(column=0, row=1, columnspan=3)
        self.tvw.scrollbar_y.grid(column=1, row=1, sticky="news")
        self.tvw.grid(column=0, row=1, sticky="news")
        self.ctrls.grid(column=0, row=2, sticky="nw")
        self.switchform.grid(column=2, row=1, rowspan=2, sticky="nw")
        self.switchform.grid_propagate(0)

        self.tvw.config_columns()
        self.tvw.config_bindings()

    def _config_ctrl_panel(self):
        self.ctrls = ttk.Frame(self.holder)
        self.ctrls.butt_load = ttk.Button(
            self.ctrls, text="load", command=self.load_from_file
        )
        self.ctrls.butt_load.pack(side="left")
        if "ot_require" not in self.schema:
            self.ctrls.butt_add = ttk.Button(
                self.ctrls, text="add", command=self.add_item_on_cursel
            )
            self.ctrls.butt_del = ttk.Button(
                self.ctrls, text="del", command=self.del_item_on_cursel
            )
            self.ctrls.butt_add.pack(side="left")
            self.ctrls.butt_del.pack(side="left")

            self.ctrls.butt_up = ttk.Button(
                self.ctrls, text="up", command=self.tvw.on_move_up
            )
            self.ctrls.butt_up.pack(side="left")
            self.ctrls.butt_down = ttk.Button(
                self.ctrls, text="down", command=self.tvw.on_move_down
            )
            self.ctrls.butt_down.pack(side="left")

    def trigger_icon_update(self):
        self.tvw.event_generate('<<icon_update>>')

    def check_clipboard(self):
        if self.clipboard is None:
            messagebox.showwarning(message="Nothing to paste")
            self.tvw.focus_set()
            return False

        return True

    def highlight_background_color(self, item_id):
        self.tvw.item(item_id, tags=(self.tvw.highlighted_tag,))

    def reset_background_color(self):
        for item_id in self.tvw.get_children():
            self.tvw.item(item_id, tags=())

    def get(self):
        """Get the data of children widgets.

        Returns :
        ---------
        a list with the get result of childrens
        """
        out = list()
        for key in self.get_ordered_keys():
            child = self.tree.get(key, None)
            if child is None:
                # happens when treeview widget exists, but not in the tree yet
                # so basically during object creation when child ask get.
                raise GetException
            try:
                data = child.get()
                if data is not None:
                    out.append(data)
            except GetException:
                pass

        return out

    def set(self, children):
        """Get the data of children widgets.

        Input :
        -------
        a list with the value of the children

        Notes:
            All the children should be passed (otherwise they'll be deleted).

            Order of existing children is not dependent on list order, new
            children are added orderly after existing.
        """

        # list to dict
        children = OrderedDict([(child['name'], child) for child in children])

        # children to delete
        map_key_to_name = self.get_map_key_to_name()
        for key in list(self.tree.keys()):
            if map_key_to_name[key] not in children:
                self.del_item_by_id(key)

        # update existing objects and create new ones
        map_name_to_key = self.get_map_name_to_key()
        for name, data in children.items():
            if name in map_name_to_key:  # update existing
                self.tree[map_name_to_key[name]].set(data)
            else:  # create new item
                self.add_new_item(data)

    def rename_callback(self, item_id):
        """Trigger renaming if dialog conditions are met."""
        def _withdraw(args):
            trans_frame.destroy()

        def _tryupdate(args):
            self.rename_item(item_id, custom_name.get())
            trans_frame.destroy()

        trans_frame = Frame(self.tvw, background="red", borderwidth=2)
        bbox = self.tvw.bbox(item_id, "#1")
        trans_frame.place(
            x=bbox[0] - 1,
            y=bbox[1] - 1,
            width=bbox[2] + 2,
            height=bbox[3] + 2,
        )

        item_name = self.tree[item_id].name
        custom_name = StringVar()
        custom_name.set(item_name)
        trans_entry = Entry(trans_frame, textvariable=custom_name)
        trans_entry.pack(fill="both")
        trans_entry.icursor('end')
        trans_entry.focus()

        trans_entry.bind("<Return>", _tryupdate)
        trans_entry.bind("<FocusOut>", _withdraw)
        trans_entry.bind("<Escape>", _withdraw)

    def rename_item(self, item_id, new_name):
        """Rename one element of the multiple.

        Notes:
            It is not allowed to repeat names.
        """
        if new_name == self.tree[item_id].name:
            pass
        elif new_name in self.get_item_names():
            messagebox.showwarning(message=f"Name {new_name} already in use")
            self.tvw.focus_set()
        else:
            self.tree[item_id].rename(new_name)

            self.trigger_icon_update()

    def load_from_file(self):
        """load multiple content from an other file

        For multiple without dependencies, updates common items, deletes
        items absent in new file and add unexisting items. Order of new file
        is kept.

        For multiple with dependencies, only items with the same name are
        updated.
        """
        path = filedialog.askopenfilename(
            title="Partial load from file",
            filetypes=[("YAML Files", ["*.yml", "*.yaml"])],
        )
        if path == '':
            return

        with open(path, "r") as fin:
            data_in = yaml.load(fin, Loader=yaml.FullLoader)
        nob = Nob(data_in)
        new_content = nob[self.name][:]

        # simple validation of content data
        if not isinstance(new_content, list):
            messagebox.showwarning(message='Invalid file')
            self.tvw.focus_set()
            return

        if "ot_require" not in self.schema:
            changed = self._load_from_file_no_deps(new_content)
        else:
            changed = self._load_from_file_deps(new_content)

        if changed:
            self.trigger_icon_update()

        self.tvw.focus_set()

    def _load_from_file_no_deps(self, new_content):
        changed = False

        new_names = [item['name'] for item in new_content]
        new_names_order = new_names.copy()

        for item in self.tree.copy().values():  # avoid size change error
            if item.name not in new_names:  # delete items
                changed = True
                item.delete()
            else:  # update items

                index = new_names.index(item.name)
                item_changed = item.update(new_content[index])
                if item_changed:
                    changed = True
                # to make it easier to create new items
                new_names.pop(index)
                new_content.pop(index)

        # create new items
        for item_new_content in new_content:
            changed = True
            item_id = self.add_new_item(item_new_content)
            self.highlight_background_color(item_id)

        # update order
        same_order = self.is_sorted_equally(new_names_order)
        if not same_order:
            changed = True
            self.reorder_by_names(new_names_order)

        return changed

    def _load_from_file_deps(self, new_content):
        changed = False

        new_names = [item['name'] for item in new_content]
        for item in self.tree.values():
            if item.name in new_names:
                index = new_names.index(item.name)
                item_changed = item.update(new_content[index])
                if item_changed:
                    changed = True

        return changed

    def add_item_on_cursel(self):
        """Add an item in the multiple.

        Item will be added after the current selection, otherwise end
        """
        id_cursel = self.tvw.index(self.tvw.selection()[-1]) + 1 if self.tvw.selection() else "end"

        # create a new item with default value
        new_item = nob_complete(self.item_schema)
        new_name = new_item["name"]
        while new_name in self.get_item_names():
            new_name += "#"
        new_item["name"] = new_name
        item_id = self.add_new_item(new_item, pos=id_cursel)

        self.trigger_icon_update()
        self.select_item(item_id)
        self.highlight_background_color(item_id)
        self.tvw.focus_set()

    def select_item(self, item_id):
        self.tvw.selection_set(item_id)
        self.tvw.focus(item_id)

    def del_item_on_cursel(self):
        """Delete a Multiple item from tv selection."""
        selection = self.tvw.selection()
        if not selection:
            messagebox.showwarning(message="No item selected...")
        else:
            for id_cursel in selection:
                self.del_item_by_id(id_cursel)

            self.trigger_icon_update()

    def paste_data(self, item_id):
        item = self.tree[item_id]
        data = copy.deepcopy(self.clipboard)
        data['name'] = item.name
        return item.update(data)

    def add_new_item(self, data, pos='end'):
        multiple_item = OTMultipleItem(self, data['name'], self.tab, pos=pos)
        multiple_item.set(data)

        self.tree[multiple_item.id] = multiple_item
        self.tvw.update_index_row_all()

        return multiple_item.id

    def del_item_by_id(self, item_id):
        """Delete a Multiple item by its item_id."""
        self.tree[item_id].delete()
        self.tvw.update_index_row_all()

    def reorder_by_names(self, new_names_order):
        name_to_key = self.get_map_name_to_key()
        for index, name in enumerate(new_names_order):
            item_id = name_to_key[name]
            self.tvw.move(item_id, self.tvw.parent(item_id),
                          index)
        self.tvw.update_index_row_all()

    def is_sorted_equally(self, new_names):
        names = self.get_item_names()
        for name, new_name in zip(names, new_names):
            if name != new_name:
                return False
        return True

    def get_item_names(self):
        """Gets ordered item names.
        """
        return [self.tree[item_id].name for item_id in self.tvw.get_children()]

    def get_map_name_to_key(self):
        return {self.tree[item_id].name: item_id for item_id in self.tvw.get_children()}

    def get_map_key_to_name(self):
        return {item_id: self.tree[item_id].name for item_id in self.tvw.get_children()}

    def get_ordered_keys(self):
        return [child for child in self.tvw.get_children()]

    def get_status(self):
        """Compute the minimal status in children."""
        status = 1
        for child in self.tree.values():
            status = min(status, child.get_status())
        return status


class OTMultipleItem(OTContainerWidget):
    """OT  multiple widget."""

    def __init__(self, multiple, name, tab, pos='end'):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        multiple :  a Tk object were the widget will be grafted

        Notes:
            OTMultipleWidget controls <<mem_change>> triggering.
        """
        self.multiple = multiple
        self.name = name
        self.id = multiple.tvw.insert("", pos, text=name)
        self.label_frame = multiple.switchform.add(self.id, title=name)
        super().__init__(multiple.item_schema, self.label_frame, name, tab)

    def rename(self, new_name):
        data = self.get()
        data['name'] = new_name
        return self.update(data, shallow_check=True)

    def delete(self):
        self.multiple.tvw.delete(self.id)
        self.multiple.switchform.sf_del(self.id)
        del self.multiple.tree[self.id]

    def set(self, new_data, only_tvw=False):
        self.name = new_data['name']
        self.label_frame.config(text=self.name)
        values = self._get_values_from_dict(new_data)

        index = self.multiple.tvw.index(self.id) + 1
        self.multiple.tvw.item(self.id, values=values, text=index)
        if not only_tvw:
            super().set(new_data)

    def _get_values_from_dict(self, data):
        values = []
        for key in self.multiple.tvw['columns']:
            value = data.get(key, "")
            if isinstance(value, dict):
                value, = value
            values.append(str(value))

        return values

    def has_new_data(self, new_data, shallow=False):
        """Verifies if item has new data.

        Notes:
            Nested verification when update is triggered by `switchform` changes
            is misleading, as it will always be false (as method requires to
            access `switchform` info before comparison)
        """

        if shallow:
            # checks only first level
            new_values = self._get_values_from_dict(new_data)
            _, _, current_values, *_ = self.multiple.tvw.item(self.id).values()
            for cur_value, new_value in zip(current_values, new_values):
                if str(cur_value) != str(new_value):
                    return True
        else:
            cur_data = self.get()
            return not cmp_dict_values(cur_data, new_data)

        return False

    def update(self, new_data, force_changed=False, only_tvw=False,
               shallow_check=False):
        # force changed allows to color in nested situations
        if not force_changed and not self.has_new_data(new_data,
                                                       shallow=shallow_check):
            return False

        self.set(new_data, only_tvw=only_tvw)
        self.multiple.highlight_background_color(self.id)

        return True


class MultipleTreeview(ttk.Treeview):

    def __init__(self, multiple, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.multiple = multiple
        self.highlighted_tag = 'highlighted'

        self.scrollbar_y = ttk.Scrollbar(
            self.master, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=self.scrollbar_y.set)
        self.tag_configure(self.highlighted_tag, background=PARAMS['hl_bg'])

        self.popup_menu = Menu(self, tearoff=False)  # binding in tv bindings

    def config_columns(self):
        """Configure the columns apearance"""
        item_props = self.multiple.item_schema["properties"]
        all_columns = list(item_props.keys())
        show_columns = list(item_props.keys())
        self["columns"] = tuple(all_columns)
        self["displaycolumns"] = tuple(show_columns)
        self["show"] = "tree headings"
        tree_col_width = 60
        col_width = int(WIDTH_UNIT / (len(self["columns"]))) + tree_col_width
        for key, item in item_props.items():
            title = key if "title" not in item else item["title"]
            self.column(key, width=col_width)
            self.heading(key, text=title)
        self.column('#0', width=tree_col_width, anchor='c')

    def config_bindings(self):
        self.bind('<<TreeviewSelect>>', self.on_item_selected, add="+")
        self.bind("<Control-c>", self.on_copy)
        self.bind("<Control-v>", self.on_paste_sel)
        self.bind("<Control-Button-1>", self.on_paste_click)
        self.bind("<Escape>", self.on_deselect)
        self.bind("<Button-2>", self.on_popup_menu_trigger)
        self.bind('<Control-B1-Motion>', self.on_paste_click)

        # popup bindings
        self.popup_menu.add_command(label='Copy (Ctrl+C)',
                                    command=self.on_copy)
        self.popup_menu.add_command(label='Paste (Ctrl+V)',
                                    command=self.on_paste_sel)

        if "ot_require" not in self.multiple.schema:
            self.bind("<Double-1>", self.on_double_click)

            self.bind("<Control-u>", self.on_move_up)
            self.bind("<Control-d>", self.on_move_down)

            self.popup_menu.add_command(label='Move up (Ctrl+U)',
                                        command=self.on_move_up)
            self.popup_menu.add_command(label='Move down (Ctrl+D)',
                                        command=self.on_move_down)

        self.bind_all("<<mem_change>>", self._refresh_view, add="+")
        self.bind('<Enter>', self._unbind_global_scroll)
        self.bind('<Leave>', self._bind_global_scroll)

    def on_item_selected(self, event):
        if self.focus() and len(self.selection()) == 1:
            self.multiple.switchform.sf_raise(self.focus())
        else:
            self.multiple.switchform.sf_raise(None)

    def on_double_click(self, event):
        """Handle a simple click on treeview."""
        col = self.identify_column(event.x)
        if col == "#1":
            item_id = self.identify_row(event.y)
            self.multiple.rename_callback(item_id)

    def on_copy(self, *args):
        item_id = self.focus()
        if not item_id:
            messagebox.showwarning(message="No item selected")
            return

        if len(self.selection()) > 1:
            messagebox.showwarning(
                message="Copy only allowed for one element selection")
            self.focus_set()
            return

        data = self.multiple.tree[item_id].get()
        self.multiple.clipboard = data

    def on_paste_sel(self, *args):
        if not self.multiple.check_clipboard():
            return

        selection = self.selection()
        if not selection:
            messagebox.showwarning(message="No items selected")
            self.focus_set()
            return

        changed = False
        for item_id in selection:
            item_changed = self.multiple.paste_data(item_id)
            if item_changed:
                changed = True

        if changed:
            self.multiple.trigger_icon_update()

    def on_paste_click(self, event):
        if not self.multiple.check_clipboard():
            return
        item_id = self.identify_row(event.y)
        if not item_id:
            return

        changed = self.multiple.paste_data(item_id)
        if changed:
            self.multiple.trigger_icon_update()

    def on_deselect(self, *args):
        self.selection_set("")
        self.focus("")

    def on_popup_menu_trigger(self, event):
        self.popup_menu.tk_popup(event.x_root, event.y_root)

    def on_move_up(self, *args):
        item_ids = self.selection()
        moved = len(item_ids)
        for item_id in item_ids:
            current_index = self.index(item_id)
            self.move(item_id, self.parent(item_id),
                      current_index - 1)

        if moved:
            self.multiple.trigger_icon_update()
            self.update_index_row_all()

        self.focus_set()

    def on_move_down(self, *args):
        item_ids = self.selection()
        moved = len(item_ids)
        for item_id in reversed(item_ids):
            current_index = self.index(item_id)
            self.move(item_id, self.parent(item_id),
                      current_index + 1)

        if moved:
            self.multiple.trigger_icon_update()
            self.update_index_row_all()

        self.focus_set()

    def _bind_global_scroll(self, *args):
        self.event_generate('<<bind_global_scroll>>')

    def _unbind_global_scroll(self, *args):
        self.event_generate('<<unbind_global_scroll>>')

    def _refresh_view(self, event):
        """Refresh items values on tree view.

        Only required when changes are done via form.
        """
        # avoid refreshing if triggered by other
        if not is_hierarchically_above(event.widget, self.master):
            return

        for item_id, item in self.multiple.tree.items():
            # only refreshes updated frame
            if is_hierarchically_above(event.widget, item.label_frame):
                values = item.get()
                item.update(values, force_changed=True, only_tvw=True)
                break

    def update_index_row_all(self):
        for key in self.multiple.get_ordered_keys():
            index = self.index(key)
            self.item(key, text=index + 1)


# pylint: disable=too-many-arguments
class OTXorWidget:
    """OT  Or-exclusive / oneOf widget."""

    def __init__(self, schema, root_frame, name, tab, n_width=1):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        name: string naming the widget
        n_width : float
             relative size of the widget
        """
        self.tree = dict()
        self.current_child = None
        self.tab = tab
        self._schema = schema
        title = schema.get('title', "#" + name)

        self.current_child = self._schema["oneOf"][0]["required"][0]
        self._holder = ttk.Frame(
            root_frame,
            name=name,
            relief="sunken",
            # width=n_width*WIDTH_UNIT
        )

        self._title = ttk.Label(self._holder, text=title)

        self._forceps = ttk.Frame(
            self._holder, width=n_width * WIDTH_UNIT, height=1
        )
        self._menu_bt = ttk.Menubutton(self._holder, text="None")

        self._xor_holder = ttk.Frame(self._holder)

        self._holder.pack(side="top", expand=True)
        # padx=0, pady=0, expand=False)
        self._title.pack(side="top", fill="x", padx=1, pady=1)
        self._forceps.pack(side="top")
        self._menu_bt.pack(side="top")
        self._xor_holder.pack(side="top", padx=1, pady=1)  # , fill="x",
        #   padx=0, pady=0, expand=False)

        self._menu_bt.menu = Menu(self._menu_bt, tearoff=False)
        self._menu_bt["menu"] = self._menu_bt.menu

        for oneof_item in self._schema["oneOf"]:
            nam = oneof_item["required"][0]
            ch_s = oneof_item["properties"][nam]
            title = nam
            if "title" in ch_s:
                title = ch_s["title"]
            self._menu_bt.menu.add_command(
                label=title, command=lambda nam=nam: self.xor_callback(nam)
            )

        if "image" in schema:
            self._img = create_image(schema, self._holder)

        if "documentation" in schema:
            self._docu = create_documentation(schema, self._holder)

        if "description" in schema:
            self._desc = create_description(
                self._holder, schema["description"], side='top',
                padx=1, pady=1,
            )

        self.update_xor_content(self.current_child)

    def xor_callback(self, name_child):
        """Event on XOR menu selection."""
        if name_child != self.current_child:
            self.update_xor_content(name_child, data_in=None)
            self._menu_bt.event_generate("<<mem_change>>")
            self.highlight_background_color()

    def highlight_background_color(self):
        self._menu_bt.configure(style='Highlighted.TMenubutton')

    def reset_background_color(self):
        self._menu_bt.configure(style='TMenubutton')

    def update_xor_content(self, name_child, data_in=None):
        """Reconfigure XOR button.

        Inputs :
        --------
        name_child : sting, naming the child object
        data_in : dictionary used to pre-fill the data
        """
        self.current_child = name_child
        child_schema = None
        for possible_childs in self._schema["oneOf"]:
            if possible_childs["required"][0] == name_child:
                child_schema = possible_childs["properties"][name_child]

        for child_widget in self._xor_holder.winfo_children():
            child_widget.destroy()

        self.tree = dict()
        self.tree[name_child] = OTContainerWidget(
            child_schema,
            self._xor_holder,
            name_child,
            self.tab,
            relief="flat",
            show_title=False,
        )
        if data_in is None:
            self.tree[name_child].set(nob_complete(child_schema))
        else:
            self.tree[name_child].set(data_in)

        title = child_schema.get('title', name_child)
        self._menu_bt.configure(text=title)

        PARAMS["top"].update_idletasks()
        self.tab.smartpacker()

    def get(self):
        """Get the data of children widgets.

        Returns :
        ---------
        a dictionnary with the get result of current children
        """
        out = dict()
        try:
            found = self.tree[self.current_child].get()
            if found is not None:
                out[self.current_child] = found
            else:
                out[self.current_child] = None
        except GetException:
            pass

        if out == {}:
            out = None
        return out

    def set(self, dict_):
        """Get the data of children widgets.

        Input :
        -------
        a dictionnary with the value of the childrens
        """
        given_keys = dict_.keys()
        if len(given_keys) > 1:
            raise SetException("Multiple matching option, skipping...")

        for one_of in self._schema["oneOf"]:
            child = next(iter(one_of["properties"]))
            if child in dict_:
                try:
                    self.update_xor_content(child, dict_[child])
                except SetException:
                    pass

    def get_status(self):
        """Proxy to the get_status of the current child."""
        return self.tree[self.current_child].get_status()


def show_docu_webpage(markdown_str):
    """ Show documentation in the web browser

    Use package `markdown`to translate markown into HTML.
    Dump is into a temporary file using `tempfile`package.
    Finally call the browser using `webbrowser`package.
    """
    md_ = markdown.Markdown()
    css_style = """
 <style type="text/css">
 body {
    font-family: Helvetica, Geneva, Arial, SunSans-Regular,sans-serif ;
    margin-top: 100px;
    margin-bottom: 100px;
    margin-right: 150px;
    margin-left: 80px;
    color: black;
    background-color: BG_COLOR
 }

 h1 {
    color: #003300
}
 </style>
"""
    css_style = css_style.replace("BG_COLOR", PARAMS["bg"])

    html = str()
    html += md_.convert(markdown_str)
    html = html.replace('src="', 'src="' + PARAMS["calling_dir"] + "/")

    # with tempfile.NamedTemporaryFile(
    #     "w", delete=False, suffix=".html"
    # ) as fout:
    #     url = "file://" + fout.name
    #     fout.write(html)

    #     html = css_style + html

    #     tmp_file = ".docu_tmp.html"
    #     with open(tmp_file, "w") as fout:
    #         fout.write(html)
    #         url = "file://" + os.path.join(os.getcwd(), tmp_file)
    #     webbrowser.open(url)
    # else:

    html = html.replace("<h1", '<h1 style="color: #003300"')
    html = html.replace("<h2", '<h2 style="color: #003300"')
    html = html.replace("<h3", '<h3 style="color: #003300"')
    top = Toplevel()
    html_label = tkhtml.HTMLScrolledText(
        top, html=html, background=PARAMS["bg"]
    )
    html_label.pack(fill="both", expand=True)
    html_label.fit_height()


def create_documentation(schema, master):

    def show_docu(event, docu_ct):
        show_docu_webpage(docu_ct)

    docu_ct = schema["documentation"]

    docu_lbl = ttk.Label(master, text="learn more...", style='Linkable.TLabel')
    docu_lbl.pack(side='bottom')

    docu_lbl.bind("<Button-1>", lambda e, docu_ct=docu_ct: show_docu(e, docu_ct))

    return docu_lbl


def create_image(schema, master):
    path = os.path.join(PARAMS["calling_dir"], schema["image"])
    img = ImageTk.PhotoImage(Image.open(path))
    img_lbl = ttk.Label(master, image=img)

    img_lbl.image = img
    img_lbl.pack(side='top')

    return img_lbl


def is_leaf(node):
    return isinstance(node, LeafWidget)


def get_nodes_with_method(tree, method_name, nodes):
    if type(tree) is dict:  # some trees are dict, other are lists
        tree = list(tree.values())

    for node in tree:
        if hasattr(node, method_name):
            nodes.append(node)

        if not is_leaf(node):
            get_nodes_with_method(node.tree, method_name, nodes)
