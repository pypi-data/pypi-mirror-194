# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proxiflow', 'proxiflow.config', 'proxiflow.core', 'proxiflow.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'numpy>=1.24.2,<2.0.0',
 'polars>=0.16.7,<0.17.0',
 'pyaml>=21.10.1,<22.0.0',
 'scipy>=1.10.1,<2.0.0']

setup_kwargs = {
    'name': 'proxiflow',
    'version': '0.1.4',
    'description': 'Data Preprocessing flow tool in python',
    'long_description': '[![image](https://badge.fury.io/py/proxiflow.svg)](https://badge.fury.io/py/proxiflow)\n[![Documentation Status](https://readthedocs.org/projects/proxiflow/badge/?version=latest)](https://proxiflow.readthedocs.io/en/latest/?badge=latest)\n[![PyPI download month](https://img.shields.io/pypi/dm/proxiflow.svg)](https://pypi.python.org/pypi/proxiflow/)\n[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/tomesm/proxiflow/graphs/commit-activity)\n[![PyPI license](https://img.shields.io/pypi/l/proxiflow.svg)](https://pypi.python.org/pypi/proxiflow/)\n[![tests](https://github.com/tomesm/proxiflow/actions/workflows/tests.yml/badge.svg)](https://github.com/tomesm/proxiflow/actions/workflows/tests.yml)\n\n\n# ProxiFlow\n\nProxiFlow is a data preparation tool for machine learning that performs\ndata cleaning, normalization, and feature engineering.\n\n## Documentation\nRead the full documentation [here](http://proxiflow.readthedocs.io/).\n\n## Usage\n\nTo use ProxiFlow, install it via pip:\n\n``` bash\npip install proxiflow\n```\n\nYou can then call it from the command line:\n\n``` bash\nproxiflow --config-file myconfig.yaml --input-file mydata.csv --output-file cleaned_data.csv\n```\n\nHere\\\'s an example of a YAML configuration file:\n\n``` yaml\ndata_cleaning:\n  remove_duplicates: True\n  handle_missing_values:\n    drop: True\n\ndata_normalization: # mandatory\n  min_max: #mandatory but values are not mandatory. It can be left empty\n    # Specify columns:\n    - Age # not mandatory\n  z_score:\n    - Price \n  log:\n    - Floors\n\nfeature_engineering:\n  ...\n```\n\nThe above configuration specifies that duplicate rows should be removed\nand missing values should be dropped.\n\n## API\n\nProxiFlow can also be used as a Python library. Here\\\'s an example:\n\n``` python\nimport polars as pl\nfrom proxiflow.config import Config\nfrom proxiflow.core import Cleaner\n\n# Load the data\ndf = pl.read_csv("mydata.csv")\n\n# Load the configuration\nconfig = Config("myconfig.yaml")\n\n# Preprocess the data\ndfl = Cleaner(config)\ncleaned_df = dfl.clean_data(df)\n\n# Write the output data\ncleaned_df.write_csv("cleaned_data.csv")\n```\n\n## TODO\n\n-   \\[x\\] Data cleaning\n-   \\[x\\] Data normalization\n-   \\[ \\] Feature engineering\n\nNote: only data cleaning is currently implemented; data normalization\nand feature engineering are TODO features.\n',
    'author': 'Martin Tomes',
    'author_email': 'tomesm@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
