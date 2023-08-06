# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drivy_tools', 'drivy_tools.src', 'drivy_tools.src.utils']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19.0,<0.20.0',
 'pydantic>=1.8.2,<2.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'typer>=0.4.0,<0.5.0',
 'user_agent>=0.1.9,<0.2.0']

entry_points = \
{'console_scripts': ['drivy = drivy_tools.main:app']}

setup_kwargs = {
    'name': 'drivy-tools',
    'version': '0.3.2',
    'description': 'Tool to make use of Drivy',
    'long_description': '# Drivy Tools\n\n[![CI](https://github.com/zekiblue/drivy_tools/actions/workflows/build_publish.yml/badge.svg)](https://github.com/zekiblue/drivy_tools/actions/workflows/build_publish.yml)\n\nThis is the tools for getaround.com. Tools have the fetching, analyzing and prediction ability\n',
    'author': 'zekiblue',
    'author_email': 'zekiberkulu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zekiblue/drivy_tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
