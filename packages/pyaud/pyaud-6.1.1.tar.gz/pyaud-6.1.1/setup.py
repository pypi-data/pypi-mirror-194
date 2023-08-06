# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaud']

package_data = \
{'': ['*']}

install_requires = \
['arcon>=0.2.1,<0.3.0',
 'gitpython>=3.1.30,<4.0.0',
 'lsfiles>=0.5',
 'object-colors>=2.0.1,<3.0.0',
 'pyaud-plugins>=0.8',
 'spall>=0,<1']

entry_points = \
{'console_scripts': ['pyaud = pyaud.__main__:main']}

setup_kwargs = {
    'name': 'pyaud',
    'version': '6.1.1',
    'description': 'Framework for writing Python package audits',
    'long_description': 'pyaud\n=====\n.. image:: https://img.shields.io/badge/License-MIT-yellow.svg\n    :target: https://opensource.org/licenses/MIT\n    :alt: License\n.. image:: https://img.shields.io/pypi/v/pyaud\n    :target: https://pypi.org/project/pyaud/\n    :alt: PyPI\n.. image:: https://github.com/jshwi/pyaud/actions/workflows/build.yaml/badge.svg\n    :target: https://github.com/jshwi/pyaud/actions/workflows/build.yaml\n    :alt: Build\n.. image:: https://github.com/jshwi/pyaud/actions/workflows/codeql-analysis.yml/badge.svg\n    :target: https://github.com/jshwi/pyaud/actions/workflows/codeql-analysis.yml\n    :alt: CodeQL\n.. image:: https://results.pre-commit.ci/badge/github/jshwi/pyaud/master.svg\n   :target: https://results.pre-commit.ci/latest/github/jshwi/pyaud/master\n   :alt: pre-commit.ci status\n.. image:: https://codecov.io/gh/jshwi/pyaud/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/pyaud\n    :alt: codecov.io\n.. image:: https://readthedocs.org/projects/pyaud/badge/?version=latest\n    :target: https://pyaud.readthedocs.io/en/latest/?badge=latest\n    :alt: readthedocs.org\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: Black\n.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336\n    :target: https://pycqa.github.io/isort/\n    :alt: isort\n.. image:: https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg\n    :target: https://github.com/PyCQA/docformatter\n    :alt: docformatter\n.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen\n    :target: https://github.com/PyCQA/pylint\n    :alt: pylint\n.. image:: https://img.shields.io/badge/security-bandit-yellow.svg\n    :target: https://github.com/PyCQA/bandit\n    :alt: Security Status\n.. image:: https://snyk.io/test/github/jshwi/pyaud/badge.svg\n    :target: https://snyk.io/test/github/jshwi/pyaud/badge.svg\n    :alt: Known Vulnerabilities\n.. image:: https://snyk.io/advisor/python/pyaud/badge.svg\n    :target: https://snyk.io/advisor/python/pyaud\n    :alt: pyaud\n\nFramework for writing Python package audits\n-------------------------------------------\n\nThe ``pyaud`` framework is designed for writing modular audits for Python packages\n\nAudits can be run to fail, such as when using CI, or include a fix\n\nFixes can be written for whole directories or individual files\n\nPlugins can be written for manipulating files\n\nSupports single script plugins\n\nInstallation\n------------\n\n.. code-block:: console\n\n    $ pip install pyaud\n\nUsage\n-----\n\nCommandline\n***********\n\n.. code-block:: console\n\n    usage: pyaud [-h] [-v] [-f] [-n] [-s] [--audit LIST] [--exclude EXCLUDE] MODULE\n\n    positional arguments:\n      MODULE             choice of module: [modules] to list all\n\n    optional arguments:\n      -h, --help         show this help message and exit\n      -v, --version      show program\'s version number and exit\n      -f, --fix          suppress and fix all fixable issues\n      -n, --no-cache     disable file caching\n      -s, --suppress     continue without stopping for errors\n      --audit LIST       comma separated list of plugins for audit\n      --exclude EXCLUDE  regex of paths to ignore\n\nPlugins\n*******\n\n``pyaud`` will search for a plugins package in the project root\n\nTo register a plugin package ensure it is importable and prefix the package with ``pyaud_``\n\nThe name ``pyaud_plugins`` is reserved and will be automatically imported\n\nTo view available plugins see ``pyaud-plugins`` `README <https://github.com/jshwi/pyaud-plugins/blob/master/README.rst>`_ or run ``pyaud modules all``\n\nFor writing plugins see `docs <https://jshwi.github.io/pyaud/pyaud.html#pyaud-plugins>`_\n\nConfigure\n*********\n\nConfiguration values are declared in the pyproject.toml file\n\n.. code-block:: toml\n\n    [tool.pyaud]\n    audit = [\n      "commit-policy",\n      "const",\n      "docs",\n      "files",\n      "format",\n      "format-docs",\n      "format-str",\n      "imports",\n      "lint",\n      "params",\n      "test",\n      "typecheck",\n      "unused"\n    ]\n    exclude = \'\'\'\n      (?x)^(\n        | docs\\/conf\\.py\n        | whitelist\\.py\n      )$\n    \'\'\'\n',
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': 'jshwi',
    'maintainer_email': 'stephen@jshwisolutions.com',
    'url': 'https://pypi.org/project/pyaud/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
