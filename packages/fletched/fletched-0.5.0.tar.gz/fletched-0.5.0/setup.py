# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fletched', 'fletched.controls', 'fletched.mvp', 'fletched.routed_app']

package_data = \
{'': ['*']}

install_requires = \
['abstractcp>=0.9.9,<0.10.0',
 'flet>=0.4.0,<0.5.0',
 'polars>=0.16.8,<0.17.0',
 'pydantic>=1.10.5,<2.0.0',
 'repath>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'fletched',
    'version': '0.5.0',
    'description': 'Tools to build flet apps with multiple views/routes',
    'long_description': '# Getting started\n\n![logo](assets/logo.png)\n\n## Introduction\n\nWelcome to fletched!\n\nAn opinionated framework on top of flet,\ndesigned to significantly reduce boilerplate code\nand aid in structuring a non-trivial project.\n\nIf flet were an arrow,\nfletched would give it feathers,\nenabling you to aim and hit way further.\n\nFor now, it offers two libraries/submodules:\n`mvp` and `routed_app`,\nwhich were originally separate projects.\nThey are designed to work well in conjunction,\nbut should you only want to use one of them,\nthat will work as well.\n\n## Installation\n\nYou can install fletched by executing\n\n```bash\npoetry add fletched\n```\n\nor\n\n```bash\npip install fletched\n```\n\ndepending on how you prefer to manage your dependencies.\n',
    'author': 'iron3oxide',
    'author_email': 'jason.hottelet@tuta.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://iron3oxide.github.io/fletched/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
