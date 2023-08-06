# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['taskqueue']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'taskqueue',
    'version': '0.0.0',
    'description': 'An awesome package is coming soon! 🎉',
    'long_description': '<h1 align="center">\n    <strong>taskqueue</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/taskqueue" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/taskqueue" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/taskqueue/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/taskqueue">\n    <br />\n    <a href="https://pypi.org/project/taskqueue" target="_blank">\n        <img src="https://img.shields.io/pypi/v/taskqueue" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/taskqueue">\n    <img src="https://img.shields.io/github/license/Kludex/taskqueue">\n</p>\n\n\n## Installation\n\n``` bash\npip install taskqueue\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/taskqueue',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
