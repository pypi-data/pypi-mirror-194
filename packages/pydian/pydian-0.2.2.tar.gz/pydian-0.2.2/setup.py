# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydian', 'pydian.lib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydian',
    'version': '0.2.2',
    'description': 'Library for pythonic data interchange',
    'long_description': 'None',
    'author': 'Eric Pan',
    'author_email': 'eric.pan@canvasmedical.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
