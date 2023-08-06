# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyproject_pre_commit']

package_data = \
{'': ['*']}

install_requires = \
['autoflake==2.0.1',
 'autopep8==2.0.1',
 'bandit[toml]==1.7.4',
 'black==22.12.0',
 'blacken-docs==1.13.0',
 'flake8-annotations-complexity==0.0.7',
 'flake8-bugbear==23.2.13',
 'flake8-builtins==2.1.0',
 'flake8-comprehensions==3.10.1',
 'flake8-debugger==4.1.2',
 'flake8-docstrings==1.7.0',
 'flake8-executable==2.1.3',
 'flake8-pep3101>=2.0.0,<3.0.0',
 'flake8-print==5.0.0',
 'flake8-pyproject==1.2.2',
 'flake8-rst-docstrings==0.3.0',
 'flake8-string-format==0.3.0',
 'isort==5.12.0',
 'mdformat-footnote==0.1.1',
 'mdformat-frontmatter==0.4.1',
 'mdformat-gfm==0.3.5',
 'mdformat==0.7.16',
 'mypy==0.991',
 'pep8-naming==0.13.3',
 'pre-commit==2.21.0',
 'pycodestyle==2.10.0',
 'shellcheck-py==0.9.0.2']

entry_points = \
{'console_scripts': ['ppc = pyproject_pre_commit:main']}

setup_kwargs = {
    'name': 'pyproject-pre-commit',
    'version': '0.0.4',
    'description': 'pre-commit hooks for python projects using pyproject.toml.',
    'long_description': '# pyproject-pre-commit\n\n[![test](https://github.com/rcmdnk/pyproject-pre-commit/actions/workflows/test.yml/badge.svg)](https://github.com/rcmdnk/pyproject-pre-commit/actions/workflows/test.yml)\n[![test coverage](https://img.shields.io/badge/coverage-check%20here-blue.svg)](https://github.com/rcmdnk/pyproject-pre-commit/tree/coverage)\n\npre-commit hooks for python projects using pyproject.toml.\n\n**.pre-commit-hooks.yaml** provides pre-defined ids which you just need to add these ids to your **.pre-commit-config.yaml**.\n\n## Requirement\n\n- Python 3.11, 3.10, 3.9, 3.8\n- Poetry (For development)\n\n## Installation\n\nIf your project uses poetry, do:\n\n```\n$ poetry add --group dev pyproject-pre-commit\n```\n\nOtherwise, install by pip:\n\n```\n$ pip install pyproject-pre-commit\n```\n\n## The repository features\n\nIf you install this package, several linters/formatters will be installed, too.\n\nThis repository has following hooks for [pre-commit](https://pre-commit.com/):\n\n- For Python\n  - black-diff: Just show Black result.\n  - [black](https://black.readthedocs.io/en/stable): Black: The uncompromising Python code formatter.\n  - [blacken-docs](https://github.com/adamchainz/blacken-docs): Run `black` on python code blocks in documentation files.\n  - autoflake-diff: Just show autoflake result.\n  - [autoflake](https://github.com/PyCQA/autoflake): autoflake removes unused imports and unused variables from Python code.\n  - autopep8-diff: Just show autopep8.\n  - [autopep8](https://github.com/hhatto/autopep8): autopep8 automatically formats Python code to conform to the PEP 8 style guide.\n  - isort-diff: Just show isort result.\n  - [isort](https://github.com/PyCQA/isort): isort your imports, so you don\'t have to.\n  - [flake8](https://github.com/PyCQA/flake8): `flake8` is a command-line utility for enforcing style consistency across Python projects.\n    - With following plugins:\n      - [flake8-pyproject](https://github.com/csachs/pyproject-flake8)\n      - [flake8-annotations-complexity](https://github.com/best-doctor/flake8-annotations-complexity)\n      - [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear)\n      - [flake8-builtins](https://github.com/gforcada/flake8-builtins)\n      - [flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions)\n      - [flake8-debugger](https://github.com/jbkahn/flake8-debugger)\n      - [flake8-docstrings](https://github.com/pycqa/flake8-docstrings)\n      - [flake8-executable](https://github.com/xuhdev/flake8-executable)\n      - [flake8-pep3101](https://github.com/gforcada/flake8-pep3101)\n      - [flake8-print](https://github.com/jbkahn/flake8-print)\n      - [flake8-rst-docstrings](https://github.com/peterjc/flake8-rst-docstrings)\n      - [flake8-string-format](https://github.com/xZise/flake8-string-format)\n      - [pep8-naming](https://github.com/PyCQA/pep8-naming)\n      - [pycodestyle](https://pycodestyle.pycqa.org/en/latest/)\n  - [bandit](https://github.com/PyCQA/bandit): Bandit is a tool for finding common security issues in Python code.\n  - [mypy](https://www.mypy-lang.org/): Mypy is a static type checker for Python.\n- For Shell script\n  - [shellcheck](https://www.shellcheck.net/): ShellCheck - A shell script static analysis tool\n- For Markdown\n  - mdformat-check: Just show mdformat result.\n  - [mdformat](https://mdformat.readthedocs.io/en/stable/): CommonMark compliant Markdown formatter.\n    - with following plugins:\n      - [mdformat-gfm](https://github.com/hukkin/mdformat-gfm)\n      - [mdformat-frontmatter](https://github.com/butler54/mdformat-frontmatter)\n      - [mdformat-footnote](https://github.com/executablebooks/mdformat-footnote)\n\nAll tools are installed as dependencies of this package.\n\nshellcheck and mdformat are given in addition to python tools\nas they can be managed by pip and most projects have README.md\nand some have shell scripts.\n\nFor tools which can format files, there are additional ids ids with `-diff` or `--check`\nwhich just show the results and not modify files.\nYou can see the difference after formatting if you place these ids before ids w/o `--diff` or `--check`.\n\nYou can set options in pyproject.toml for all tools above:\n\n- flake8: flake8-pyproject allows to read options from pyproject.toml\n- bandit: There is a plugin for the flake8, but plugin version does not read options from pyproject.toml even with pyproject.toml. Therefore, use bandit directly and give `-c pyproject.toml` option in the hooks.\n\n## .pre-commit-config.yaml\n\nPrepare **.pre-commit-config.yaml** like:\n\n```yaml\nrepos:\n- repo: https://github.com/rcmdnk/pyproject-pre-commit\n  rev: v0.0.1\n  hooks:\n  - id: black-diff\n  - id: black\n  - id: blacken-docs\n  - id: autoflake-diff\n  - id: autoflake\n  - id: autopep8-diff\n  - id: autopep8\n  - id: isort-diff\n  - id: isort\n  - id: flake8\n  - id: bandit\n  - id: mypy\n  - id: shellcheck\n  - id: mdformat-check\n  - id: mdformat\n```\n\nThis can be made by `ppc` command:\n\n```\n$ ppc --pre-commit > .pre-commit-config.yaml\n```\n\nIf you already have it, add hooks w/o `repos:` by\n\n```\n$ ppc --pre-commit |grep -v "^repos:" >> .pre-commit-config.yaml\n```\n\nYou may want to modify after adding these configurations.\n\n## pyproject.toml\n\nYou can set options in pyproject.toml for all tools.\n\nExample options can be made by `ppc` command:\n\n```\n$ ppc --pyproject >> pyproject.toml\n```\n\nYou may want to modify after adding these configurations.\n',
    'author': 'rcmdnk',
    'author_email': 'rcmdnk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rcmdnk/pyproject-pre-commit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
