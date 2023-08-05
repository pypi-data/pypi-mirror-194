# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ss13_tools',
 'ss13_tools.auth',
 'ss13_tools.byond',
 'ss13_tools.centcom',
 'ss13_tools.log_downloader',
 'ss13_tools.scrubby',
 'ss13_tools.slur_detector']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'colorama>=0.4.6,<0.5.0',
 'pycryptodome>=3.17,<4.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'ss13-tools',
    'version': '2.1.0',
    'description': 'Python toolchain for SS13',
    'long_description': "# SS13 tools\n\n[![PyLint](https://github.com/RigglePrime/SS13-tools/actions/workflows/pylint.yml/badge.svg)](https://github.com/RigglePrime/SS13-tools/actions/workflows/pylint.yml)\n[![Flake8](https://github.com/RigglePrime/SS13-tools/actions/workflows/flake8-lint.yml/badge.svg)](https://github.com/RigglePrime/SS13-tools/actions/workflows/flake8-lint.yml)\n[![Build](https://github.com/RigglePrime/SS13-tools/actions/workflows/publish.yml/badge.svg)](https://github.com/RigglePrime/SS13-tools/actions/workflows/publish.yml)\n\nA set of tools to help with automating tasks for the /tg/ branch of SS13.\n\nMade for Python 3.9+\n\n## How to run\n\n`pip install ss13-tools; python -m ss13_tools` (pip3 on Linux) or dowload the executable [here](https://github.com/RigglePrime/SS13-tools/releases/latest)\n\n## Contents\n\n- auth (TODO)\n- byond: tools for working with BYOND, such as checking if a ckey exists\n- [centcom](https://centcom.melonmesa.com/)\n- log_downloader: downloads logs from tg's [parsed logs](https://tgstation13.org/parsed-logs)\n- scrubby: scrubby tools\n- slur_detector: what it says on the tin\n\n## Downloading\n\nFor compiled versions, see [this](https://github.com/RigglePrime/admin-tools/releases) link\n\nNow also available on [PyPi](https://pypi.org/project/ss13-tools/)!\n",
    'author': 'RigglePrime',
    'author_email': '27156122+RigglePrime@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/RigglePrime/SS13-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.1,<3.12',
}


setup(**setup_kwargs)
