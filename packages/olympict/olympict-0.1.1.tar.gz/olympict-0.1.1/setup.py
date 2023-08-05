# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['olympict', 'olympict.files']

package_data = \
{'': ['*']}

install_requires = \
['olympipe>=1.0.3', 'opencv-python>=4.6.0.66,<5.0.0.0']

setup_kwargs = {
    'name': 'olympict',
    'version': '0.1.1',
    'description': 'A powerful parallel pipelining tool for image processing',
    'long_description': '# Olympict\n\n![coverage](https://gitlab.com/superjambon/olympict/badges/master/coverage.svg?job=tests)![status](https://gitlab.com/superjambon/olympict/badges/master/pipeline.svg)\n\n![Olympict](https://gitlab.com/superjambon/olympict/-/raw/master/Olympict.png)\n\n\nThis project will make image processing pipelines \neasy to use using the basic multiprocessing module. This module uses type checking to ensure your data process validity from the start.\n\n',
    'author': 'GKasser',
    'author_email': 'gabriel.kasser@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/gabraken/olympict',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
