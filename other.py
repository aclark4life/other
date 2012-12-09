# encoding: utf-8
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import directlyProvides
from zope.interface import directlyProvidedBy
from zope.interface import implementedBy
from zope.interface import implements
from zope.interface import implementsOnly
from zope.interface import invariant
from zope.interface import providedBy
from zope.interface.adapter import AdapterRegistry
from zope.interface.exceptions import BrokenImplementation
from zope.interface.interface import adapter_hooks
from zope.interface.verify import verifyObject

from zope.component import provideUtility
from zope.component import queryUtility

TITLE = "The Zen of Zope, by Alex Clark"

# This is a crash course on the Zope Component Architecture (ZCA), based on
# http://docs.zope.org/zope.interface/README.html and
# http://docs.zope.org/zope.component/index.html, and heavily inspired by
# The Anti-Zen of Python, by Daniel Greenfeld and
# The Zen of Python, by Tim Peters.
# Special thanks to Guido Van Rossum for Python, and Jim Fulton for Zope.
# Copyright (C) 2012 Alex Clark
# All rights reserved


__gittip_url__ = "https://www.gittip.com/aclark4life/"


class IUgly(Interface):
    """
    """
    beautiful = Attribute("Beautiful is an attribute of ugly.")


class IExplicit(Interface):
    """
    """


class Implicit(object):
    """
    """
    implements(IExplicit)


class IComplex(Interface):
    """
    """


class Complex:
    """
    """
    implements(IComplex)


class Complicated:
    """
    """


class INested(Interface):
    """
    """


class Nested:
    """
    """
    implements(INested)


class Flat(Complex):
    """
    """
    implementsOnly(INested)


class ISparse(Interface):
    """
    """


class RangeError(Invalid):
    """
    """
    def __repr__(self):
        """
        """
        return "RangeError(%r)" % self.args


def range_invariant(ob):
    """
    """
    if ob.max < ob.min:
        raise RangeError(ob)


class IRange(Interface):
    """
    """
    min = Attribute("Lower bound")
    max = Attribute("Upper bound")
    invariant(range_invariant)


class Range(object):
    """
    """
    implements(IRange)

    def __init__(self, min, max):
        """
        """
        self.min, self.max = min, max

    def __repr__(self):
        """
        """
        return "Range(%s, %s)" % (self.min, self.max)


class ISpecialCases(Interface):
    """
    """
    pass


class IPurity(Interface):
    """
    """
    pass


class Practicality(object):
    """
    """
    implements(IPurity)


class IErrors(Interface):
    """
    """
    pass


class ISilence(Interface):
    """
    """
    pass


class IPass(IErrors):
    """
    """
    pass


class Errors:
    """
    """
    implements(IErrors)


class Silence:
    """
    """
    implements(ISilence)


class Explicit:
    implements(IExplicit)

    def __init__(self, errors, silence):
        """
        """
        self.errors, self.silence = errors, silence


class IAmbiguity(Interface):
    """
    """
    pass


class IGuess(Interface):
    """
    """
    pass


def handler(event):
    """
    """
    print 'handler', event


class IFile(Interface):
    """
    """
    body = Attribute('Contents of the file.')


class File(object):
    """
    """
    implements(IFile)
    body = "Uniquely communicate economically sound infrastructures"


def hook(provided, object):
    """
    """
    adapter = registry.lookup1(providedBy(object), provided, '')
    return adapter(object)


class ISize(Interface):
    """
    """

    def getSize():
        """
        """


class FileSize(object):
    """
    """
    implements(ISize)

    def __init__(self, context):
        """
        """
        self.context = context

    def getSize(self):
        """
        """
        return len(self.context.body)


class INow(Interface):
    """
    """
    x = Attribute("The X attribute")
    y = Attribute("The Y attribute")


class INever(INow):
    """
    """


class Never(object):
    """
    """
    implements(INow)
    x = 1

    def __init__(self):
        self.y = 2


class RightNow(object):
    implements(INever)
    x = 1


class IImplementation(Interface):
    """
    """
    def explain():
        """
        """


class Implementation:
    """
    """
    implements(IImplementation)

    def __init__(self, implementation="easy to explain, it may query the "
        "good idea utility."):
        """
        """
        self.implementation = implementation

    def explain(self):
        """
        """
        print "If the implementation is", self.implementation


#------------------------------------------------------------------------------


print "%s\n\n" % TITLE


# 1) Beautiful is better than ugly.
if 'beautiful' in IUgly:
    print IUgly['beautiful'].__doc__


# 2) Explicit is better than implicit.
if IExplicit.implementedBy(Implicit):
    print "Explicit is implemented by implicit."


# 3) Simple is better than complex.
simple = Complex()
if IComplex.providedBy(simple):
    print "Simple is provided by complex."


# 4) Complex is better than complicated.
complicated = Complicated()
directlyProvides(complicated, IComplex)
for interface in directlyProvidedBy(complicated).interfaces():
    if interface.getName() == 'IComplex':
        print "Complex is directly provided by complicated."


# 5) Flat is better than nested.
interfaces = [interface for interface in implementedBy(Flat).interfaces()]
if len(interfaces) == 1:
    if interfaces[0].getName() == 'INested':
        print "Flat only implements nested."


# 6) Sparse is better than dense.
ISparse.setTaggedValue('dense', 'Sparse has tagged value dense.')
tags = ISparse.getTaggedValueTags()
if 'dense' in tags:
    print ISparse.getTaggedValue('dense')


# 7) Readability counts.
try:
    IRange.validateInvariants(Range(2, 1))
except RangeError:
    print "Readability count is not in range."


# 8) Special cases aren't special enough to break the rules.
try:
    ISpecialCases('the rules')
except TypeError:
    print "Special cases could not adapt the rules."


# 9) Although practicality beats purity.
practicality = Practicality()
if IPurity(practicality) is practicality:
    print "Practicality implements purity."


# 10) Errors should never pass silently.
# Register an object that depends on IErrors and provides ISilence
registry = AdapterRegistry()  # XXX Logic below is not quite right
registry.register([IErrors], ISilence, 'should not', 'pass')
if (registry.lookup([IErrors], ISilence, 'should not') == 'pass' and
    registry.lookup([Interface], ISilence) is None):
    print ("Errors should never require a specification that doesn’t extend "
        "the specification of silence.")


# 11) Unless explicitly silenced.
errors = Errors()
silence = Silence()
registry.register([IErrors, ISilence], IPass, '', Explicit)
explicit = registry.queryMultiAdapter((errors, silence), IPass)
if (explicit.__class__.__name__ == "Explicit" and
    explicit.errors is errors and explicit.silence is silence):
    print "Unless explicit is a multi-adapter."


# 12) In the face of ambiguity, refuse the temptation to guess.
registry.subscribe([IAmbiguity], IGuess, 'refuse the temptation to guess')
if 'refuse the temptation to guess' in [sub for sub in
    registry.subscriptions([IAmbiguity], IGuess)]:
    print ("In subscribing to ambiguity, return all the objects that refuse "
        "the temptation to guess.")


# 13) There should be one-- and preferably only one --obvious way to do it.
registry.subscribe([IErrors], None, handler)
if registry.subscriptions([IErrors], None) == [handler]:
    print ("There should be none-- and preferably only zero --output from a "
         "handler.")


# 14) Although that way may not be obvious at first unless you're Dutch.
adapter_hooks.append(hook)
registry.register([IFile], ISize, '', FileSize)
f = File()
size = ISize(f)
if registry.lookup1(IFile, ISize, '')(f).getSize() == size.getSize():
    print ("Although that way may not be obvious at first unless you've "
         "registered an adapter hook")


# 15) Now is better than never.
never = Never()
if verifyObject(INow, never):
    print "Now is verified by never."


# 16) Although never is often better than *right* now.
right_now = RightNow()
try:
    verifyObject(INever, right_now)
except BrokenImplementation:
    print "Although never is not implemented by *right* now."


# 17) If the implementation is hard to explain, it's a bad idea.
bad_idea = Implementation("hard to explain, it queries the bad idea "
    "utility.")  # XXX Logic?
provideUtility(bad_idea, IImplementation, 'bad idea')
queryUtility(IImplementation, 'bad idea').explain()


# 18) If the implementation is easy to explain, it may be a good idea.
good_idea = Implementation()  # XXX Logic?
provideUtility(good_idea, IImplementation, 'good idea')
queryUtility(IImplementation, 'good idea').explain()


# 19) Namespaces are one honking great idea -- let's do more of those!
print "Implicit namespace packages are one honking great idea -- let's do more of those!"
