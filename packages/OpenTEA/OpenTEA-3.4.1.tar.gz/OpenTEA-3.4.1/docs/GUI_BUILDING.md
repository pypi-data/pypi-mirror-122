# Building the GUI

## Simple Example

We start with the following simple example, step by step, on the [SCHEMA specification](https://json-schema.org/understanding-json-schema/)


The basic structure of the GUI is a graph. The nodes of the graphs are spread over 3 levels, root, tabs and blocks.

```
- root
  - tab 1
    - block 1.1
    - block 1.2
 - tab 2
    - block 2.1
    - block 2.2
    - block 2.3
```

![roottabblock](./_images/root_tabs_blocks.png)
**Root is the Major "Forms" tab. Tabs are shown in the second line with oragne icons. Then four nested blocks are shown**  

**Root** stands for the top-level of the whole form.

**Tabs** are the nodes grouping parameters of a similar family, such as "numerics", "boundary conditions", "meshes". 
One should design the interface with the general idea of a Left to Right filling of the forms.
Therefore there is a tacit order of resolutions between tabs.
**The last tab** must be reserved for the final execution of the action.

**Blocks** are grouping visually parameters in columns. The packing algorithm is filling the GUI screen in columns. The width of the general window controls the number of columns packed.


 
*Please, stick this 3-level structure for your GUIs. 
The packing is optimized for this usage. Less than 3 levels will probably fail at startup. 
More than 3 levels (blocks in blocks) will limit the fluidity of the repacking when readjusting the window.*
 

###Root Node level, the window

A this level, we only create a [SCHEMA object](https://json-schema.org/understanding-json-schema/reference/object.html) (`type:object`) which can store, as `properties` , one or several tabs

```yaml
---
title: "All you can Eat..."
type: object
properties:
  first_tab:
	    ...
  second_tab:
	    ...
	    
```

Root nodes, in yaml are litterally sticking to left margin of your YAML file.


### Second Node level, the tab

We define here again a [SCHEMA object](https://json-schema.org/understanding-json-schema/reference/object.html) (`type:object`) which can store, as `properties` , one or several hlder objects called **blocks**.


```yaml
..(root)
  first_tab:
	 type: object
	 title: First tab.
	 process: custom_callback.py
	 description: "tab description"
	 order: 20
	 properties:
	   first_block:
	     ...
	   second_block:
	     ...           
```

*A quick tip : Tabs nodes, in yaml are found after 1 indentation (2 spaces, providing you use the standard 2 spaces chars indentation). The content is found after 2 indentations / 4 chars.*


As for now, tabs a displayed in the order of the schema.
The Tab level is interpreting the  following additionnal attributes:

- `description`. This attribute is the SCHEMA official attibute. It takes a string. The string will be shown in the GUI at thebottom left of the Tab.
- `process`. This attribute is special for opentea. The string refer to the name of a python script to be called when pressing the "Process" button (a.k.a callback).  See section Tabs callbacks for further information...
- `order` This attribute is special for opentea, but have no effect for the moment. It will force the order of Tabs when the functunality "Hide this tab" will be implemented.

Tab DOES NOT support the attributes `image`or `documentation`.
It however supports the  attribute `description`, providing the string is sufficently short.
Indeed, there is no huge room for display at the bottom of the tabs. 

#### Tabs callbacks

Without callbacks, OpenTEA is simply some forms allowing you to fill a nested object (a YAML file on the disc) according to a SCHEMA specification. 
Tabs callbacks are the way to add interactivity to your forms. The data passed from the GUI to the callback is the GUI memory itself, dumped as the file `dataset_from_gui.yml`. The data passed from the  callback to the GUI is dumped as the file `dataset_to_gui.yml`

In the end, the signature of the function is `callback(nob_in) > nob_out`, with nob a python nested object (e.g. dicts of dicts of lists of anything you can serialize in YAML...). YOu can refer to [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation) for practical examples.

A typical callback is the following:

```Python
"""Module for the first tab."""

from opentea.noob.noob import nob_get, nob_set
from opentea.process_utils import process_tab


def custom_fun(nob_in):
    """Update the result."""
    nob_out = nob_in.copy()
    operation = nob_get(nob_in, "operand")
    nb1 = nob_get(nob_in, "number_1")
    nb2 = nob_get(nob_in, "number_2")

    res = None
    if operation == "+":
        res = nb1 + nb2
    elif operation == "-":
        res = nb1 - nb2
    elif operation == "*":
        res = nb1 * nb2
    elif operation == "/":
        res = nb1 / nb2
    else:
        res = None

    # raise RuntimeError("Tahiti a plante ce processus")

    nob_set(nob_out, res, "result")
    return nob_out


if __name__ == "__main__":
    process_tab(custom_fun)
```

Concerning **Error Handling**. OpenTEA calls a Sub process of a python script. Therefore, a failue in the script will not freeze the application.  The current Tab becomes red, with the message typically *Failed after 0.16s*. You can customize : if the script raises a `RunTimeError("foobar")`, the error string (here `"foobar"`) will be copied to the button status, typically *Failed after 0.16s, RunTimeError:  foobar* 


### Third Node level, the block

We define here again a [SCHEMA object](https://json-schema.org/understanding-json-schema/reference/object.html) (`type:object`) which can store, as `properties` , one or several holder objects called **blocks**.

It looks like the following:
![block](./_images/block.png)

```yaml
......(tab)
      first_block:
        type: object
        title: Customer Info
        description: >

          Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi 
          ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit 
          in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur 
          sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit 
          anim id est laborum.
          
        documentation: >
    
			# title
			  
			## subtitle
			
			Lorem ipsum dolor sit amet, consectetur adipiscing elit,
			sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
			Ut eru[avbp website](http://www.cerfacs.fr/avbp7x/)  nisi 
			ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit 
			in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur 
			sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit 
			  
			## subtitle
			
			Lorem ipsum dolor sit amet, consectetur adipiscing elit,
			sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
			  
			![image](test-pattern-tv.jpg)
			
			| add  | bdfsf | vxgc | sds | vwv  |
			|---|---|---|---|---|
			| 11  | 12  | 13  | 14  | 15  |
			| 21  | 22  | 23  | 24  | 25  |
 
        image: test-pattern-tv.jpg
        properties:
          name:
            ... 
          age:
            ... 
          membership:
            ... 

```
*Block nodes, in yaml, are found after three indentation (6 spaces, providing you use the standard 2 spaces chars indentation). The content is found after four indentations / 8 chars.*

You can nest more blocks under blocks if needed.

The Block level is accepting the following additionnal attributes:

- `description`. This attributes is the SCHEMA official attibute. It takes a string. The string will be shown in the GUI at the bottom left of the block.
- `image`. This attribute is specific to OpenTEA, and does not belong to the SCHEMA standard. The image must be stored in the folder of the main schema file. It will be shown, without scaling, at the bottom of the block.
- `documentation`. This attribute is specific to OpenTEA, and does not belong to the SCHEMA standard. It takes a string using Markdown syntax. This wil add at the bottom of the block the blue label "learn more...". On click this label trigger the opening of the browser, loading the HTML rendering of the Markdown content. Al features of Markdown are supoorted. Images must be stored at the root of tge GUI, where the schema is.
- `expert`.This attribute is specific to OpenTEA. It make the block collapsable. If `expert`is set to True, the block is initially collapsed. A click on the + / -  witl expand-collapse it.
![expertc](./_images/expert_collapsed.png)
![experte](./_images/expert_expanded.png)


### Leaf level , or Parameters


Parameters are defined still in acordance with the SCHEMA standard:

#### Entries

The most basic parameters are called Entries.
Here are the most common types : 

- `string` [string types](https://json-schema.org/understanding-json-schema/reference/string.html)
- `integer`, `number`, [numeric types](https://json-schema.org/understanding-json-schema/reference/numeric.html)
-  `boolean`. [boolean types](https://json-schema.org/understanding-json-schema/reference/boolean.html)

```yaml
         (block)
		   name:
				title: "Name"
				type: string
				default: "john doe"
			age:
				title: "Age"
				type: integer
				default: 42
			age:
				title: "Weight"
				type: number
				default: 13.2
			membership:
				title: "Membership"
				type: boolean
				default: False
```
The appearance is the following:
![entries](./_images/entries.png)

The gui will check the type of the entry, and refuse invalid inputs.

You can add further validation rules, to prevent non-acceptable values righ from the form, using the SCHEMA validators. In the following example, the user cannot enter a number outside ofthe range ]1, 2[. : 

```yaml
         (block)
         ent1:
            default: 1.3
            exclusiveMaximum: true
            exclusiveMinimum: true
            maximum: 2
            minimum: 1
            title: Essai double_gt1_lt2
            type: number
```

### simple arrays (lists)

The SCHEMA arrays, for the simplest ones, are equivalent to Python's lists.
In the following example, the list is modifiable by the user, from 0 to 999 elements.

```yaml
         (block)
         list_patches:
            type: array
            title : Liste des patches
            items : 
              type : string
              default: single_patch
```

The list entries look like:
![listentries](./_images/list_entries.png)

this is given by the SCHEMA:

```yaml
 entlist:
        title: List entries
        type: object
        description: >
            List entries
        properties:
          entl1:
            title: String - dynamic
            type: array
            items:
              type: string
              default: Catch a tiger
          entl2:
            title: Integer - X4
            type: array
            minItems: 4
            maxItems: 4
            items:
              type: integer 
              default: 42
          entl3:
            title: Number - 3X 
            type: array
            minItems: 3
            maxItems: 3
            items:
              type: number 
              default: 666.
```

### Disabled state

You can set an entry in *disabled* state when you set the opentea-specific attribute `state= disabled`.
The user wil not be able to act directly on the value. You can howver promatically modify the value by changing the memory in the callback. In the following example, a list of string that will be modified by setting the node `list_patches` to a list of strings.

```yaml
         (block)
         list_patches:
            type: array
            title : Patch list
            state : disabled
            items : 
              type : string
              default: single_patch
```
![listdisabled](./_images/list_disabled.png)


#### Choices

The SCHEMA notation for used-defined entries options is the `enum` attribute :

```yaml
         (block)
         ndim_choice:
           default: two
           enum:
           - two
           - three
           enum_titles:
           - 2-D
           - 3-D
           title: Dimensions
           type: string
```

Note the attribute `enum_titles` specific to opentea, to override the Titles shown in the GUI.

The choice is initially a radiobutton, but with switch to a combobox beyond 3 items:

![choices](./_images/choices.png)

In some cases you want to create a choice between options that will be known only at run-time.
This is a **dynamic choice**.
In the following example, the list `list_patches` is updated by some callbacks.
The choice `choice_patches` will have its options list updated when  `list_patches` changes.

```yaml
		list_patches:
            type: array
            title : Liste des patches
            state : disabled
            items : 
              type : string
              default: single_patch
		choice_patches:
            title: Choix patches
            type: string
            ot_dyn_choice: list_patches
```

#### Comments

If you want to create an input on multilines, openTea offer the widget comment.
It is basically a Textbox. In the yaml, add simply the decorator `ot_type: comment`to a string.
In the following example, two comment entries are created. 

```yaml
	       mod_comment:
            title: bossa nova
            type: string
            default: Lorem ipsum sic hamet
            height: 20
            ot_type: comment
          readonly_comment:
            title: fdo
            type: string
            default: Lorem ipsum sic hamet
            state: disabled
            ot_type: comment
```

![comments](./_images/comments.png)

The `height` attibute allow to increase the size of the widget. Its default appearance is on 6 lines.
The `state=disabled`allow to deactivate the user-interaction. 
The widget content can only be updated by a callback, which is usefull to present logfiles, informations or input_files generated by the GUI. 

### Files and folder

When you want a dialog to set a file or a folder, add the attribute `ot_type: file`.
The entry will include a small button starting a "Selecting file dialog".

You can limit the search to some extentions using the atrribute  "ot_filter: [h5]" (for .h5 files).
You also can limit to directories using the attribute "ot_filter: directory".
In the following example, two widgets are created, a H5 file selector and a directory selector.

```yaml
 			file4:
            ot_type: file
            ot_filter:
            - h5
            title: Choix fichier (*.h5)
            type: string
            default: any.h5
          file5:
            ot_type: file
            ot_filter: directory
            title: Choix repertoire
            type: string
            default: anyfolder
```

## Special blocks

Special blocks are structures allowing more complexity in the nested object 

### eXclusive OR objects

The exclusive OR mean that the structure can be either one graph or another, *but nothing else*. 


*This stems from the [SCHEMA oneOf](https://json-schema.org/understanding-json-schema/reference/combining.html#oneof), which is much more permissive : one graph, or another or a void graph*.


![xor](./_images/xor.png)

To achieve a proper validation with the SCHEMA standard, the XOR structure is the following.
Erm... brace yourselves, this is the hardest SCHEMA  part you will encounter in this manual:

```yaml
... (block or tab)
          purchase:
            title: "select purchase"
            type: object
            oneOf:
            - type: object
              required: [takeaway]
              properties:
                takeaway:
                  type: object
                  properties:
                    ...
            - type: object
              required: [lobby]
              properties:
                lobby:
                  type: object
                  properties:
                    ...
```

Here the `oneOf` takes  a list of options. Each option is an `object` with a `required` single property. :

```yaml
...(oneOf)
              type: object
              required: [lobby]
              properties:
                lobby:
                  type: object
                  properties:
                      ...
```

The XOR Widget full supports the attributes `description`, `documentation`or `image`, like the other blocks.

### Multiple objects

This structure is the [SCHEMA array](https://json-schema.org/understanding-json-schema/reference/object.html), using `required`properties:


It is a big widget, with a treeview on the left, and a flipform on the right:
![multiple](./_images/multiple.png)


```yaml
... (block or tab)
  vegetables:
    title: Edible vegetable (Multiple example)
    type: array
    items:
      type: object
      required:
      - name
      - veggieLike
      properties:
        name: 
          type: string
          description: The name of the vegetable.
          default: dummy_vegetable
          state: disabled
        veggieLike:
          type: boolean
          description: Do I like this vegetable?
          default: False
```

 Opentea requires a **compulsory string property**, `name` that you must set as read/only (see example before), 
This will help to handle the content of the multiple. Indeed, If your multiple dialogue handle mode than 20 items, you will be happy to use names and not list index... trust me.

The Multiple Widget DOES NOT support the attributes `description`, `documentation`or `image`.


#### Multiple with dependency

You can link the multiple to another value using the openTEA specific `ot_require` keyword. It must refer to an existing node, preferably a list of strings, like here the `list_patches` information.

```yaml
      mul_cont:
        items:
          type: object
          title: Boundary cond.
        ot_require: list_patches
        type: array
        properties:
          (...)
```

If this list of patches is updated, the items under the multiple influence will be updated. 

## Data output

The data is saved as a YAML serialized nested object.
The data saved by the GUI "simple_example" in `./src/opentea/examples/simple/` is looking like this :

```yaml
irst_tab:
  first_block:
    age: 42
    membership: false
    name: john doe
  second_block:
    purchase:
      takeaway:
        bag: false
second_tab:
  first_block:
    vegetables:
    - name: dummy_vegetable
      veggieLike: false
```

## Style adjustments


Most of the styling in the OpenTEA GUI is automatic.
The layout, the colors and the widgets cannot be overriden.

The GUI developer can however tune some aspects:

### Theme

OpenTEA is powered by Tkinter, and rely on Tkinter themes.
The default theme is `clam`, available on all platforms.
You can force a Tkinter theme available on your platform (`aqua` on OSX for example),
using the optional argument `theme="aqua"` on the startup function `main_otinker()`.


### Images

The images in the GUI are introduced either with the attribute 'image' in blocks, or in the markdown documentation.

### Block Descriptions 

Block descriptions can be tuned with the following tags inserted in the text:
- `<small>` decrease the font size to 12
- `<tiny>` decrease the font size to 10
- `<bold>`chenge text to bold
- `<italic>` change text to italic

For example, the following input will create a description with italic, 12pts default font.

```
     description: >
                 <small> <italic> Lorem ipsum sic hamet
```
