# Contributing

If you are here, it means you wish to help this project go forward. So first:
**Thanks!**

There are several aspects on which you can contribute:

## The documentation

The documentation for OpenTEA is hosted on the server domu.cerfacs.fr. It is
visible at cerfacs.fr/opentea. It is generated using a tool called
[Sphinx](http://www.sphinx-doc.org/). You must have it installed via `pip
install sphinx`. Then, go in the `doc/` folder, edit the `.rst` files (see the
Sphinx doc for details) according to your desired modifications. The html can
then be built by doing `make html`.

When you are happy with your update, create a branch and a merge request on
nitrox. Once accepted, you can upload it with `make push`. Warning: to do this,
you must have access to opentea@domu, and define the alias `domu_opentea`.
Contact the [COOP Team](mailto:coop@cerfacs.fr) to get the access. To define the
alias, edit your `~/.ssh/config` file to add:

```
Host domu_opentea
    HostName domu
    User opentea
    ProxyJump dogon
```

## The TCL/Tk renderer

Who are you??? See [Antoine Dauptain](mailto:dauptain@cerfacs.fr)

## The Python engine

The engine is in the `opentea/` folder. Have fun :).

Please create reasonably sized branches around a clear feature `X`, and
call it `feature_X`. Before pushing, please follow these instructions:

  - the first time: run `make init` (installs the dependencies)
  - then, before each commit, run:
      - `make lint`: checks your syntax. You **must** get 10/10 on this step.
      - `make test`: checks that all unit tests pass. Again, less than
         100% is not acceptable for merging.

When you have passed all both the above tests, push your branches to the
master repo and create a merge request towards `develop`.

## Thanks for contributing!
