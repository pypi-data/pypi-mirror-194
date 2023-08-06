# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['habboapps']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'habboapps',
    'version': '0.1.0',
    'description': '',
    'long_description': 'habbo extension interface for Python',
    'author': 'habbo hotel',
    'author_email': 'habbo@habbohotel.com.br',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
