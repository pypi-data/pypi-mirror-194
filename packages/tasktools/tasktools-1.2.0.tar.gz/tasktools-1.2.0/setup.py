# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tasktools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tasktools',
    'version': '1.2.0',
    'description': 'This module allows you to work with asyncio coroutines and schedule some tasks.',
    'long_description': "Asyncio Tasks Tools\n======================\n\nThe [asyncio](https://docs.python.org/3/library/asyncio.html) module,\nfrom standar library since 3.4, is basic for the coroutines and\ntasks. You need to study first this module because it's not really easy.\n\nThis module allows you to work with asyncio coroutines and schedule some\ntasks.\n\nThese tasks can be build in a really generic way, like an independet loop.\n\nThe tools in this module can help you to manage your coroutines and succeed.\n\nThe 'how to use' on [documentation](../doc/tasktools.pdf) file.\n\n\nHow to install\n-----------------\n\nTo install, in your virtualenvironment, execute pip:\n\n```\npip install git+[url]\n```\n\nOr, using setup:\n\n```\npython setup.py tasktools\n```\n",
    'author': 'David Pineda',
    'author_email': 'dahalpi@gmail.com',
    'maintainer': 'David Pineda',
    'maintainer_email': 'dahalpi@gmail.com',
    'url': 'https://tasktools.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
