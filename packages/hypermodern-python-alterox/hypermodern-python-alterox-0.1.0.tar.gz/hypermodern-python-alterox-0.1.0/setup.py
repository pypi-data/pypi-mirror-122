# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypermodern_python_alterox']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.13.0,<4.0.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['hypermodern-python-alterox = '
                     'hypermodern_python_alterox.console:main']}

setup_kwargs = {
    'name': 'hypermodern-python-alterox',
    'version': '0.1.0',
    'description': 'The hypermodern Python project',
    'long_description': '[![Tests](https://github.com/alexistli/hypermodern-python/workflows/Tests/badge.svg)](https://github.com/alexistli/hypermodern-python/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/alexistli/hypermodern-python/branch/master/graph/badge.svg)](https://codecov.io/gh/alexistli/hypermodern-python)\n[![PyPI](https://img.shields.io/pypi/v/hypermodern-python-alterox.svg)](https://pypi.org/project/hypermodern-python-alterox/)\n\n# hypermodern-python-alterox\n',
    'author': 'alexistli',
    'author_email': 'alexis.torelli.treanton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alexistli/hypermodern-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
