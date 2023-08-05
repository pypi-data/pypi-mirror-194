# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_duality']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.2', 'typing-extensions>=4.4.0']

setup_kwargs = {
    'name': 'pydantic-duality',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'Stanislav Zmiev',
    'author_email': 'szmiev2000@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
