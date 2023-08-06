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
['alembic[sqlalchemy]>=1.8.1,<2.0.0',
 'colorlog[debugging]>=6.7.0,<7.0.0',
 'pika[rabbitmq]>=1.3.1,<2.0.0',
 'sqlalchemy[sqlalchemy]>=1.4.44,<2.0.0']

entry_points = \
{'console_scripts': ['pocpoc = pocpoc.api.microservices.cli:cli']}

setup_kwargs = {
    'name': 'pocpoc',
    'version': '0.1.0',
    'description': '',
    'long_description': '# POCPOC Tools 🛠️\n',
    'author': 'Lucas Silva',
    'author_email': 'lucas76leonardo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
