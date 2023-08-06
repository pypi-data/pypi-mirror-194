# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mightstone',
 'mightstone.ass',
 'mightstone.ass.compressor',
 'mightstone.ass.compressor.codecs',
 'mightstone.assets',
 'mightstone.cli',
 'mightstone.rule',
 'mightstone.services',
 'mightstone.services.cardconjurer',
 'mightstone.services.edhrec',
 'mightstone.services.mtgjson',
 'mightstone.services.scryfall']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0',
 'aiosqlite>=0.18.0,<0.19.0',
 'aiostream>=0.4.5,<0.5.0',
 'appdirs>=1.4.4,<2.0.0',
 'asyncstdlib>=3.10.5,<4.0.0',
 'beanie>=1.17.0,<2.0.0',
 'cairosvg>=2.6.0,<3.0.0',
 'click>=8.0.1,<9.0.0',
 'dependency-injector>=4.41.0,<5.0.0',
 'httpx-cache>=0.7.0,<0.8.0',
 'httpx>=0.23.3,<0.24.0',
 'ijson>=3.2.0.post0,<4.0.0',
 'logging>=0.4.9.6,<0.5.0.0',
 'nest-asyncio>=1.5.6,<2.0.0',
 'ordered-set>=4.1.0,<5.0.0',
 'pillow>=9.4.0,<10.0.0',
 'pytest>=7.2.1,<8.0.0',
 'python-slugify>=8.0.0,<9.0.0',
 'requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['mightstone = mightstone.cli:cli']}

setup_kwargs = {
    'name': 'mightstone',
    'version': '0.4.0',
    'description': 'A library manage all things Magic The Gathering related in python',
    'long_description': '# mightstone\n\n\n[![PyPi](https://img.shields.io/pypi/v/mightstone.svg)](https://pypi.python.org/pypi/mightstone)\n[![Documentation](https://readthedocs.org/projects/mightstone/badge/?version=latest)](https://mightstone.readthedocs.io/en/latest/?badge=latest)\n[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/7037/badge)](https://bestpractices.coreinfrastructure.org/projects/7037)\n\nA library manage all things Magic The Gathering related in python\n\n\n## Developing\n\nRun `make` for help\n\n    make install             # Run `poetry install`\n    make showdeps            # run poetry to show deps\n    make lint                # Runs bandit and black in check mode\n    make format              # Formats you code with Black\n    make test                # run pytest with coverage\n    make build               # run `poetry build` to build source distribution and wheel\n    make pyinstaller         # Create a binary executable using pyinstaller\n\n\n## System dependencies\n\nMightstone use [Ijson](https://github.com/ICRAR/ijson) that relies on [YAJL](https://lloyd.github.io/yajl/). IJson will\nuse its python backend on the run if YAJL is not installed, but you cold benefit from installing YAJL locally.\n\n\n',
    'author': 'Guillaume Boddaert',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/guibod/mightstone',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
