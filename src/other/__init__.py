"""
The Zen of Zope: a crash course on the Zope Component Architecture (ZCA),
told through the aphorisms of The Zen of Python.

Importing this package prints them, the way ``import this`` prints the Zen
of Python. Each numbered section below is self-contained: its line of the
Zen, a note on the ZCA concept it shows, what it defines, and the check that
prints its line. Read it from top to bottom.
"""

# Based on the zope.interface and zope.component documentation, and heavily
# inspired by The Anti-Zen of Python, by Daniel Greenfeld and The Zen of
# Python, by Tim Peters. Special thanks to Guido Van Rossum for Python, and
# Jim Fulton for Zope.
# Copyright (C) 2012 Jeffrey 'Alex' Clark
# Released under the MIT License; see LICENSE.

from dataclasses import dataclass

from zope.component import provideUtility, queryUtility
from zope.interface import (
    Attribute,
    Interface,
    Invalid,
    directlyProvidedBy,
    directlyProvides,
    implementedBy,
    implementer,
    implementer_only,
    invariant,
    providedBy,
)
from zope.interface.adapter import AdapterRegistry
from zope.interface.exceptions import BrokenImplementation
from zope.interface.interface import adapter_hooks
from zope.interface.verify import verifyObject

print("The Zen of Zope, by Jeffrey 'Alex' Clark\n\n")


# ------------------------------------------------------------------------------
# 1. Beautiful is better than ugly.
#
# An interface specifies behavior: documentation, attributes, invariants.
# verifyObject checks that an object has what its interface promises.
# ------------------------------------------------------------------------------


class IPerson(Interface):
    beautiful = Attribute("Beautiful is an attribute of person.")


@implementer(IPerson)
class Person:
    beautiful = True


if verifyObject(IPerson, Person()):
    print(IPerson["beautiful"].__doc__)


# ------------------------------------------------------------------------------
# 2. Explicit is better than implicit.
#
# Classes implement interfaces; their instances provide them.
# ------------------------------------------------------------------------------


class IExplicit(Interface):
    """An interface, implemented by a class."""


@implementer(IExplicit)
class Implicit:
    pass


if IExplicit.implementedBy(Implicit):
    print("Explicit is implemented by implicit.")


# ------------------------------------------------------------------------------
# 3. Simple is better than complex.
#
# An instance provides the interfaces its class implements.
# ------------------------------------------------------------------------------


class IComplex(Interface):
    """An interface, provided by instances of a class that implements it."""


@implementer(IComplex)
class Complex:
    pass


if IComplex.providedBy(Complex()):
    print("Simple is provided by complex.")


# ------------------------------------------------------------------------------
# 4. Complex is better than complicated.
#
# An object can also provide an interface directly, whatever its class
# implements.
# ------------------------------------------------------------------------------


class Complicated:
    pass


complicated = Complicated()
directlyProvides(complicated, IComplex)
if IComplex in directlyProvidedBy(complicated):
    print("Complex is directly provided by complicated.")


# ------------------------------------------------------------------------------
# 5. Flat is better than nested.
#
# implementer_only replaces the interfaces a class inherits, instead of
# adding to them.
# ------------------------------------------------------------------------------


class INested(Interface):
    """The only interface Flat implements."""


@implementer_only(INested)
class Flat(Complex):
    pass


if list(implementedBy(Flat)) == [INested]:
    print("Flat only implements nested.")


# ------------------------------------------------------------------------------
# 6. Sparse is better than dense.
#
# Interfaces can carry tagged values: arbitrary metadata stored on them.
# ------------------------------------------------------------------------------


class ISparse(Interface):
    """An interface with a tagged value."""


ISparse.setTaggedValue("dense", "Sparse has tagged value dense.")
if "dense" in ISparse.getTaggedValueTags():
    print(ISparse.getTaggedValue("dense"))


# ------------------------------------------------------------------------------
# 7. Readability counts.
#
# Invariants are conditions that must hold for an object to provide an
# interface; validateInvariants raises when one fails.
# ------------------------------------------------------------------------------


class RangeError(Invalid):
    """The upper bound is below the lower bound."""


def range_invariant(ob):
    if ob.max < ob.min:
        raise RangeError(ob)


class IRange(Interface):
    min = Attribute("Lower bound")
    max = Attribute("Upper bound")
    invariant(range_invariant)


@implementer(IRange)
@dataclass
class Range:
    min: int
    max: int


try:
    IRange.validateInvariants(Range(2, 1))
except RangeError:
    print("Readability count is not in range.")


# ------------------------------------------------------------------------------
# 8. Special cases aren't special enough to break the rules.
#
# Calling an interface adapts an object to it, and raises TypeError when
# there is no way to.
# ------------------------------------------------------------------------------


class ISpecialCases(Interface):
    """An interface nothing adapts to."""


try:
    ISpecialCases("the rules")
except TypeError:
    print("Special cases could not adapt the rules.")


# ------------------------------------------------------------------------------
# 9. Although practicality beats purity.
#
# Adapting an object to an interface it already provides returns the object
# itself.
# ------------------------------------------------------------------------------


class IPurity(Interface):
    """An interface Practicality provides."""


@implementer(IPurity)
class Practicality:
    pass


practicality = Practicality()
if IPurity(practicality) is practicality:
    print("Practicality implements purity.")


# ------------------------------------------------------------------------------
# 10. Errors should never pass silently.
#
# An adapter registry maps required specifications to provided ones. A
# lookup finds a registration for specifications that extend the required
# one (IPass extends IErrors), but not for ones that don't (Interface: IErrors
# extends it, not the other way round).
# ------------------------------------------------------------------------------


class IErrors(Interface):
    """Errors."""


class ISilence(Interface):
    """Silence."""


class IPass(IErrors):
    """Errors that pass, explicitly silenced."""


registry = AdapterRegistry()
registry.register([IErrors], ISilence, "should not", "pass")
if (
    registry.lookup([IErrors], ISilence, "should not") == "pass"
    and registry.lookup([IPass], ISilence, "should not") == "pass"
    and registry.lookup([Interface], ISilence, "should not") is None
):
    print(
        "Errors should never require a specification that doesn’t extend "
        "the specification of silence."
    )


# ------------------------------------------------------------------------------
# 11. Unless explicitly silenced.
#
# A multi-adapter adapts several objects at once.
# ------------------------------------------------------------------------------


@implementer(IErrors)
class Errors:
    pass


@implementer(ISilence)
class Silence:
    pass


@implementer(IPass)
@dataclass
class Explicit:
    """Adapts errors and silence, together, to IPass."""

    errors: Errors
    silence: Silence


errors, silence = Errors(), Silence()
registry.register([IErrors, ISilence], IPass, "", Explicit)
explicit = registry.queryMultiAdapter((errors, silence), IPass)
if IPass.providedBy(explicit) and explicit == Explicit(errors, silence):
    print("Unless explicit is a multi-adapter.")


# ------------------------------------------------------------------------------
# 12. In the face of ambiguity, refuse the temptation to guess.
#
# Subscriptions don't pick one registration: a lookup returns all of them.
# ------------------------------------------------------------------------------


class IAmbiguity(Interface):
    """Ambiguity."""


class IGuess(Interface):
    """A guess."""


registry.subscribe([IAmbiguity], IGuess, "refuse the temptation to guess")
if "refuse the temptation to guess" in registry.subscriptions([IAmbiguity], IGuess):
    print(
        "In subscribing to ambiguity, return all the objects that refuse "
        "the temptation to guess."
    )


# ------------------------------------------------------------------------------
# 13. There should be one-- and preferably only one --obvious way to do it.
#
# Subscribers that provide None are handlers: calling subscribers() runs
# them all and throws away whatever they return.
# ------------------------------------------------------------------------------

handled = []


def handler(event):
    handled.append(event)
    return "output"


registry.subscribe([IErrors], None, handler)
if registry.subscribers([errors], None) == () and handled == [errors]:
    print("There should be none-- and preferably only zero --output from a handler.")


# ------------------------------------------------------------------------------
# 14. Although that way may not be obvious at first unless you're Dutch.
#
# Adapter hooks let calling an interface find adapters in your own registry.
# ------------------------------------------------------------------------------


class IFile(Interface):
    body = Attribute("Contents of the file.")


@implementer(IFile)
class File:
    body = "Uniquely communicate economically sound infrastructures"


class ISize(Interface):
    def size():
        """Return the size."""


@implementer(ISize)
@dataclass
class FileSize:
    """Adapts an IFile to ISize."""

    context: File

    def size(self):
        return len(self.context.body)


def hook(provided, ob):
    """Adapt ob to provided using our registry, or return None if we can't."""
    adapter = registry.lookup1(providedBy(ob), provided)
    return adapter(ob) if adapter else None


adapter_hooks.append(hook)
registry.register([IFile], ISize, "", FileSize)
if isinstance(ISize(File()), FileSize):
    print(
        "Although that way may not be obvious at first unless you've "
        "registered an adapter hook."
    )


# ------------------------------------------------------------------------------
# 15. Now is better than never.
#
# verifyObject passes when an object has everything its interface declares.
# ------------------------------------------------------------------------------


class INow(Interface):
    x = Attribute("The X attribute")
    y = Attribute("The Y attribute")


@implementer(INow)
class Never:
    x, y = 1, 2


if verifyObject(INow, Never()):
    print("Now is verified by never.")


# ------------------------------------------------------------------------------
# 16. Although never is often better than *right* now.
#
# ...and fails when something is missing, including what an interface
# inherits.
# ------------------------------------------------------------------------------


class INever(INow):
    """Everything INow has."""


@implementer(INever)
class RightNow:
    x = 1  # but no y


try:
    verifyObject(INever, RightNow())
except BrokenImplementation:
    print("Although never is not implemented by *right* now.")


# ------------------------------------------------------------------------------
# 17. If the implementation is hard to explain, it's a bad idea.
#
# Utilities are objects registered by the interface they provide, and an
# optional name, then looked up from anywhere.
# ------------------------------------------------------------------------------


class IImplementation(Interface):
    def explain():
        """Print an explanation of the implementation."""


@implementer(IImplementation)
@dataclass
class Implementation:
    implementation: str = "easy to explain, it may query the good idea utility."

    def explain(self):
        print("If the implementation is", self.implementation)


provideUtility(
    Implementation("hard to explain, it queries the bad idea utility."),
    IImplementation,
    "bad idea",
)
queryUtility(IImplementation, "bad idea").explain()


# ------------------------------------------------------------------------------
# 18. If the implementation is easy to explain, it may be a good idea.
# ------------------------------------------------------------------------------

provideUtility(Implementation(), IImplementation, "good idea")
queryUtility(IImplementation, "good idea").explain()


# ------------------------------------------------------------------------------
# 19. Namespaces are one honking great idea -- let's do more of those!
#
# Not a ZCA concept, but see https://peps.python.org/pep-0420/
# ------------------------------------------------------------------------------

print(
    "Implicit namespace packages are one honking great idea -- let's do more of those!"
)
