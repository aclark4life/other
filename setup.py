from setuptools import setup


VERSION = '1.0.0'


setup(
    install_requires=[
        'zope.component',
#        'this',  # This. Included in stdlib
        'that',  # That. Included for reference
    ],
    name='other',  # The other! Get it?
    py_modules=[
        'other',  
    ],
    version=VERSION,
)
