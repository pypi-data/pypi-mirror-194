# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['algolibs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'algolibs',
    'version': '0.1.3',
    'description': '',
    'long_description': '# algolibs\npython algo libs\n\n## TODO\n\n- [x] Linked List\n    - [x] Remove nth from end\n    - [x] Linked list has cycle\n    - [x] Detect linked list cycle entry point\n- [x] Stack\n    - [x] MinStack\n- [ ] Queue\n- [ ] Binary Tree\n',
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
