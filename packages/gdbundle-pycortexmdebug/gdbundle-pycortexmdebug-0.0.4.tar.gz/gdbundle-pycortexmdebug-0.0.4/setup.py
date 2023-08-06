# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdbundle_pycortexmdebug',
 'gdbundle_pycortexmdebug.cmdebug',
 'gdbundle_pycortexmdebug.cmdebug.cmdebug',
 'gdbundle_pycortexmdebug.cmdebug.scripts']

package_data = \
{'': ['*']}

install_requires = \
['gdbundle>=0.0.3,<0.1.0']

setup_kwargs = {
    'name': 'gdbundle-pycortexmdebug',
    'version': '0.0.4',
    'description': 'gdbundle wrapper for PyCortexMDebug',
    'long_description': None,
    'author': 'Tyler Hoffman',
    'author_email': 'tyler@memfault.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
