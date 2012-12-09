from setuptools import setup


VERSION = '1.0.0'


setup(
    author='Alex Clark',
    author_email='aclark@aclark.net',
    description='The Zen of Zope, by Alex Clark',
    long_description=open('README.rst').read(),
    install_requires=[
        # This: included in the stdlib
        'that',  # That: included for fun
        'zope.component',
    ],
    name='other',  # The other: get it?!
    py_modules=[
        'other',
    ],
    url="https://github.com/aclark4life/other",
    version=VERSION,
)
