# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['margincropper']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.4.0,<10.0.0']

setup_kwargs = {
    'name': 'margincropper',
    'version': '1.0.1',
    'description': 'Crops margins from PIL images',
    'long_description': None,
    'author': 'megahomyak',
    'author_email': 'g.megahomyak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
