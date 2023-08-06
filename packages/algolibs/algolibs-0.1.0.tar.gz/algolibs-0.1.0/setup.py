# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['algolibs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'algolibs',
    'version': '0.1.0',
    'description': '',
    'long_description': '# algolib\npython algo lib\n',
    'author': 'CodeMax',
    'author_email': 'istommao@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
