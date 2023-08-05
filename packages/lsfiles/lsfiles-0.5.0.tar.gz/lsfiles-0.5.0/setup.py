# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lsfiles']

package_data = \
{'': ['*']}

install_requires = \
['gitpython>=3.1.31,<4.0.0']

setup_kwargs = {
    'name': 'lsfiles',
    'version': '0.5.0',
    'description': 'Path object VC index',
    'long_description': 'lsfiles\n=======\n.. image:: https://img.shields.io/badge/License-MIT-yellow.svg\n    :target: https://opensource.org/licenses/MIT\n    :alt: License\n.. image:: https://img.shields.io/pypi/v/lsfiles\n    :target: https://pypi.org/project/lsfiles/\n    :alt: PyPI\n.. image:: https://github.com/jshwi/lsfiles/actions/workflows/build.yaml/badge.svg\n    :target: https://github.com/jshwi/lsfiles/actions/workflows/build.yaml\n    :alt: Build\n.. image:: https://github.com/jshwi/lsfiles/actions/workflows/codeql-analysis.yml/badge.svg\n    :target: https://github.com/jshwi/lsfiles/actions/workflows/codeql-analysis.yml\n    :alt: CodeQL\n.. image:: https://results.pre-commit.ci/badge/github/jshwi/lsfiles/master.svg\n   :target: https://results.pre-commit.ci/latest/github/jshwi/lsfiles/master\n   :alt: pre-commit.ci status\n.. image:: https://codecov.io/gh/jshwi/lsfiles/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/lsfiles\n    :alt: codecov.io\n.. image:: https://readthedocs.org/projects/lsfiles/badge/?version=latest\n    :target: https://lsfiles.readthedocs.io/en/latest/?badge=latest\n    :alt: readthedocs.org\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: Black\n.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336\n    :target: https://pycqa.github.io/isort/\n    :alt: isort\n.. image:: https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg\n    :target: https://github.com/PyCQA/docformatter\n    :alt: docformatter\n.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen\n    :target: https://github.com/PyCQA/pylint\n    :alt: pylint\n.. image:: https://img.shields.io/badge/security-bandit-yellow.svg\n    :target: https://github.com/PyCQA/bandit\n    :alt: Security Status\n.. image:: https://snyk.io/test/github/jshwi/pyaud/badge.svg\n    :target: https://snyk.io/test/github/jshwi/pyaud/badge.svg\n    :alt: Known Vulnerabilities\n.. image:: https://snyk.io/advisor/python/lsfiles/badge.svg\n    :target: https://snyk.io/advisor/python/lsfiles\n    :alt: lsfiles\n\nPath object VC index\n--------------------\n\nIndex versioned .py files\n\nInstall\n-------\n\n``pip install lsfiles``\n\nDevelopment\n-----------\n\n``poetry install``\n\nUsage\n-----\n\n\nThe ``LSFiles`` instance is a list-like object instantiated with an empty index\n\n.. code-block:: python\n\n    >>> from lsfiles import LSFiles\n    >>> from pathlib import Path\n    >>>\n    >>> files = LSFiles()\n    >>> files\n    <LSFiles []>\n\n\nThe ``LSFiles`` index calls ``git ls-files`` and only versioned files are indexed\n\n.. code-block:: python\n\n    >>> files.populate()\n    >>> for path in sorted([p.relative_to(Path.cwd()) for p in files]):\n    ...     print(path)\n    docs/conf.py\n    lsfiles/__init__.py\n    lsfiles/_indexing.py\n    lsfiles/_objects.py\n    lsfiles/_version.py\n    tests/__init__.py\n    tests/_environ.py\n    tests/_test.py\n    tests/conftest.py\n    whitelist.py\n\nThe ``LSFiles`` instance is an index of unique file paths\n\nIt\'s implementation of ``extend`` prevents duplicates\n\n.. code-block:: python\n\n    >>> p1 = Path.cwd() / "f1"\n    >>> p2 = Path.cwd() / "f1"\n    >>>\n    >>> files = LSFiles()\n    >>> files.extend([p1, p2])\n    >>> sorted([p.relative_to(Path.cwd()) for p in files.reduce()])\n    [PosixPath(\'f1\')]\n\nReduce minimizes index to directories and individual files relative to the current working dir\n\nThe list value is returned, leaving the instance unaltered\n\n.. code-block:: python\n\n    >>> p1 = Path.cwd() / "f1"\n    >>>\n    >>> d = Path.cwd() / "dir"\n    >>> p2 = d / "f2"\n    >>> p3 = d / "f3"\n    >>>\n    >>> files = LSFiles()\n    >>> files.extend([p1, p2, p3])\n    >>> sorted(p.relative_to(Path.cwd()) for p in files.reduce())\n    [PosixPath(\'dir\'), PosixPath(\'f1\')]\n\nExclusions can be added on instantiation\n\nExclusions are evaluated by their basename, and does not have to be an absolute path\n\n.. code-block:: python\n\n    >>> p1 = Path.cwd() / "docs" / "conf.py"\n    >>> p2 = Path.cwd() / "lsfiles" / "__init__.py"\n    >>>\n    >>> files = LSFiles()\n    >>> files.populate(f".*\\/{p1.name}")\n    >>>\n    >>> ps = [str(p) for p in files]\n    >>>\n    >>> assert not str(p1) in ps\n    >>> assert str(p2) in ps\n',
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': 'jshwi',
    'maintainer_email': 'stephen@jshwisolutions.com',
    'url': 'https://pypi.org/project/lsfiles/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
