# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cgepy', 'cgepy.ext', 'cgepy.ext.beta']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cgepy',
    'version': '0.7.0',
    'description': 'Tools for developing graphical programs inside the console.',
    'long_description': '### cgepy // 0.7.0\n###### A simple graphics engine with no dependencies.\n***\ncgePy, or cge, is a text-based graphics engine that can operate in the console or terminal.\\\nCurrently with zero dependencies, a simple system that can suit many needs, and easily tweaked settings, cgePy will allow you to turn ideas into reality.\n',
    'author': 'catbox305',
    'author_email': 'lion712yt@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
