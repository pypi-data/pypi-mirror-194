# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fulmo_cookiecutter_poetry']

package_data = \
{'': ['*']}

install_requires = \
['cookiecutter>=2.1.1,<3.0.0']

entry_points = \
{'console_scripts': ['fcp = fulmo_cookiecutter_poetry.cli:main']}

setup_kwargs = {
    'name': 'fulmo-cookiecutter-poetry',
    'version': '0.4.2',
    'description': 'A python cookiecutter application to create a new python project that uses poetry to manage its dependencies.',
    'long_description': '<p align="center">\n  <img width="100" src="https://raw.githubusercontent.com/jexio/fulmo-cookiecutter-poetry/main/docs/static/cookiecutter.svg">\n</p style = "margin-bottom: 2rem;">\n\n---\n\n[![Release](https://img.shields.io/github/v/release/jexio/fulmo-cookiecutter-poetry)](https://pypi.org/project/fulmo-cookiecutter-poetry/)\n[![Build status](https://img.shields.io/github/actions/workflow/status/jexio/fulmo-cookiecutter-poetry/main.yml?branch=main)](https://github.com/jexio/fulmo-cookiecutter-poetry/actions/workflows/main.yml?query=branch%3Amain)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/fulmo-cookiecutter-poetry)](https://pypi.org/project/fulmo-cookiecutter-poetry/)\n[![Documentation Coverage](https://raw.githubusercontent.com/jexio/fulmo-cookiecutter-poetry/main/docs/static/interrogate_badge.svg)](https://interrogate.readthedocs.io/)\n[![Maintainability Index](https://raw.githubusercontent.com/jexio/fulmo-cookiecutter-poetry/main/docs/static/wily_badge.svg)](https://wily.readthedocs.io/en/latest/)\n[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://jexio.github.io/fulmo-cookiecutter-poetry/)\n[![License](https://img.shields.io/github/license/jexio/fulmo-cookiecutter-poetry)](https://img.shields.io/github/license/jexio/fulmo-cookiecutter-poetry)\n\n**Contents**\n- [Features](#features)\n- [Quick start](#quickstart)\n- [Credits](#credits)\n<br>\n\n## Features\n\nThis is a modern Cookiecutter template that can be used to initiate a Python project with all the necessary tools for development, testing, and deployment. It supports the following features:\n\n- [Poetry](https://python-poetry.org/) for dependency management\n- CI/CD with [GitHub Actions](https://github.com/features/actions/)\n- Pre-commit hooks with [pre-commit](https://pre-commit.com/)\n- Code quality with:\n  - [black](https://pypi.org/project/black/)\n  - [isort](https://github.com/timothycrosley/isort/)\n  - [ruff](https://github.com/charliermarsh/ruff/)\n  - [mypy](https://mypy.readthedocs.io/en/stable/)\n  - [interrogate](https://interrogate.readthedocs.io/en/latest/)\n- Checks dependencies for known security vulnerabilities with [Safety](https://github.com/pyupio/safety/)\n- All development tasks (lint, format, test, etc) wrapped up in a python CLI by [duty](https://pawamoy.github.io/duty/)\n- Publishing to [Pypi](https://pypi.org) by creating a new release on GitHub\n- Testing and coverage with [pytest](https://docs.pytest.org/en/7.1.x/) and [codecov](https://about.codecov.io/)\n- Documentation with [MkDocs](https://www.mkdocs.org/)\n- Compatibility testing for multiple versions of Python with [Tox](https://tox.wiki/en/latest/)\n- Auto-generated `CHANGELOG.md` from git commits (using Angular message style) [commitizen](https://commitizen-tools.github.io/commitizen/)\n- Makefile for convenience\n\n---\n<p align="center">\n  <a href="https://jexio.github.io/fulmo-cookiecutter-poetry/">Documentation</a> - <a href="https://github.com/jexio/fulmo-cookiecutter-poetry-example">Example</a> -\n  <a href="https://pypi.org/project/fulmo-cookiecutter-poetry/">PyPi</a>\n</p>\n\n---\n\n\n## Quickstart\n\n<details>\n<summary><b>Install cookiecutter</b></summary>\nOn your local machine, navigate to the directory in which you want to\ncreate a project directory, and run the following commands:\n\n``` bash\npip install cookiecutter\ncookiecutter https://github.com/jexio/fulmo-cookiecutter-poetry.git\n```\n</details>\n\n<details>\n<summary><b>Github repository</b></summary>\nCreate a repository on GitHub, and then run the following commands, replacing `{project-name}`, with the name that you gave the Github repository and\n`{github_username}` with your Github username.\n\n``` bash\ncd <project_name>\ngit init -b main\ngit add .\ngit commit -m "Init commit"\ngit remote add origin git@github.com:<github_username>/<project_name>.git\ngit push -u origin main\n```\n</details>\n\n<details>\n<summary><b>Creating an environment</b></summary>\nFinally, install the environment and the pre-commit hooks with\n\n ```bash\n make install\n ```\n</details>\n\n\n<details>\n<summary><b>CI/CD and Docs</b></summary>\n\nYou are now ready to start development on your project! The CI/CD\npipeline will be triggered when you open a pull request, merge to main,\nor when you create a new release.\n<br>\nTo finalize the set-up for publishing to PyPi, see [here](https://jexio.github.io/fulmo-cookiecutter-poetry/features/publishing/#set-up-for-pypi/)\n<br>\nFor activating the automatic documentation with MkDocs, see [here](https://jexio.github.io/fulmo-cookiecutter-poetry/features/mkdocs/#enabling-the-documentation-on-github/)\n<br>\nTo enable the code coverage reports, see [here](https://jexio.github.io/fulmo-cookiecutter-poetry/features/codecov/)\n</details>\n\n## Credits\n\nThis cookiecutter was built for learning purpose and inspired by:\n\n* [fedejaure/cookiecutter-modern-pypackage][fedejaure/cookiecutter-modern-pypackage]: Cookiecutter template for a modern Python package.\n* [pawamoy/copier-pdm][pawamoy/copier-pdm]: Copier template for Python projects managed by PDM.\n* [fpgmaas/cookiecutter-poetry][fpgmaas/cookiecutter-poetry]: This is a modern Cookiecutter template that can be used to initiate a Python project with all the necessary tools for development, testing, and deployment.\n* [hypermodern-python][hypermodern-python]: Hypermodern Python article series.\n\n\n[fedejaure/cookiecutter-modern-pypackage]: https://github.com/fedejaure/cookiecutter-modern-pypackage\n[pawamoy/copier-pdm]: https://github.com/pawamoy/copier-pdm\n[fpgmaas/cookiecutter-poetry]: https://github.com/fpgmaas/cookiecutter-poetry\n[hypermodern-python]: https://cjolowicz.github.io/posts/hypermodern-python-01-setup/\n',
    'author': 'Gleb Glushkov',
    'author_email': 'ptjexio@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jexio/cookiecutter-poetry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
