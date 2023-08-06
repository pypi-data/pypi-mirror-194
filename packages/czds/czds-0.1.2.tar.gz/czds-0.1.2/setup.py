# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['czds', 'czds.utils']

package_data = \
{'': ['*'], 'czds': ['data/*']}

install_requires = \
['attrs>=22.2.0,<23.0.0',
 'click>=8.0.1',
 'fire>=0.5.0,<0.6.0',
 'prompt-toolkit>=3.0.36,<4.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'rich>=13.3.1,<14.0.0']

entry_points = \
{'console_scripts': ['czds = czds.__main__:main']}

setup_kwargs = {
    'name': 'czds',
    'version': '0.1.2',
    'description': 'CZDS',
    'long_description': "# CZDS\n\n[![PyPI](https://img.shields.io/pypi/v/czds.svg)][pypi status]\n[![Status](https://img.shields.io/pypi/status/czds.svg)][pypi status]\n[![Python Version](https://img.shields.io/pypi/pyversions/czds)][pypi status]\n[![License](https://img.shields.io/pypi/l/czds)][license]\n\n[![Read the documentation at https://czds.readthedocs.io/](https://img.shields.io/readthedocs/czds/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Code Quality & Tests](https://github.com/MSAdministrator/czds/actions/workflows/tests.yml/badge.svg)](https://github.com/MSAdministrator/czds/actions/workflows/tests.yml)\n\n[![Codecov](https://codecov.io/gh/MSAdministrator/czds/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi status]: https://pypi.org/project/czds/\n[read the docs]: https://czds.readthedocs.io/\n[tests]: https://github.com/MSAdministrator/czds/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/MSAdministrator/czds\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## What is CZDS?\n\nEach Top Level Domain (TLD) is maintained by a registry operator, who also manages a publicly available list of Second Level Domains (SLDs) and the details needed to resolve those domain names to Internet Protocol (IP) addresses.\n\nThe registry operator’s zone data contains the mapping of domain names, associated name server names, and IP addresses for those name servers. These details are updated by the registry operator for its respective TLDs whenever information changes or a domain name is added or removed.\n\nEach registry operator keeps its zone data in a text file called the Zone File which is updated once every 24 hours.\n\n## Features\n\n- Retrieve Centralized Zone Transfer Files from root DNS servers hosted by ICAAN and other agencies\n- Download one or all of the zone files and return data in multiple formats; text, json or a file (default)\n- You can now retrieve zone files using multi-threading\n\n## Roadmap\n\nThe following are some of the features I am planning on adding but would love to hear everyones thoughts as well.\n\n- Add ability to search based on domain and/or TLD\n  - This may include using algorithms like Levenshtein distance, confusables/idna characters, etc.\n- Add ability to derive differences between zone files over time\n- Add ability to retrieve other contextual external information like WHOIS\n- Add ability to save/store data into a database\n\n## Requirements\n\n- You need a CZDS account with ICAAN. You can sign-up [here](https://czds.icann.org)\n- Internet access\n\n## Installation\n\nYou can install _CZDS_ via [pip] from [PyPI]:\n\n```console\n$ pip install czds\n```\n\nIf you are using `poetry` (recommended) you can add it to your package using\n\n```console\npoetry add czds\n```\n\n\n## Usage\n\nBelow is the command line reference but you can also use the current version of czds to retrieve the help by typing ```czds --help```.\n\n```console\nNAME\n    czds - Main class for ICAAN CZDS.\n\nSYNOPSIS\n    czds GROUP | VALUE | --username=USERNAME --password=PASSWORD --save_directory=SAVE_DIRECTORY\n\nDESCRIPTION\n    Main class for ICAAN CZDS.\n\nARGUMENTS\n    USERNAME\n        Type: ~AnyStr\n    PASSWORD\n        Type: ~AnyStr\n    SAVE_DIRECTORY\n        Type: ~AnyStr\n\nGROUPS\n    GROUP is one of the following:\n\n     BASE_HEADERS\n\n     links\n\nVALUES\n    VALUE is one of the following:\n\n     AUTH_URL\n\n     BASE_URL\n\n     OUTPUT_FORMAT\n\n     PASSWORD\n\n     SAVE_PATH\n\n     THREAD_COUNT\n\n     USERNAME\n\n     connection\n```\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide](CONTRIBUTING.md).\n\n## Developmemt\n\nYou can clone the repositry and begin development using\n\n```bash\ngit clone https://github.com/MSAdministrator/czds.git\ncd czds\npoetry install\n```\n\nIf you are using `pyenv` to manage your enviroments you can set a config option in poetry to use the set pyenv version of python by running this:\n\n```bash\npoetry config virtualenvs.prefer-active-python true\npoetry install\n```\n## License\n\nDistributed under the terms of the [MIT license][LICENSE.md],\n_CZDS_ is free and open source software.\n\n## Security\n\nSecurity concerns are a top priority for us, please review our [Security Policy](SECURITY.md).\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue](https://github.com/MSAdministrator/czds/issues/new) along with a detailed description.\n\n## Credits\n\nThis project was generated from [@MSAdministrator]'s [Hypermodern Python Cookiecutter] template.\n\n[@MSAdministrator]: https://github.com/MSAdministrator\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/MSAdministrator/czds/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/MSAdministrator/czds/blob/main/LICENSE\n[contributor guide]: https://github.com/MSAdministrator/czds/blob/main/CONTRIBUTING.md\n[command-line reference]: https://czds.readthedocs.io/en/latest/usage.html\n",
    'author': 'Josh Rickard',
    'author_email': 'rickardja@live.com',
    'maintainer': 'Josh Rickard',
    'maintainer_email': 'rickardja@live.com',
    'url': 'https://github.com/MSAdministrator/czds',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
