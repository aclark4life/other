# Based on http://docs.zope.org/zope.interface/README.html
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import directlyProvides
from zope.interface import directlyProvidedBy
from zope.interface import implementedBy
from zope.interface import implements
from zope.interface import implementsOnly
from zope.interface import invariant


#The Zen of Python, by Tim Peters
#
#Beautiful is better than ugly.
#Explicit is better than implicit.
#Simple is better than complex.
#Complex is better than complicated.
#Flat is better than nested.
#Sparse is better than dense.
#Readability counts.
#Special cases aren't special enough to break the rules.
#Although practicality beats purity.
#Errors should never pass silently.
#Unless explicitly silenced.
#In the face of ambiguity, refuse the temptation to guess.
#There should be one-- and preferably only one --obvious way to do it.
#Although that way may not be obvious at first unless you're Dutch.
#Now is better than never.
#Although never is often better than *right* now.
#If the implementation is hard to explain, it's a bad idea.
#If the implementation is easy to explain, it may be a good idea.
#Namespaces are one honking great idea -- let's do more of those!


class IUgly(Interface):
    """
    """
    beautiful = Attribute("Beautiful is an attribute of ugly")


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
        return "RangeError(%r)" % self.args


def range_invariant(ob):
    if ob.max < ob.min:
        raise RangeError(ob)


class IRange(Interface):
    min = Attribute("Lower bound")
    max = Attribute("Upper bound")
    invariant(range_invariant)


class Range(object):
    implements(IRange)

    def __init__(self, min, max):
        self.min, self.max = min, max

    def __repr__(self):
        return "Range(%s, %s)" % (self.min, self.max)


class ISpecialCases(Interface):
    pass


class IPurity(Interface):
    pass


class Practicality(object):
    implements(IPurity)


#-------------------------------------------------------------------------------


print "The Zen of Zope, by Alex Clark\n\n"

# 1)
if 'beautiful' in IUgly:
    print IUgly['beautiful'].__doc__

# 2)
if IExplicit.implementedBy(Implicit):
    print "Explicit is implemented by implicit"

# 3)
simple = Complex()
if IComplex.providedBy(simple):
    print "Simple is provided by complex"

# 4)
complicated = Complicated()
directlyProvides(complicated, IComplex)
for interface in directlyProvidedBy(complicated).interfaces():
    if interface.getName() == 'IComplex':
        print "Complex is directly provided by complicated"

# 5)
interfaces = [interface for interface in implementedBy(Flat).interfaces()]
if len(interfaces) == 1:
    if interfaces[0].getName() == 'INested':
        print "Flat only implements nested"

# 6)
ISparse.setTaggedValue('dense', 'Sparse has tagged value dense')
tags = ISparse.getTaggedValueTags()
if 'dense' in tags:
    print ISparse.getTaggedValue('dense')


# 7)
try:
    IRange.validateInvariants(Range(2,1))
except RangeError:
    print "Readability count is not in range"

# 8)
try:
    ISpecialCases('break the rules')
except TypeError:
    print "Special cases could not adapt break the rules"

# 9)
practicality = Practicality()
if IPurity(practicality) is practicality:
    print "Practicality implements purity"
