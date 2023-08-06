# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pocpoc',
 'pocpoc.api',
 'pocpoc.api.codec',
 'pocpoc.api.codec.codecs',
 'pocpoc.api.context_tracker',
 'pocpoc.api.di',
 'pocpoc.api.di.adapters',
 'pocpoc.api.logging',
 'pocpoc.api.messages',
 'pocpoc.api.messages.adapters',
 'pocpoc.api.messages.adapters.json',
 'pocpoc.api.messages.adapters.rabbitmq',
 'pocpoc.api.messages.adapters.runtime',
 'pocpoc.api.messages.events',
 'pocpoc.api.messages.rpc',
 'pocpoc.api.microservices',
 'pocpoc.api.microservices.adapters',
 'pocpoc.api.microservices.cli',
 'pocpoc.api.queries',
 'pocpoc.api.storage',
 'pocpoc.api.storage.adapters',
 'pocpoc.api.storage.adapters.sqa',
 'pocpoc.api.storage.uow',
 'pocpoc.api.storage.uow.adapters',
 'pocpoc.api.storage.uow.adapters.sqa',
 'pocpoc.api.utils']

package_data = \
{'': ['*']}

install_requires = \
['click==8.1.3']

extras_require = \
{'debugging': ['colorlog>=6.7.0,<7.0.0'],
 'rabbitmq': ['pika>=1.3.1,<2.0.0'],
 'sqa': ['sqlalchemy>=1.4.44,<2.0.0', 'alembic>=1.8.1,<2.0.0']}

entry_points = \
{'console_scripts': ['pocpoc = pocpoc.api.microservices.cli:cli']}

setup_kwargs = {
    'name': 'pocpoc',
    'version': '0.1.5',
    'description': '',
    'long_description': '# PocPoc\n\n[![PyPI version](https://badge.fury.io/py/pocpoc.svg)](https://badge.fury.io/py/pocpoc)\\\n[![Python version](https://img.shields.io/pypi/pyversions/pocpoc.svg)](https://pypi.python.org/pypi/pocpoc)\n\nA Python library for managing Dependency Injection, Events and Commands, with Redis adapters. It also handles database transactions with the Unit of Work concept using SQLAlchemy adapters.\n\nInstallation\n------------\n\nYou can install the library using pip:\n\npip install pocpoc\n\nFeatures\n--------\n\n- Dependency Injection without decorators\n- Redis adapters for Events and Commands\n- SQLAlchemy adapter for handling database transactions with the Unit of Work concept\n\nDocumentation\n-------------\n\nThe full documentation can be found at [https://pocpoc.readthedocs.io/](https://pocpoc.readthedocs.io/).\n\nContributing\n------------\n\nContributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more information.\n\nLicense\n-------\n\nPocPoc is released under the MIT License. See the [LICENSE](LICENSE) file for more information.\n',
    'author': 'Lucas Silva',
    'author_email': 'lucas76leonardo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
