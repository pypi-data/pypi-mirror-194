# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sabaka']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sabaka',
    'version': '0.1.0',
    'description': 'flexible python error messaging',
    'long_description': '[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![PyPI Latest Release](https://img.shields.io/pypi/v/sabaka.svg)](https://pypi.org/project/sabaka/) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Documentation Status](https://readthedocs.org/projects/sabaka/badge/?version=latest)](http://sabaka.readthedocs.io/?badge=latest)\n\n# What is sabaka?\n\n<p align="center">\n<img src="https://www.indiewire.com/wp-content/uploads/2018/07/NUP_179022_0915.jpg" height="300"/>\n</p>\n\n\n\nIn Belter Creole, in the TV show The Expanse (and in the books on which the show was based), "Sabaka" means ["a general-purpose curse; "Dammit!" or "You bastard!"](https://expanse.fandom.com/wiki/Belter_Creole), a suitable name for an error messaging package. The purpose of **sabaka** is to expand options for error messages beyond passed strings to include:\n\n1. a message composed from passed args and kwargs; and\n2. a default message.\n   \nThis is done by either using one of the included Exception subclasses or by mixing-in one of the mixin classes which add other messaging options to Python\'s base exceptions.\n\n# Examples\n\n# API\n\n## Exceptions\n\n\n## Exception Mixins\n\n\n# Contributing \n\nContributors are always welcome and should find **sabaka** easy to work with. The project is highly documented so that users and developers can make **sabaka** work with their projects. It is designed for Python coders at all levels. Beginners should be able to follow the readable code and internal documentation to understand how it works. More advanced users should find complex and tricky problems addressed through efficient code.\n',
    'author': 'Corey Rayburn Yung',
    'author_email': 'coreyrayburnyung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/WithPrecedent/sabaka',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
