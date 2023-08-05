# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_argparse_builder']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.5,<2.0.0']

setup_kwargs = {
    'name': 'pydantic-argparse-builder',
    'version': '0.1.1',
    'description': 'Build ArgumentParser from pydantic model.',
    'long_description': '# pydantic-argparse-builder\n\nBuild ArgumentParser from pydantic model.\n\n## What\'s difference with other projects.\n\nThis project focuses on creating an argument parser from the pydantic model.\nYou can easily add a sub parser.\n\n## Example 1\n\n```python\nfrom argparse import ArgumentParser\nfrom pydantic import BaseModel, Field\nfrom pydantic_argparse_builder import build_parser\n\nclass Config(BaseModel):\n    string: str = Field(description="string parameter")\n    integer: int = Field(description="integer parameter")\n\nparser = ArgumentParser()\nbuild_parser(parser)\nparser.print_help()\n```\n\n```\nusage: basic.py [-h] --string STRING --integer INTEGER\n\noptional arguments:\n  -h, --help            show this help message and exit\n\nConfig:\n  --string STRING, -s STRING\n                        a required string\n  --integer INTEGER, -i INTEGER\n                        a required integer\n```\n\n## Example 2\n\n```python\nfrom argparse import ArgumentParser\nfrom pydantic import BaseModel, Field\nfrom pydantic_argparse_builder import build_parser\n\nclass SubConfigA(BaseModel):\n    string: str = Field(description="string parameter")\n    integer: int = Field(description="integer parameter")\n\nclass SubConfigB(BaseModel):\n    double: float = Field(description="a required string")\n    integer: int = Field(0, description="a required integer")\n\n\nparser = ArgumentParser()\nsubparsers = parser.add_subparsers()\nbuild_parser(subparsers.add_parser("alpha"), SubConfigA)\nbuild_parser(subparsers.add_parser("beta"), SubConfigB)\nparser.print_help()\n```\n\n```\nusage: sub_parser.py [-h] {alpha,beta} ...\n\npositional arguments:\n  {alpha,beta}\n\noptional arguments:\n  -h, --help    show this help message and exit\n```\n',
    'author': 'elda27',
    'author_email': 'kaz.birdstick@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
