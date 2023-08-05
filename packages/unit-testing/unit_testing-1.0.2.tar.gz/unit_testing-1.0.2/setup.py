# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unit_testing']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'unit-testing',
    'version': '1.0.2',
    'description': 'An example project for showcasing unit testing.',
    'long_description': "# 5G00EV17-3001 Unit testing\n\nAn example project for showcasing unit testing.\n\n|   Category   |  Badges  |\n|:------------:|---|\n| **PyPI**     | ![Python versions](https://img.shields.io/pypi/pyversions/iplib3?logo=python) ![PyPI - Implementation](https://img.shields.io/pypi/implementation/iplib3) |\n| **Tests**    | [![codecov](https://codecov.io/gh/Diapolo10/5G00EV17-3001_unit-testing/branch/main/graph/badge.svg?token=FpaCuVjOAB)](https://codecov.io/gh/Diapolo10/5G00EV17-3001_unit-testing) ![Unit tests](https://github.com/diapolo10/5G00EV17-3001_unit-testing/workflows/Unit%20tests/badge.svg) ![Unit tests](https://github.com/diapolo10/5G00EV17-3001_unit-testing/workflows/Pylint/badge.svg) ![Unit tests](https://github.com/diapolo10/5G00EV17-3001_unit-testing/workflows/Flake8/badge.svg) |\n| **Activity** | ![GitHub contributors](https://img.shields.io/github/contributors/diapolo10/5G00EV17-3001_unit-testing) ![Last commit](https://img.shields.io/github/last-commit/diapolo10/5G00EV17-3001_unit-testing?logo=github)\n| **QA**       | [![CodeFactor](https://www.codefactor.io/repository/github/diapolo10/5G00EV17-3001_unit-testing/badge?logo=codefactor)](https://www.codefactor.io/repository/github/diapolo10/5G00EV17-3001_unit-testing) [![Rating](https://img.shields.io/librariesio/sourcerank/pypi/iplib3)](https://libraries.io/github/Diapolo10/iplib3/sourcerank) |\n| **Other**    | [![License](https://img.shields.io/github/license/diapolo10/5G00EV17-3001_unit-testing)](https://opensource.org/licenses/MIT) ![Repository size](https://img.shields.io/github/repo-size/diapolo10/5G00EV17-3001_unit-testing?logo=github) ![Code size](https://img.shields.io/github/languages/code-size/diapolo10/5G00EV17-3001_unit-testing?logo=github) ![Lines of code](https://img.shields.io/tokei/lines/github/diapolo10/5G00EV17-3001_unit-testing?logo=github) |\n\n-------------------------------------------------------------------------------\n\n## Description\n\nThis project showcases how unit testing works by implementing a very simple\nPython library, and adding unit tests to it. The project uses Pytest.\n\n## Getting Started\n\n### Dependencies\n\nThe main project has no library dependencies, but the actual unit testing\npart relies on several packages listed in\n[`pyproject.toml`][pyproject.toml]. But in general, you'll need:\n\n- Python 3.7 or newer\n- Poetry\n\nThe project is automatically tested on the latest versions of Windows,\nMac OS, and Ubuntu, and it has also been tested on both CPython\nand PyPy. Using other implementations or operating systems\nmay work, but is not guaranteed.\n\n### Installation\n\nPlease see the documentation [here][installation].\n\n### Running unit tests\n\nPlease see the documentation [here][running unit tests].\n\n## Version history\n\nThe project's changelog can be found [here][changelog].\n\n## License\n\nThis project is licensed under the MIT license - see the [`LICENSE`][license]-file for details.\n\n## Acknowledgements\n\nInspiration, code snippets, debugging help, etc.\n\n- My fellow team members\n\n[pyproject.toml]: ./pyproject.toml\n[installation]: ./docs/installation.md\n[running unit tests]: ./docs/running_unit_tests.md\n[changelog]: ./CHANGELOG.md\n[license]: ./LICENSE\n",
    'author': 'Lari Liuhamo',
    'author_email': 'lari.liuhamo+pypi@gmail.com',
    'maintainer': 'Lari Liuhamo',
    'maintainer_email': 'lari.liuhamo+pypi@gmail.com',
    'url': 'https://pypi.org/project/5G00EV17-3001_unit-testing/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
