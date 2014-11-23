#!/usr/bin/env python
from setuptools import setup

version = '0.1'

packages = [
    'goattower',
]

setup(name='goattower',
    version=version,
    description="Goats. In a tower. Text.",
    long_description="",
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='irc bot redis service',
    author='Kyle Terry',
    author_email='kyle@kyleterry.com',
    url='https://github.com/kyleterry/tenyks-service',
    license='LICENSE',
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'psycopg2',
        'sqlalchemy'
    ],
)
