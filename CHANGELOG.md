# Changelog

## 2.1.0 (2026/10/23)

- Declare `zope.interface` as a direct dependency [aclark]
- Add a `dev` dependency group with `prek` [aclark]
- License under MIT [aclark]
- Drop the `that` dependency; it was never imported [aclark]
- Use the full author name, Jeffrey 'Alex' Clark [aclark]
- Convert the README to Markdown and rename `CHANGES.txt` to `CHANGELOG.md` [aclark]
- Run the tests with pytest; add a `test` dependency group [aclark]
- Make `other` a package in a `src` layout, with tests in `tests/` [aclark]
- Reorganize the tutorial so each section defines what it uses [aclark]
- Trim boilerplate from the tutorial: dataclasses instead of assign-only `__init__` methods, one-line docstrings, `size()` instead of `getSize()` [aclark]
- Explain in each section's banner how its line of the Zen becomes ZCA code [aclark]
- Make section 3 literally true: `ISimple` is provided by a `Complex` instance [aclark]
- Drop `MANIFEST.in` and `requirements.txt`; add Python version
  classifiers, keywords and project URLs [aclark]
- Add background, installation and development sections to the README [aclark]
- Fix the adapter hook breaking failed adaptation process-wide after import [aclark]
- Make sections 1, 10, 11 and 13 demonstrate what their lines describe [aclark]
- Test the full output against the README, and the adapter hook fix [aclark]

## 2.0.1 (2026/10/22)

- Replace Gittip URL with GitHub Sponsors `Funding` URL in project metadata [aclark]

## 2.0.0 (2026/10/22)

- Drop Python 2; require Python 3.10+ [aclark]
- Use `@implementer` class decorators instead of `implements()` [aclark]
- Move packaging to `pyproject.toml` [aclark]
- Publish to PyPI with trusted publishing via GitHub Actions [aclark]
- Add tests [aclark]

## 1.0.0 (2012/12/8)

- First release [aclark]
