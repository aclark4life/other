The Zen of Zope, by Alex Clark
==============================

A crash course on the `Zope Component Architecture`_ (ZCA), told through the
19 aphorisms of `The Zen of Python`_.

Background
----------

Python has ``import this``, which prints *The Zen of Python* by Tim Peters.
Daniel Greenfeld answered it with `that`_, *The Anti-Zen of Python*. And so,
naturally, there is ``import other``.

Each line of the Zen is rewritten around a ZCA concept and then
demonstrated with working ``zope.interface`` and ``zope.component`` code:
interfaces and the objects that implement or provide them, invariants,
tagged values, adapters and multi-adapters, subscribers, adapter hooks,
verification and utilities. Read `other.py`_ from top to bottom to see how
each line is produced.

It was written in 2012, based on the ``zope.interface`` and
``zope.component`` documentation, and updated for Python 3 in 2026.

Installation
------------

``other`` requires Python 3.10 or later. Install it from PyPI::

    $ pip install other

This also installs ``zope.component``, ``zope.interface`` and, for fun,
``that``.

Usage
-----

Run it from the command line (``import other`` prints the same thing)::

    $ python -m other
    The Zen of Zope, by Alex Clark


    Beautiful is an attribute of person.
    Explicit is implemented by implicit.
    Simple is provided by complex.
    Complex is directly provided by complicated.
    Flat only implements nested.
    Sparse has tagged value dense.
    Readability count is not in range.
    Special cases could not adapt the rules.
    Practicality implements purity.
    Errors should never require a specification that doesn’t extend the specification of silence.
    Unless explicit is a multi-adapter.
    In subscribing to ambiguity, return all the objects that refuse the temptation to guess.
    There should be none-- and preferably only zero --output from a handler.
    Although that way may not be obvious at first unless you've registered an adapter hook.
    Now is verified by never.
    Although never is not implemented by *right* now.
    If the implementation is hard to explain, it queries the bad idea utility.
    If the implementation is easy to explain, it may query the good idea utility.
    Implicit namespace packages are one honking great idea -- let's do more of those!

Development
-----------

Clone the repository and install it in editable mode, along with the
``dev`` dependency group (pip 25.1 or later)::

    $ git clone https://github.com/aclark4life/other.git
    $ cd other
    $ pip install -e . --group dev

Run the tests from the root of the clone::

    $ python -m unittest -v tests

Linting and formatting use `ruff`_, run through `prek`_ pre-commit hooks.
Install the hooks once per clone, and they run on every commit::

    $ prek install

To run every hook against every file (this may fix and reformat files)::

    $ prek run --all-files

.. _Zope Component Architecture: https://zopecomponent.readthedocs.io/
.. _The Zen of Python: https://peps.python.org/pep-0020/
.. _that: https://pypi.org/project/that/
.. _other.py: https://github.com/aclark4life/other/blob/master/other.py
.. _ruff: https://docs.astral.sh/ruff/
.. _prek: https://prek.j178.dev/
