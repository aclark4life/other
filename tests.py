from other import IUgly
from unittest import TestCase
from unittest import main
from zope.interface import implements
from zope.interface.verify import verifyObject


class Dude:
    """
    """
    implements(IUgly)
    beautiful = False


class TestSuite(TestCase):  # Not really a test suite
    """
    """

    def test_ugly(self):
        """
        Verify the dude object has a beautiful attribute
        """
        dude = Dude()
        verifyObject(IUgly, dude)


if __name__ == '__main__':
    main()
