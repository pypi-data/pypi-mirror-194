# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unigo',
 'unigo.api',
 'unigo.api.store',
 'unigo.api.store.cache',
 'unigo.api.store.client',
 'unigo.repl',
 'unigo.repl.commands',
 'unigo.stats',
 'unigo.test',
 'unigo.tree',
 'unigo.utils']

package_data = \
{'': ['*'], 'unigo': ['data/*']}

install_requires = \
['Cython>=0.29.32,<0.30.0',
 'Flask>=2.0.2,<3.0.0',
 'Owlready2>=0.38,<0.39',
 'docopt>=0.6.2,<0.7.0',
 'line-profiler>=3.5.1,<4.0.0',
 'marshmallow>=3.14.1,<4.0.0',
 'notebook>=6.4.12,<7.0.0',
 'pydantic>=1.10.1,<2.0.0',
 'pyproteinsext>=3.0.3,<4.0.0',
 'requests>=2.27.1,<3.0.0',
 'requires>=0.10.2,<0.11.0',
 'scipy>=1.8.0,<2.0.0',
 'wheel>=0.37.1,<0.38.0']

setup_kwargs = {
    'name': 'unigo',
    'version': '2.0.5',
    'description': '',
    'long_description': None,
    'author': 'glaunay',
    'author_email': 'pitooon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
