# The Zen of Zope, by Jeffrey 'Alex' Clark

A crash course on the [Zope Component Architecture](https://zopecomponent.readthedocs.io/)
(ZCA), told through the 19 aphorisms of
[The Zen of Python](https://peps.python.org/pep-0020/).

## Background

Python has `import this`, which prints *The Zen of Python* by Tim Peters.
Daniel Greenfeld answered it with [`that`](https://pypi.org/project/that/),
*The Anti-Zen of Python*. And so, naturally, there is `import other`.

Each line of the Zen is rewritten around a ZCA concept and then
demonstrated with working `zope.interface` and `zope.component` code:
interfaces and the objects that implement or provide them, invariants,
tagged values, adapters and multi-adapters, subscribers, adapter hooks,
verification and utilities. Read `other.py` in the
[repository](https://github.com/aclark4life/other) from top to bottom to see
how each line is produced.

It was written in 2012, based on the `zope.interface` and `zope.component`
documentation, and updated for Python 3 in 2026.

## Installation

`other` requires Python 3.10 or later. Install it from PyPI:

```console
$ pip install other
```

This also installs `zope.component` and `zope.interface`.

## Usage

Run it from the command line (`import other` prints the same thing):

```console
$ python -m other
The Zen of Zope, by Jeffrey 'Alex' Clark


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
```

## Development

Clone the repository and install it in editable mode, along with the `dev`
dependency group (pip 25.1 or later):

```console
$ git clone https://github.com/aclark4life/other.git
$ cd other
$ pip install -e . --group dev
```

Run the tests with [pytest](https://docs.pytest.org/) from the root of the clone:

```console
$ pytest
```

Linting and formatting use [ruff](https://docs.astral.sh/ruff/), run through
[prek](https://prek.j178.dev/) pre-commit hooks. Install the hooks once per
clone, and they run on every commit:

```console
$ prek install
```

To run every hook against every file (this may fix and reformat files):

```console
$ prek run --all-files
```

## License

MIT. See [LICENSE](https://github.com/aclark4life/other/blob/main/LICENSE).
