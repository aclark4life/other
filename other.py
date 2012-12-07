# Based on http://docs.zope.org/zope.interface/README.html
import zope.interface




class IBeautiful(zope.interface.Interface):
    """A Beautiful interface"""

    ugly = zope.interface.Attribute("""Ugly is an attribute of Beautiful""")




print "The Zen of Zope, by Alex Clark\n\n"


beautiful = IBeautiful['ugly']
print beautiful.__doc__
