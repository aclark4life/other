from other import IPerson
from other import Person
from unittest import TestCase
from unittest import main
from zope.interface.verify import verifyObject


class TestSuite(TestCase):  # Not really a test suite
    """
    Tests for the objects defined in other.py.
    """

    def test_beautiful(self):
        """
        Verify object has a beautiful attribute
        """
        person = Person()
        self.assertTrue(verifyObject(IPerson, person))


if __name__ == '__main__':
    main()
