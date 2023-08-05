# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['carly']

package_data = \
{'': ['*']}

install_requires = \
['Twisted>=21.7', 'attrs']

setup_kwargs = {
    'name': 'carly',
    'version': '0.12.0',
    'description': 'A tool for putting messages into and collecting responses from Twisted servers using real networking',
    'long_description': 'carly\n=====\n\n|CircleCI|_\n\n.. |CircleCI| image:: https://circleci.com/gh/cjw296/carly/tree/master.svg?style=shield\n.. _CircleCI: https://circleci.com/gh/cjw296/carly/tree/master\n\n\nA tool for putting messages into and collecting responses from Twisted servers and clients using real networking.\n\n"call me maybe"\n\nWhy carly? \'cos someone already took `Jepsen!`__\n\n__ https://jepsen.io/\n',
    'author': 'Chris Withers',
    'author_email': 'chris@withers.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cjw296/carly',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.7',
}


setup(**setup_kwargs)
