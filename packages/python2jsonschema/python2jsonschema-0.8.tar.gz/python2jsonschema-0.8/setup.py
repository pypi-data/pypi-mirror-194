# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python2jsonschema']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.11"': ['typing-extensions>=4.5.0,<5.0.0']}

entry_points = \
{'console_scripts': ['python2jsonschema = python2jsonschema.cli:cli']}

setup_kwargs = {
    'name': 'python2jsonschema',
    'version': '0.8',
    'description': 'Creates a Json Schema File based on Python Types',
    'long_description': '# python2jsonschema\nSimple generate a Json Schema for your Python Classes\n',
    'author': 'Adrian Ehrsam',
    'author_email': 'adrian.ehrsam@bmsuisse.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
