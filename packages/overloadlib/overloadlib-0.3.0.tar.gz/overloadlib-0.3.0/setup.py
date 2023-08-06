# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['overloadlib']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=4.5.0,<5.0.0']}

entry_points = \
{'console_scripts': ['overloadlib = overloadlib.__main__:app']}

setup_kwargs = {
    'name': 'overloadlib',
    'version': '0.3.0',
    'description': 'A python package to implement overloading of functions in python.',
    'long_description': 'Overloadlib\n===========\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/overloadlib.svg\n   :target: https://pypi.org/project/overloadlib/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/overloadlib.svg\n   :target: https://pypi.org/project/overloadlib/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/overloadlib\n   :target: https://pypi.org/project/overloadlib\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/overloadlib\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/overloadlib/latest.svg?label=Read%20the%20Docs\n   :target: https://overloadlib.readthedocs.io/\n   :alt: Read the documentation at https://overloadlib.readthedocs.io/\n.. |Tests| image:: https://github.com/NicDom/overloadlib/workflows/Tests/badge.svg\n   :target: https://github.com/NicDom/overloadlib/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/NicDom/overloadlib/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/NicDom/overloadlib\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* Introduces ``@overload``, ``@override`` and ``@<Function>.add`` decorators, allowing one to overload and override functions. Functions are then called according to their argument types:\n\n.. code-block:: python\n\n   @overload\n   def func(var: str):\n      return var\n\n   # via @<Function>.add\n   @func.add\n   def _(var: int) -> str:\n      return str(var * 5)\n\n   # via @overload\n   @overload\n   def func() -> str:\n      return "Functions don\'t need to have arguments."\n\n   # via @override\n   @override(funcs=[func])\n   def new(str_1: str, int_1: int):\n      return str_1 * int_1\n\n   assert func("a") == "a" == new("a")\n   assert func(1) == "5" == new(1)\n   assert func() == "Functions don\'t need to have arguments." == new()\n   assert new("house", 2) == "househouse"\n\n\n* Raises human readable errors, if no callable was determined with the given arguments. For example the following given:\n\n.. code-block:: python\n\n   @overload\n   def some_func(str_1: str, int_1: int):\n      return str_1 + str(int_1)\n\n   @overload\n   def some_func(str_1: str):\n      return str_1\n\nCalling:\n\n.. code::\n\n    >>> some_func(str_1=2)\n    PyOverloadError:\n    Error when calling:\n    (__main__.some_func):\n            def some_func(str_1: int):\n                    ...:\n            \'str_1\' needs to be of type (<class \'str\'>,) (is type <class \'int\'>)\n\nor\n\n.. code-block:: python\n\n    >>> some_func(10)\n    __main__.NoFunctionFoundError: No matching function found.\n    Following definitions of \'some_func\' were found:\n    (__main__.some_func):\n            def some_func(str_1: str, int_1: int):\n                    ...\n    (__main__.some_func):\n            def some_func(str_1: str):\n                    ...\n    The following call was made:\n    (__main__.some_func):\n            def some_func(int_1: int):\n                    ...\n\n* Any type of variables is allowed: Build-in ones like ``str, int, List`` but also own ones, like classes etc.\n* ``@overload`` uses ``get_type_hints`` to identify the right function call via type-checking. Hence, it may also be used as a type-checker for functions.\n* Forgot, which overloads of a specific function have been implemented? No worries, you can print them with their typing information using `print(func_versions_info(<my_func>))`, e.g.\n\n.. code-block::\n\n   >>> print(func_versions_info(some_func))\n\n   Following overloads of \'some_func\' exist:\n   (__main__.some_func):\n            def some_func(str_1: str, int_1: int):\n                  ...\n   (__main__.some_func):\n            def some_func(str_1: str):\n                  ...\n\n\n\nRequirements\n------------\n\nRequires Python 3.7+.\n\n\nInstallation\n------------\n\nYou can install *Overloadlib* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install overloadlib\n\nor install with  ``Poetry``\n\n.. code:: console\n\n   $ poetry add overloadlib\n\n\nThen you can run\n\n.. code:: console\n\n   $ overloadlib --help\n\n\nor with  ``Poetry``:\n\n.. code:: console\n\n   $ poetry run overloadlib --help\n\n\n<details>\n<summary>Installing Poetry</summary>\n<p>\n\nTo download and install Poetry run (with curl):\n\n.. code:: console\n\n   $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -\n\n\nor on windows (without curl):\n\n.. code:: console\n\n   $ (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -\n\n\n</p>\n</details>\n\nUninstall\n~~~~~~~~~\n\nIf you wan to uninstall the package, simply run\n\n.. code:: console\n\n   $ pip uninstall overloadlib\n\n\nor with  ``Poetry``:\n\n.. code:: console\n\n   $ poetry remove overloadlib\n\n\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Overloadlib* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated by a template inspired by `@cjolowicz`_\'s `Hypermodern Python Cookiecutter`_ template and  `@TezRomacH`_\'s `python-package-template`_\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter.\n.. _python-package-template: https://github.com/TezRomacH/python-package-template\n.. _@TezRomacH: https://github.com/TezRomacH\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/NicDom/overloadlib/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://overloadlib.readthedocs.io/en/latest/usage.html\n',
    'author': 'Niclas D. Gesing',
    'author_email': 'nicdomgesing@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NicDom/overloadlib',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
