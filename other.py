"""
The Zen of Zope: a crash course on the Zope Component Architecture (ZCA),
told through the aphorisms of The Zen of Python. Run it to print them.
"""

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

# This is a crash course on the Zope Component Architecture (ZCA), based on
# http://docs.zope.org/zope.interface/README.html and
# http://docs.zope.org/zope.component/index.html, and heavily inspired by
# The Anti-Zen of Python, by Daniel Greenfeld and
# The Zen of Python, by Tim Peters.
# Special thanks to Guido Van Rossum for Python, and Jim Fulton for Zope.
# Copyright (C) 2012 Alex Clark
# Released under the MIT License; see LICENSE.


class Complicated:
    """
    A plain class that implements nothing; its instances are later made to
    provide IComplex directly.
    """


class INested(Interface):
    """
    Marker interface that Flat implements to the exclusion of all others.
    """


class ISparse(Interface):
    """
    Marker interface used to demonstrate tagged values.
    """


class RangeError(Invalid):
    """
    Raised when a range's upper bound is less than its lower bound.
    """

    def __repr__(self):
        """
        Return a representation including the offending object.
        """
        return f"RangeError({self.args[0]!r})"


def range_invariant(ob):
    """
    Invariant for IRange: raise RangeError if ob.max is less than ob.min.
    """
    if ob.max < ob.min:
        raise RangeError(ob)


class IRange(Interface):
    """
    A range with lower and upper bounds, constrained by range_invariant.
    """

    min = Attribute("Lower bound")
    max = Attribute("Upper bound")
    invariant(range_invariant)


@implementer(IRange)
class Range:
    """
    A simple range implementing IRange.
    """

    def __init__(self, min, max):
        """
        Store the lower and upper bounds.
        """
        self.min, self.max = min, max

    def __repr__(self):
        """
        Return a representation showing both bounds.
        """
        return f"Range({self.min}, {self.max})"


class ISpecialCases(Interface):
    """
    Interface with no adapters registered, so adapting to it fails.
    """


class IPurity(Interface):
    """
    Interface implemented by Practicality.
    """


@implementer(IPurity)
class Practicality:
    """
    Implements IPurity, so adapting it to IPurity returns itself.
    """


class IErrors(Interface):
    """
    Interface for errors; required by the adapters and subscribers below.
    """


class ISilence(Interface):
    """
    Interface for silence; provided by the 'should not' registration.
    """


class IPass(IErrors):
    """
    Interface provided by the Explicit multi-adapter of errors and silence.
    """


@implementer(IErrors)
class Errors:
    """
    A class that implements IErrors.
    """


@implementer(ISilence)
class Silence:
    """
    A class that implements ISilence.
    """


@implementer(IPass)
class Explicit:
    """
    Multi-adapter of errors and silence, registered to provide IPass.
    """

    def __init__(self, errors, silence):
        """
        Store the adapted errors and silence objects.
        """
        self.errors, self.silence = errors, silence


class IAmbiguity(Interface):
    """
    Interface required by the subscription that refuses to guess.
    """


class IGuess(Interface):
    """
    Interface provided by the subscription that refuses to guess.
    """


handled = []


def handler(event):
    """
    Event handler subscribed for IErrors; records the event it receives.
    Its return value is discarded, as handlers' always are.
    """
    handled.append(event)
    return "output"


class IFile(Interface):
    """
    A file with a body.
    """

    body = Attribute("Contents of the file.")


@implementer(IFile)
class File:
    """
    A file implementing IFile with a fixed body.
    """

    body = "Uniquely communicate economically sound infrastructures"


def hook(provided, object):
    """
    Adapter hook: look up an adapter from what object provides to the
    provided interface in the local registry and apply it to object.
    Return None when there is no adapter, so other hooks get a turn.
    """
    adapter = registry.lookup1(providedBy(object), provided, "")
    if adapter is not None:
        return adapter(object)
    return None


class ISize(Interface):
    """
    Something that knows its size.
    """

    def getSize():
        """
        Return the size.
        """


@implementer(ISize)
class FileSize:
    """
    Adapts an IFile to ISize.
    """

    def __init__(self, context):
        """
        Store the adapted file as the context.
        """
        self.context = context

    def getSize(self):
        """
        Return the length of the file's body.
        """
        return len(self.context.body)


class INow(Interface):
    """
    Interface with x and y attributes, used to demonstrate verifyObject.
    """

    x = Attribute("The X attribute")
    y = Attribute("The Y attribute")


class INever(INow):
    """
    Extends INow, so implementers must also provide x and y.
    """


@implementer(INow)
class Never:
    """
    Correctly implements INow: x on the class, y on the instance.
    """

    x = 1

    def __init__(self):
        """
        Set the y attribute.
        """
        self.y = 2


@implementer(INever)
class RightNow:
    """
    Claims to implement INever but lacks y, so verifyObject fails.
    """

    x = 1


class IImplementation(Interface):
    """
    An implementation that can explain itself.
    """

    def explain():
        """
        Print an explanation of the implementation.
        """


@implementer(IImplementation)
class Implementation:
    """
    An IImplementation registered as a utility below.
    """

    def __init__(
        self, implementation="easy to explain, it may query the good idea utility."
    ):
        """
        Store the description of the implementation.
        """
        self.implementation = implementation

    def explain(self):
        """
        Print the description of the implementation.
        """
        print("If the implementation is", self.implementation)


# ------------------------------------------------------------------------------


print("The Zen of Zope, by Alex Clark\n\n")


# 1) Beautiful is better than ugly.

# Interfaces are objects that specify the behavior of objects that
# provide them, through:
#     - Informal documentation e.g. doc strings
#     - Attribute definitions
#     - Invariants, which are conditions that must hold true for
#         an object to provide an interface


class IPerson(Interface):
    """
    A person, who is beautiful.
    """

    beautiful = Attribute("Beautiful is an attribute of person.")


@implementer(IPerson)
class Person:
    """
    A person implementing IPerson.
    """

    beautiful = True


person = Person()
if verifyObject(IPerson, person):
    print(IPerson["beautiful"].__doc__)


# 2) Explicit is better than implicit.
class IExplicit(Interface):
    """
    We say that objects provide interfaces. If an object provides an interface
    then the interface specifies the behavior of the object. In other words,
    interfaces specify the behavior of the objects that provide them.
    """


@implementer(IExplicit)
class Implicit:
    """
    We normally say that classes implement interfaces. If a class implements an
    interface, then the instances of the class provide the interface. Objects
    provide interfaces that their classes implement [2]. (Objects can provide
    interfaces directly, in addition to what their classes implement.)
    """


if IExplicit.implementedBy(Implicit):
    print("Explicit is implemented by implicit.")


# 3) Simple is better than complex.
class IComplex(Interface):
    """
    Interface implemented by Complex and directly provided by complicated.
    """


@implementer(IComplex)
class Complex:
    """
    A class that implements IComplex.
    """


simple = Complex()
if IComplex.providedBy(simple):
    print("Simple is provided by complex.")


# 4) Complex is better than complicated.
complicated = Complicated()
directlyProvides(complicated, IComplex)
for interface in directlyProvidedBy(complicated).interfaces():
    if interface.getName() == "IComplex":
        print("Complex is directly provided by complicated.")


# 5) Flat is better than nested.
@implementer_only(INested)
class Flat(Complex):
    """
    Subclasses Complex but implements only INested, not IComplex.
    """


interfaces = [interface for interface in implementedBy(Flat).interfaces()]
if len(interfaces) == 1 and interfaces[0].getName() == "INested":
    print("Flat only implements nested.")


# 6) Sparse is better than dense.
ISparse.setTaggedValue("dense", "Sparse has tagged value dense.")
tags = ISparse.getTaggedValueTags()
if "dense" in tags:
    print(ISparse.getTaggedValue("dense"))


# 7) Readability counts.
try:
    IRange.validateInvariants(Range(2, 1))
except RangeError:
    print("Readability count is not in range.")


# 8) Special cases aren't special enough to break the rules.
try:
    ISpecialCases("the rules")
except TypeError:
    print("Special cases could not adapt the rules.")


# 9) Although practicality beats purity.
practicality = Practicality()
if IPurity(practicality) is practicality:
    print("Practicality implements purity.")


# 10) Errors should never pass silently.
# Register a value that requires IErrors and provides ISilence. Lookups
# find it for specifications that extend IErrors (IPass does), but not for
# ones that don't (Interface, which IErrors extends, not the other way round).
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


# 11) Unless explicitly silenced.
errors = Errors()
silence = Silence()
registry.register([IErrors, ISilence], IPass, "", Explicit)
explicit = registry.queryMultiAdapter((errors, silence), IPass)
if (
    IPass.providedBy(explicit)
    and explicit.errors is errors
    and explicit.silence is silence
):
    print("Unless explicit is a multi-adapter.")


# 12) In the face of ambiguity, refuse the temptation to guess.
registry.subscribe([IAmbiguity], IGuess, "refuse the temptation to guess")
if "refuse the temptation to guess" in [
    sub for sub in registry.subscriptions([IAmbiguity], IGuess)
]:
    print(
        "In subscribing to ambiguity, return all the objects that refuse "
        "the temptation to guess."
    )


# 13) There should be one-- and preferably only one --obvious way to do it.
# Subscribers that provide None are handlers: calling subscribers() runs
# them all and throws away whatever they return.
registry.subscribe([IErrors], None, handler)
if registry.subscribers((errors,), None) == () and handled == [errors]:
    print("There should be none-- and preferably only zero --output from a handler.")


# 14) Although that way may not be obvious at first unless you're Dutch.
adapter_hooks.append(hook)
registry.register([IFile], ISize, "", FileSize)
f = File()
size = ISize(f)
if registry.lookup1(IFile, ISize, "")(f).getSize() == size.getSize():
    print(
        "Although that way may not be obvious at first unless you've "
        "registered an adapter hook."
    )


# 15) Now is better than never.
never = Never()
if verifyObject(INow, never):
    print("Now is verified by never.")


# 16) Although never is often better than *right* now.
right_now = RightNow()
try:
    verifyObject(INever, right_now)
except BrokenImplementation:
    print("Although never is not implemented by *right* now.")


# 17) If the implementation is hard to explain, it's a bad idea.
bad_idea = Implementation(
    "hard to explain, it queries the bad idea utility."
)  # XXX Logic?
provideUtility(bad_idea, IImplementation, "bad idea")
queryUtility(IImplementation, "bad idea").explain()


# 18) If the implementation is easy to explain, it may be a good idea.
good_idea = Implementation()  # XXX Logic?
provideUtility(good_idea, IImplementation, "good idea")
queryUtility(IImplementation, "good idea").explain()


# 19) Namespaces are one honking great idea -- let's do more of those!
# http://www.python.org/dev/peps/pep-0420/
print(
    "Implicit namespace packages are one honking great idea -- let's do more of those!"
)
