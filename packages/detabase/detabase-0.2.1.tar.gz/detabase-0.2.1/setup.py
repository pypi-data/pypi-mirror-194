# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['detabase']

package_data = \
{'': ['*']}

install_requires = \
['deta[async]==1.1.0a2', 'starlette>=0.25.0,<0.26.0']

setup_kwargs = {
    'name': 'detabase',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'Daniel Arantes',
    'author_email': 'arantesdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
