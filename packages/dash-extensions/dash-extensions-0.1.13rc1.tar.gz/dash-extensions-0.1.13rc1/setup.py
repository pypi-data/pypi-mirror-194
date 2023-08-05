# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dash_extensions']

package_data = \
{'': ['*'], 'dash_extensions': ['file_system_store/*']}

install_requires = \
['Flask-Caching==2.0.2',
 'dash>=2.8.1',
 'jsbeautifier>=1.14.3,<2.0.0',
 'more-itertools>=9.0.0,<10.0.0']

extras_require = \
{'mantine': ['dash-mantine-components>=0.11.0,<0.12.0']}

setup_kwargs = {
    'name': 'dash-extensions',
    'version': '0.1.13rc1',
    'description': 'Extensions for Plotly Dash.',
    'long_description': '[![PyPI Latest Release](https://img.shields.io/pypi/v/dash-extensions.svg)](https://pypi.org/project/dash-extensions/)\n[![codecov](https://img.shields.io/codecov/c/github/thedirtyfew/dash-extensions?logo=codecov)](https://codecov.io/gh/thedirtyfew/dash-extensions)\n[![Testing](https://github.com/thedirtyfew/dash-extensions/actions/workflows/python-test.yml/badge.svg)](https://github.com/thedirtyfew/dash-extensions/actions/workflows/python-test.yml)\n[![CodeQL](https://github.com/thedirtyfew/dash-extensions/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/thedirtyfew/dash-extensions/actions/workflows/codeql-analysis.yml)\n\nThe `dash-extensions` package is a collection of utility functions, syntax extensions, and Dash components that aim to improve the Dash development experience. It can be divided in four main pillars,\n\n* The `enrich` module, which contains various enriched versions of Dash components\n* A number of custom components, e.g. the `Websocket` component, which enables real-time communication and push notifications\n* The `javascript` module, which contains functionality to ease the interplay between Dash and JavaScript\n* The `snippets` module, which contains a collection of utility functions (documentation limited to source code comments)\n\nThe `enrich` module enables a number of _transforms_ that add functionality and/or syntactic sugar to Dash. Examples include\n\n* Making it possible to target an `Output` by multiple callbacks via the `MultiplexerTransform`\n* Enabling logging from within Dash callbacks via the `LogTransform`\n* Improving app performance via the `ServersideOutputTransform`\n\nto name a few. To enable interactivity, the documentation has been moved to a [separate page](http://dash-extensions.com).\n\nNB: The 0.1.0 version introduces a number of breaking changes, see the changelog for details.\n',
    'author': 'emher',
    'author_email': 'emil.h.eriksen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://dash-extensions.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
