# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lil_nocap']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.2,<2.0.0', 'pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'lil-nocap',
    'version': '0.2.3',
    'description': 'A package for downloading bulk files from courtlistener',
    'long_description': "# Easy Bulk export, no cap\nThis repository provides scripts and notebooks that make it easy to export data in bulk from CourtListener's freely available downloads.\n\n##\n* [x] Create first version of notebook suitable for Data Scientists\n  * [x] Create the appropriate _dtypes_ to optimize panda storage\n  * [x] Select necessary cols _usecols_, for example 'created_by' date field indicating a database _insert_ isn't necessary\n  * [x] Read the _opinions.csv_ (190+gb) chunk at a time from disk while converting into JSON\n* [ ] Create a standalone script that can be piped to other tools\n  * [*] Create PyPi library using [Poetry](https://python-poetry.org/): [package](https://pypi.org/project/lil-nocap)\n  * [ ] Output script using [json lines](https://jsonlines.org/examples/) format\n* [ ] Improve speed by using [DASK DataFrame](https://docs.dask.org/en/stable/dataframe.html)\n\n",
    'author': 'sabzo',
    'author_email': 'sabelo@sabelo.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
