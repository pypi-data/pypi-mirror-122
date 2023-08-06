# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['donordrivepython', 'donordrivepython.api', 'donordrivepython.api.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0', 'rich>=10.12.0,<11.0.0', 'xdgenvpy>=2.3.5,<3.0.0']

setup_kwargs = {
    'name': 'donordrivepython',
    'version': '1.0.0',
    'description': 'A utility to access the DonorDrive API',
    'long_description': None,
    'author': 'Eric Mesa',
    'author_email': 'ericsbinaryworld@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
