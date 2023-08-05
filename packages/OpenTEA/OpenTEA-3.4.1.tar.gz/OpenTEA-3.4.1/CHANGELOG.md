# Changelog

All notable changes to this project will be documented in this file.
The format is based on Keep a Changelog,
and this project adheres to Semantic Versioning.


## [3.4.1] 2021 / 10 / 04

### Added
- popup menu with copy, paste and move for `OTMultipleWidget`
- new bindings in `OTMultipleWidget` (move and deselect)
- move up and down buttons in `OTMultipleWidget`
- highlight widgets when they are changed (by changing color)
- add scrollbar to disabled listboxes (`OTListStatic`)
- `MouseScrollFrame`: scrollable frame scrollable via mouse wheel
- add copy-paste popup menu to `OTList` and `OTListStatic`
- add copy-paint binding to `OTMultipleWidget`
- add row number to multiple treeview
- `OTHidden` leaf to make it easier to have nodes that can change value, but are not visible
- add several warning message boxes in `OTMultipleWidget`


### Fixed
- remove double description when `ot_type` in schema
- bindings in `OTMultipleWidget`
- no underscores required as prefix in `OTMultipleItem` names
- `OTMultipleItem` load button behavior
- multiple changes that were not triggering tab icon change
- checkboxes, menus and radiobuttons do not trigger any action if current value is chosen again
- `OTFileBrowser` does not raise error when user cancel path search
- `OTList` behavior: validation of input and error message
- theme selection
- empty titles are not shown in `OTContainer`


### Changed
- `OTMultipleWidget.tree` is now a `dict` (instead of `list`)
- split `OTList` and `OTChoice` in smaller objects for easier mantainability
- replaced several `tk.Label` by `ttk.Label` in order to make the most out of styles
- multiple treeview is now its own object (`MultipleTreeview`)
- name only appears in switchform title in `OTMultipleItem`
- entries with no validation requirements (strings) do not have extra space for status label anymore 


## [3.3.0] 2021 / 03 / 09

### Added

- adding `opentea.__version__` attribute though VERSION file
- adding a new project management. A project name is asked if missing
- nobvisual inspection of projects
- recursive fusion of SCHEMA, for composite GUIs

### Changed

- the project is saved at each "Validate/Process"
- cursor switch to waiting mode during "Validate/Process"
- the temp. files like `dataset_to_gui.yml` are now hidden as `.dataset_to*`
- help windows are now rendered using the tkhtmlview package as a top-level window.
- File dialogs store relative paths, not absolute paths

### Fixed

[ - ]

### Deprecated

[ - ]

## [3.2.3 ] 2020 / 11 / 09

### Added

[ - ]
  
### Changed

[ - ]

### Fixed

- the widget comment is no more recursively adding blank lines.

### Deprecated

  [ - ]

## [3.2.2 ] 2020 / 11 / 09

### Added

  [ - ]
  
### Changed

- nob_complete can now keep the input data that was not  in the SCHEMA

### Fixed

- some loop holes in validate_light

### Deprecated

- H5proxy is deprecated, should be replaced by hdfdict

## [3.2.1 ] 2020 / 06 / 04

### Added

  [ - ]
  
### Changed

- Statuses of tabs are recovered when reading a project
- search disabled in consoles by default
- CLI improvements

### Fixed

- spurious dependency on python 3.7 for subprocess, now 3.6 is fine too
- no more deprecated calls to 3D engine
- for documentation : use recomonmark instead of m2r (deprecated)

### Deprecated

[ - ]

## [3.2] 2020 / 03 / 13

### Added

- expert dialogs
- dynamic choices
- support of 3D viewer with tiny_3d_engine
  
### Changed

- red output if an error is onprocess
- comments with clear enable/disable mode
- description can tag style tags for itlaliv, bold, small or tiny texts.

### Fixed

 - bug on multiple with depencencies if the list was going to zero

### Deprecated

[ - ]

## [3.1.1] 2020 / 01 / 15

### Added

[ - ]

### Changed

[ - ] 

### Fixed

- deprecation warning from **h5proxy** removed (consider using hdfdict or H5wrapper instead..)

### Deprecated

[ - ]

## [3.1.0] 2019 / 12 / 05

### Added

- **h5proxy** to read quickly in an H5file (consider using hdfdict or H5wrapper instead..)
- **schema2md** convert schema file into HTML tables 

### Changed

[ - ]

### Fixed

[ - ]

### Deprecated

[ - ]

## [3.0.0] 2019 / 03 / 26

### Added

- Tkinter Graphical engine
- noob library
- nob_complete
- nob_validate

### Changed

[ - ]

### Fixed

[ - ]

### Deprecated

- All Tcl and Python for Version 2 

## [2.3] 2018 / 10 / 17

### Added

[ - ]

### Changed

- Documentation using sphinx
- widget info can display icon depending on content

### Fixed

[ - ]

### Deprecated

[ - ]
