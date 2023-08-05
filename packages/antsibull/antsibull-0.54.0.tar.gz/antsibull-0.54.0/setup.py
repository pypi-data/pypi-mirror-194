# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['antsibull', 'antsibull.cli', 'antsibull.data', 'antsibull.utils', 'tests']

package_data = \
{'': ['*'], 'antsibull.data': ['debian/*']}

install_requires = \
['aiofiles',
 'aiohttp>=3.0.0',
 'antsibull-changelog>=0.14.0',
 'antsibull-core>=1.5.0,<3.0.0',
 'asyncio-pool',
 'jinja2',
 'packaging>=20.0',
 'semantic_version',
 'sh>=1.0.0,<2.0.0',
 'twiggy']

entry_points = \
{'console_scripts': ['antsibull-build = antsibull.cli.antsibull_build:main']}

setup_kwargs = {
    'name': 'antsibull',
    'version': '0.54.0',
    'description': 'Tools for building the Ansible Distribution',
    'long_description': '<!--\nCopyright (c) Ansible Project\nGNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)\nSPDX-License-Identifier: GPL-3.0-or-later\n-->\n\n# antsibull -- Ansible Build Scripts\n[![Discuss on Matrix at #community:ansible.com](https://img.shields.io/matrix/community:ansible.com.svg?server_fqdn=ansible-accounts.ems.host&label=Discuss%20on%20Matrix%20at%20%23community:ansible.com&logo=matrix)](https://matrix.to/#/#community:ansible.com)\n[![Python linting badge](https://github.com/ansible-community/antsibull/workflows/Python%20linting/badge.svg?event=push&branch=main)](https://github.com/ansible-community/antsibull/actions?query=workflow%3A%22Python+linting%22+branch%3Amain)\n[![Python testing badge](https://github.com/ansible-community/antsibull/workflows/Python%20testing/badge.svg?event=push&branch=main)](https://github.com/ansible-community/antsibull/actions?query=workflow%3A%22Python+testing%22+branch%3Amain)\n[![dumb PyPI on GH pages badge](https://github.com/ansible-community/antsibull/workflows/👷%20dumb%20PyPI%20on%20GH%20pages/badge.svg?event=push&branch=main)](https://github.com/ansible-community/antsibull/actions?query=workflow%3A%22👷+dumb+PyPI+on+GH+pages%22+branch%3Amain)\n[![Codecov badge](https://img.shields.io/codecov/c/github/ansible-community/antsibull)](https://codecov.io/gh/ansible-community/antsibull)\n\nTooling for building various things related to Ansible\n\nScripts that are here:\n\n* antsibull-build - Builds Ansible-2.10+ from component collections ([docs](docs/build-ansible.rst))\n\nRelated projects are [antsibull-changelog](https://pypi.org/project/antsibull-changelog/) and [antsibull-docs](https://pypi.org/project/antsibull-docs/), which are in their own repositories ([antsibull-changelog repository](https://github.com/ansible-community/antsibull-changelog/), [antsibull-docs repository](https://github.com/ansible-community/antsibull-docs/)). Currently antsibull-changelog is a dependency of antsibull. Therefore, the scripts contained in it will be available as well when installing antsibull.\n\nYou can find a list of changes in [the Antsibull changelog](./CHANGELOG.rst).\n\nUnless otherwise noted in the code, it is licensed under the terms of the GNU\nGeneral Public License v3 or, at your option, later.\n\nantsibull is covered by the [Ansible Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html).\n\n## Versioning and compatibility\n\nFrom version 0.1.0 on, antsibull sticks to semantic versioning and aims at providing no backwards compatibility breaking changes **to the command line API (antsibull)** during a major release cycle. We might make exceptions from this in case of security fixes for vulnerabilities that are severe enough.\n\nWe explicitly exclude code compatibility. **antsibull is not supposed to be used as a library.** The only exception are potential dependencies with other antsibull projects (currently, none). If you want to use a certain part of antsibull as a library, please create an issue so we can discuss whether we add a stable interface for **parts** of the Python code. We do not promise that this will actually happen though.\n\n## Running from source\n\nPlease note that to run antsibull from source, you need to install some related projects adjacent to the antsibull checkout.  More precisely, assuming you checked out the antsibull repository in a directory `./antsibull/`, you need to check out the following projects in the following locations:\n\n- [antsibull-changelog](https://github.com/ansible-community/antsibull-changelog/) needs to be checked out in `./antsibull-changelog/`.\n- [antsibull-core](https://github.com/ansible-community/antsibull-core/) needs to be checked out in `./antsibull-core/`.\n\nThis can be done as follows:\n\n    git clone https://github.com/ansible-community/antsibull-changelog.git\n    git clone https://github.com/ansible-community/antsibull-core.git\n    git clone https://github.com/ansible-community/antsibull.git\n    cd antsibull\n\nScripts are created by poetry at build time.  So if you want to run from a checkout, you\'ll have to run them under poetry::\n\n    python3 -m pip install poetry\n    poetry install  # Installs dependencies into a virtualenv\n    poetry run antsibull-build --help\n\nNote: When installing a package published by poetry, it is best to use pip >= 19.0.  Installing with pip-18.1 and below could create scripts which use pkg_resources which can slow down startup time (in some environments by quite a large amount).\n\n## Creating a new release:\n\nIf you want to create a new release::\n\n    vim pyproject.toml  # Make sure the correct version number is used\n    vim changelogs/fragment/$VERSION_NUMBER.yml  # create \'release_summary:\' fragment\n    antsibull-changelog release --version $VERSION_NUMBER\n    git add CHANGELOG.rst changelogs\n    git commit -m "Release $VERSION_NUMBER."\n    poetry build\n    poetry publish  # Uploads to pypi.  Be sure you really want to do this\n\n    git tag $VERSION_NUMBER\n    git push --tags\n    vim pyproject.toml  # Bump the version number to X.Y.Z.post0\n    git commit -m \'Update the version number for the next release\' pyproject.toml\n    git push\n',
    'author': 'Toshio Kuratomi',
    'author_email': 'a.badger@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ansible-community/antsibull',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
