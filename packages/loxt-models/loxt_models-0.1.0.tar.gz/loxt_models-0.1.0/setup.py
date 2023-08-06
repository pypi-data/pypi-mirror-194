# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loxt_models']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'loxt-models',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Pierre Gobin',
    'author_email': 'dev@pierregobin.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
