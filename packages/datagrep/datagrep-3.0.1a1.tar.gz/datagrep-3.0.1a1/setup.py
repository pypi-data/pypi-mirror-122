# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datagrep', 'datagrep.platform']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.3,<0.4']

entry_points = \
{'console_scripts': ['datagrep = datagrep.main:app',
                     'dgp = datagrep.platform.main:app']}

setup_kwargs = {
    'name': 'datagrep',
    'version': '3.0.1a1',
    'description': 'The datagrep CLI.',
    'long_description': '# datagrep\n\nThe datagrep CLI.\n',
    'author': 'Michael Schock',
    'author_email': 'm@mjschock.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
