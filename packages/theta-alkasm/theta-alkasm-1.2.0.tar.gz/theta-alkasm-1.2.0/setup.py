# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['theta']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'theta-alkasm',
    'version': '1.2.0',
    'description': 'Extensions for multithreaded Python applications.',
    'long_description': '# theta\n\nExtensions for multithreaded Python applications.\n\n## Install\n\n```sh\npip install theta-alkasm\n```\n\n## Development\n\nIn a virtual environment:\n\n```\n$ poetry install\n$ poetry check\n$ poetry run pytest\n$ poetry run black theta\n$ poetry run mypy theta\n```\n',
    'author': 'Alexander Reynolds',
    'author_email': 'alex@theory.shop',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alkasm/theta',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
