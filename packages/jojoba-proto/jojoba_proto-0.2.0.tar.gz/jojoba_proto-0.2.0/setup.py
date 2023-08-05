# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jojoba_proto']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-tools>=1.51.1,<2.0.0']

setup_kwargs = {
    'name': 'jojoba-proto',
    'version': '0.2.0',
    'description': '',
    'long_description': '',
    'author': 'Heorhii Torianyk',
    'author_email': 'deadstonepro@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
