# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glotter']

package_data = \
{'': ['*']}

install_requires = \
['docker>=6.0.1,<7.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'pytest-xdist>=3.2.0,<4.0.0',
 'pytest>=7.2.1,<8.0.0',
 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['glotter = glotter.__main__:main']}

setup_kwargs = {
    'name': 'glotter2',
    'version': '0.4.1',
    'description': 'An execution library for scripts written in any language. This is a fork of https://github.com/auroq/glotter',
    'long_description': "# Glotter2\n\n[![Makefile CI](https://github.com/rzuckerm/glotter2/actions/workflows/makefile.yml/badge.svg)](https://github.com/rzuckerm/glotter2/actions/workflows/makefile.yml)\n[![Coverage](https://rzuckerm.github.io/glotter2/badge.svg)](https://rzuckerm.github.io/glotter2)\n[![PyPI version](https://img.shields.io/pypi/v/glotter2)](https://pypi.org/project/glotter2)\n[![Python versions](https://img.shields.io/pypi/pyversions/glotter2)](https://pypi.org/project/glotter2)\n[![Python wheel](https://img.shields.io/pypi/wheel/glotter2)](https://pypi.org/project/glotter2)\n\nThis is a fork of the original [Glotter](https://github.com/auroq/glotter) repository, which\nappears to be unmaintained.\n\nGlotter2 is an execution library for collections of single file scripts. It uses Docker to be able to build, run, and optionally test scripts in any language without having to install a local sdk or development environment.\n\n## Contributing\n\nIf you'd like to contribute to Glotter2, read our [contributing guidelines](./CONTRIBUTING.md).\n\n## Changelog\n\n### Glotter2 releases\n\n* 0.4.1:\n  * Bump version since wrong version pushed to pypi\n* 0.4.0:\n  * Change test ID from `<filename>` to `<language>/<filename>`\n  * Speed up test collection by about 1 min and total test time by about\n    5 min in [sample-programs][sample-programs] by caching list of sources\n  * Modify `download`, `run`, and `test` commands so that `-p`, `-l`, and\n    `-s` are no longer mutually exclusive\n  * Add `--parallel` to `download` command to parallelize image downloads\n  * Add `--parallel` to `test` command to parallelize tests\n* 0.3.0:\n  * Fix crash when running tests for [sample-programs][sample-programs]\n    with glotter 0.2.x\n  * Upgrade dependencies to latest version:\n    * `docker >=6.0.1, <7`\n    * `Jinja >=3.1.2, <4`\n    * `pytest >=7.2.1, <8`\n    * `PyYAML >=6.0, <7`\n  * Upgrade python to 3.8 or above\n\n### Original Glotter releases\n\n* 0.2.x: Add reporting verb to output discovered sources as a table in stdout or to a csv\n* 0.1.x: Initial release of working code.\n\n[sample-programs]: https://github.com/TheRenegadeCoder/sample-programs\n",
    'author': 'auroq',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rzuckerm/glotter2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
