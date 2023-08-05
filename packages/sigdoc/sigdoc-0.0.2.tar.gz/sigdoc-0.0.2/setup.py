# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sigdoc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sigdoc',
    'version': '0.0.2',
    'description': 'Inline documentation of parameters, returns, and raises',
    'long_description': '# sigdoc\n\n[![pypi](https://img.shields.io/pypi/v/sigdoc.svg)](https://pypi.python.org/pypi/sigdoc)\n[![downloads](https://pepy.tech/badge/sigdoc/month)](https://pepy.tech/project/sigdoc)\n[![versions](https://img.shields.io/pypi/pyversions/sigdoc.svg)](https://github.com/JacobHayes/sigdoc)\n[![license](https://img.shields.io/github/license/JacobHayes/sigdoc.svg)](https://github.com/JacobHayes/sigdoc/blob/golden/LICENSE)\n[![CI](https://github.com/JacobHayes/sigdoc/actions/workflows/ci.yaml/badge.svg)](https://github.com/JacobHayes/sigdoc/actions/workflows/ci.yaml)\n[![codecov](https://codecov.io/gh/JacobHayes/sigdoc/branch/golden/graph/badge.svg?token=6LUCpjcGdN)](https://codecov.io/gh/JacobHayes/sigdoc)\n\nInline documentation of parameters, returns, and raises.\n\n---\n\nDocumenting function parameters and returns in docstrings is tedious - type hints need to be duplicated, the order is hard to maintain, and added/removed params and returns easily get out of sync.\n\n`sigdoc` provides helpers to automatically extend docstrings _at runtime_ by annotating a function\'s parameter and return type hints "inline". This inline notation greatly increases the locality of the code and documentation, reducing the maintenance burden.\n\n![](https://raw.githubusercontent.com/JacobHayes/sigdoc/main/docs/jupyter-help.png)\n\nAs this relies on runtime generation, the full docstring will only be visible to runtime inspection. Luckily, this includes `help(...)` in `python`, `ipython`, and `jupyter` (including `Shift+Tab`). Static analysis tools (such as many IDEs) won\'t know how to decipher the full docstring, but often show the function\'s signature, which will still have all of the useful information included.\n\n## Installation\n\n`sigdoc` can be installed from PyPI on python 3.9+ with `pip install sigdoc`.\n\n## Contributing\n\nEveryone is welcome to contribute - feel free to open an issue or PR!\n',
    'author': 'Jacob Hayes',
    'author_email': 'jacob.r.hayes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/JacobHayes/sigdoc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
