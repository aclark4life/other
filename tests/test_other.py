import re
import subprocess
import sys
from pathlib import Path

import pytest
from zope.interface import Interface
from zope.interface.verify import verifyObject

from other import IPerson, Person

ROOT = Path(__file__).parent.parent


def readme_output():
    """
    Return the sample output shown in the README's Usage section.
    """
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    match = re.search(r"\$ python -m other\n(.*?)\n```", readme, re.DOTALL)
    return match.group(1)


def test_beautiful():
    assert verifyObject(IPerson, Person())


def test_output_matches_readme():
    """
    Every section prints its line only if its check passes, so the full
    output matching the README means all 19 demonstrations work.
    """
    result = subprocess.run(
        [sys.executable, "-m", "other"],
        capture_output=True,
        check=True,
        cwd=ROOT,
        encoding="utf-8",
    )
    assert result.stdout.rstrip("\n") == readme_output()


def test_failed_adaptation_still_raises():
    """
    The adapter hook installed on import must not break adaptation
    elsewhere: a failed adaptation still raises 'Could not adapt'.
    """

    class IUnrelated(Interface):
        pass

    with pytest.raises(TypeError) as excinfo:
        IUnrelated(object())
    assert excinfo.value.args[0] == "Could not adapt"
