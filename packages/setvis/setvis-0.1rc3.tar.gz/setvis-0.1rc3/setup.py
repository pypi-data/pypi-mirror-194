# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['setvis']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=2.3,<3.0',
 'numpy>=1.21,<2.0',
 'pandas>=1.3,<2.0',
 'pydantic>=1.8,<2.0',
 'tomli>=2.0,<3.0']

extras_require = \
{'all': ['notebook>=6.4,<7.0',
         'matplotlib>=3.4.3,<4.0.0',
         'scikit-learn>=0.2',
         'Sphinx>=4.3,<5.0',
         'pydata-sphinx-theme>=0.7,<0.8',
         'pytest>=6.2,<7.0',
         'psycopg2>=2.9,<3.0',
         'numexpr>=2.7,<3.0',
         'Bottleneck>=1.3,<2.0'],
 'db': ['psycopg2>=2.9,<3.0'],
 'doc': ['Sphinx>=4.3,<5.0', 'pydata-sphinx-theme>=0.7,<0.8'],
 'extra': ['notebook>=6.4,<7.0',
           'matplotlib>=3.4.3,<4.0.0',
           'scikit-learn>=0.2',
           'Sphinx>=4.3,<5.0',
           'pydata-sphinx-theme>=0.7,<0.8',
           'pytest>=6.2,<7.0'],
 'notebooks': ['notebook>=6.4,<7.0',
               'matplotlib>=3.4.3,<4.0.0',
               'scikit-learn>=0.2'],
 'performance-extras': ['numexpr>=2.7,<3.0', 'Bottleneck>=1.3,<2.0'],
 'test': ['pytest>=6.2,<7.0']}

setup_kwargs = {
    'name': 'setvis',
    'version': '0.1rc3',
    'description': 'Visualize set membership and missing data',
    'long_description': "# setvis\n\n[![Python Package](https://github.com/alan-turing-institute/setvis/actions/workflows/main.yml/badge.svg)](https://github.com/alan-turing-institute/setvis/actions/workflows/main.yml)\n[![Documentation Status](https://readthedocs.org/projects/setvis/badge/?version=latest)](https://setvis.readthedocs.io/en/latest/?badge=latest)\n\nSetvis is a python library for visualising set membership and patterns of missingness in data.\n\nIt can be used both programmatically and interactively in a Jupyter notebook (via Bokeh widgets).  It operates on data using a memory efficient architecture, and supports loading data from flat files, Pandas dataframes, and directly from a Postgres database.\n\n## Documentation\n\n[The setvis documentation](https://setvis.readthedocs.io/en/latest/index.html) is hosted on Read the Docs.\n\n## Installation (quick start)\n\n**For the complete installation instructions, consult [the installation page of the documentation](https://setvis.readthedocs.io/en/latest/installation.html), which includes information on some extra installation options and setting up a suitable environment on several platforms.**\n\nWe recommend installing setvis in a python virtual environment or Conda environment.\n\nTo install setvis, most users should run:\n\n```\npip install 'setvis[notebook]'\n```\n\nThis will include everything to run setvis in a notebook, and to run the tutorial examples that do not need a database connection.\n\nThe Bokeh plots produced by setvis require the package `notebook >= 6.4` to display properly.  This will be included when installing setvis using the command above.\n\n\n## Tutorials\n\nFor basic examples, please see the two example notebooks:\n- [Missingness example](https://github.com/alan-turing-institute/setvis/blob/main/notebooks/Example%20-%20import%20data%20to%20visualize%20missingness.ipynb)\n- [Set example](https://github.com/alan-turing-institute/setvis/blob/main/notebooks/Example%20-%20import%20data%20to%20visualize%20sets.ipynb)\n\nAdditionally, there is a series of Tutorials notebooks, starting with [Tutorial 1](https://github.com/alan-turing-institute/setvis/blob/main/notebooks/Tutorial%201%20-%20Overview%20and%20an%20example%20analysis.ipynb).\n\nAfter installing setvis, to follow theses tutorials interactively you will need to clone or download this repository. Then start jupyter from within it:\n\n```\npython -m jupyter notebook notebooks\n```\n\n\n## Acknowledgements\n\nThe development of the setvis software was supported by funding from the Engineering and Physical Sciences Research Council (EP/N013980/1; EP/R511717/1) and the Alan Turing Institute.\n",
    'author': 'The Setvis Maintainers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alan-turing-institute/setvis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
