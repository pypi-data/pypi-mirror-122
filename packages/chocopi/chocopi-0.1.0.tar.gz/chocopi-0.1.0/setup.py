# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['chocopi']
setup_kwargs = {
    'name': 'chocopi',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Antariksh Verma',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
