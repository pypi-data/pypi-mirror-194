# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nsg_octopart']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'nsg-parts-search',
    'version': '0.0.1',
    'description': 'NSG class for making parts searches in Octopart using the Nexar API v4',
    'long_description': '# nsg-parts-search\nOficial repository for NSG Parts Search service\n',
    'author': 'Antonio Arroyave',
    'author_email': 'antonio.arroyave@nsg-engineering.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
