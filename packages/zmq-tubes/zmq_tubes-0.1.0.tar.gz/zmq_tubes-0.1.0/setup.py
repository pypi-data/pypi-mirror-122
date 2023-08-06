# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zmq_tubes']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'pyzmq>=22.2.1,<23.0.0']

setup_kwargs = {
    'name': 'zmq-tubes',
    'version': '0.1.0',
    'description': 'Wrapper for ZMQ comunication.',
    'long_description': None,
    'author': 'Martin Korbel',
    'author_email': 'mkorbel@alps.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
