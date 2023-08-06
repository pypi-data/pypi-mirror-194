# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devt']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'devt',
    'version': '0.1.0',
    'description': '',
    'long_description': '# devt',
    'author': 'tamuto',
    'author_email': 'mutomob@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
