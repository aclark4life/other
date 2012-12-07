# Based on http://docs.zope.org/zope.interface/README.html
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import implements


class IUgly(Interface):
    """
    """
    beautiful = Attribute("Beautiful is an attribute of ugly")


class IExplicit(Interface):
    """
    """


class Implicit:
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


print "The Zen of Zope, by Alex Clark\n\n"

if 'beautiful' in IUgly:
    print IUgly['beautiful'].__doc__

if IExplicit.implementedBy(Implicit):
    print "Explicit is implemented by implicit"

simple = Complex()
if IComplex.providedBy(simple):
    print "Simple is provided by complex"
