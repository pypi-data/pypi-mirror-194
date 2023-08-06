# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['git_cheater']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'git-cheater',
    'version': '0.0.1',
    'description': 'git-cheater',
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
