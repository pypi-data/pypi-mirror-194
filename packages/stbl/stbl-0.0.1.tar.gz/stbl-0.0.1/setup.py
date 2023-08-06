# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['stbl']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stbl',
    'version': '0.0.1',
    'description': 'stbl',
    'long_description': 'None',
    'author': 'HE Yaowen',
    'author_email': 'he.yaowen@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
