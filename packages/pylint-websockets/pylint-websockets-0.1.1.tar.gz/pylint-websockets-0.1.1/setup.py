# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylint_websockets']

package_data = \
{'': ['*']}

install_requires = \
['pylint', 'websockets']

setup_kwargs = {
    'name': 'pylint-websockets',
    'version': '0.1.1',
    'description': 'A Pylint plugin for the Python websockets library',
    'long_description': "# Pylint Websockets\n\nA pylint plugin for websockets\n\n## Installation\n\nVia Pip\n\n```\npip install pylint-websockets\n```\n\nVia Poetry\n\n```\npoetry add --dev pylint-websockets\n```\n\n## Usage\n\nAdd the following arguments when running Pylint:\n\n```\n--load-plugins=pylint_websockets\n```\n\nAlternatively, add the following to your `pyproject.toml`:\n\n```toml\n[tool.pylint.MASTER]\nload-plugins = 'pylint_websockets'\n```\n",
    'author': 'Bryan Hu',
    'author_email': 'bryan.hu.2020@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ThatXliner/pylint-pylint-websockets',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
