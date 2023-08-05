# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['packetboat']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'packetboat',
    'version': '0.0.0',
    'description': '',
    'long_description': '',
    'author': 'big-o',
    'author_email': 'big-o@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
