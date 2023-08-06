# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rfw_lightning']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rfw-lightning',
    'version': '0.0.1',
    'description': 'Robot Framework Lightning',
    'long_description': '',
    'author': 'RPA Framework',
    'author_email': 'rpafw@robocorp.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
