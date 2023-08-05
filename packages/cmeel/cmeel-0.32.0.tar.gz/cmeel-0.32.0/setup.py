# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmeel']

package_data = \
{'': ['*']}

install_requires = \
['tomli>=2.0.1,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=4.12.0,<5.0.0'],
 'build': ['cmake>=3.22.3,<4.0.0',
           'packaging>=21.3,<22.0',
           'wheel>=0.37.1,<0.38.0']}

setup_kwargs = {
    'name': 'cmeel',
    'version': '0.32.0',
    'description': 'Create Wheel from CMake projects',
    'long_description': '# CMake Wheel\n\n[![PyPI version](https://badge.fury.io/py/cmeel.svg)](https://pypi.org/project/cmeel)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/cmake-wheel/cmeel/main.svg)](https://results.pre-commit.ci/latest/github/cmake-wheel/cmeel/main)\n[![Documentation Status](https://readthedocs.org/projects/cmeel/badge/?version=latest)](https://cmeel.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nWheel build backend using CMake, to package anything with pip and distribute on PyPI.\n\nFollowing those relevant PEPs:\n- [PEP 427](https://peps.python.org/pep-0427/), The Wheel Binary Package Format 1.0\n- [PEP 517](https://peps.python.org/pep-0517/), A build-system independent format for source trees\n- [PEP 518](https://peps.python.org/pep-0518/), Specifying Minimum Build System Requirements for Python Projects\n- [PEP 600](https://peps.python.org/pep-0600/), Future ‘manylinux’ Platform Tags for Portable Linux Built Distributions\n- [PEP 621](https://peps.python.org/pep-0621/), Storing project metadata in pyproject.toml\n- [PEP 639](https://peps.python.org/pep-0639/), Improving License Clarity with Better Package Metadata, **DRAFT**\n\n## Chat\n\nhttps://matrix.to/#/#cmake-wheel:matrix.org\n\n## Basic idea\n\nGlue between PEP 517 `build_wheel` function and modern CMake standard project configuration / build / test / install\n\nThis Install in `${PYTHON_SITELIB}/cmeel.prefix/`:\n- As there is a dot, it is not a valid python module name, so no risk of importing anything there by mistake\n- Play well with others, as everything is confined to `${PYTHON_SITELIB}/cmeel.prefix`\n- `${PYTHON_SITELIB}/cmeel.pth` automatically load `${PYTHON_SITELIB}/cmeel.prefix/${PYTHON_SITELIB}`, so python\n  packages work out of the box\n- Existing `${PYTHON_SITELIB}/cmeel.prefix` are automatically added to `$CMAKE_PREFIX_PATH`, so we can build CMake\n  packages whose dependencies are provided by other CMake packages installed with cmeel\n- Stuff in `${PYTHON_SITELIB}/cmeel.prefix/bin` is exposed via `cmeel.run:cmeel_run`\n',
    'author': 'Guilhem Saurel',
    'author_email': 'guilhem.saurel@laas.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cmake-wheel/cmeel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
