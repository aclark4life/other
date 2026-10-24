import re
import subprocess
import sys
from pathlib import Path
from unittest import TestCase, main

from zope.interface import Interface
from zope.interface.verify import verifyObject

from other import IPerson, Person

HERE = Path(__file__).parent


def readme_output():
    """
    Return the sample output shown in the README's Usage section.
    """
    readme = (HERE / "README.rst").read_text(encoding="utf-8")
    match = re.search(r"\$ python -m other\n(.*?)\n\n(?=\S)", readme, re.DOTALL)
    block = match.group(1)
    return "\n".join(line.removeprefix("    ") for line in block.splitlines())


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

    def test_output_matches_readme(self):
        """
        Every section prints its line only if its check passes, so the full
        output matching the README means all 19 demonstrations work.
        """
        result = subprocess.run(
            [sys.executable, "-m", "other"],
            capture_output=True,
            check=True,
            cwd=HERE,
            encoding="utf-8",
        )
        self.assertEqual(result.stdout.rstrip("\n"), readme_output())

    def test_failed_adaptation_still_raises(self):
        """
        The adapter hook installed on import must not break adaptation
        elsewhere: a failed adaptation still raises 'Could not adapt'.
        """

        class IUnrelated(Interface):
            pass

        with self.assertRaises(TypeError) as cm:
            IUnrelated(object())
        self.assertEqual(cm.exception.args[0], "Could not adapt")


if __name__ == "__main__":
    main()
