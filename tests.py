from unittest import TestCase, main

from zope.interface.verify import verifyObject

from other import IPerson, Person


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


if __name__ == "__main__":
    main()
