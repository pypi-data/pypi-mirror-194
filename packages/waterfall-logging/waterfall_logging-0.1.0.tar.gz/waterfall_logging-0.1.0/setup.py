# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['waterfall_logging']

package_data = \
{'': ['*']}

install_requires = \
['kaleido==0.2.1',
 'pandas>=1.5.3,<2.0.0',
 'plotly>=5.13.0,<6.0.0',
 'pyspark>=3.3.1,<4.0.0',
 'tabulate>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'waterfall-logging',
    'version': '0.1.0',
    'description': 'Waterfall statistic logging for data quality or filtering steps.',
    'long_description': '[![Version](https://img.shields.io/pypi/v/waterfall-logging)](https://pypi.org/project/waterfall-logging/)\n[![](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)\n[![Downloads](https://pepy.tech/badge/waterfall-logging)](https://pepy.tech/project/waterfall-logging)\n[!](https://img.shields.io/github/license/LouisdeBruijn/waterfall-logging)\n[![Docs - GitHub.io](https://img.shields.io/static/v1?logo=readthdocs&style=flat&color=purple&label=docs&message=waterfall-statistics)][#docs-package]\n\n[#docs-package]: https://LouisdeBruijn.github.io/waterfall-logging/\n\n# Waterfall-logging\n\nWaterfall-logging is a Python package that enables you to log column counts in a Pandas DataFrames, export it as a Markdown table and plot a Waterfall statistics figure.\n\nDocumentation with examples can be found [here](https://LouisdeBruijn.github.io/waterfall-logging).\n\nDeveloped by Louis de Bruijn, https://louisdebruijn.com.\n\n\n## Installation\n\n### Install to use\nInstall Waterfall-logging using PyPi:\n\n```commandline\npip install waterfall-logging\n```\n\n### Install to contribute\n\n```commandline\ngit clone https://github.com/LouisdeBruijn/waterfall-logging\npython -m pip install -e .\n\npre-commit install --hook-type pre-commit --hook-type pre-push\n```\n\n## Documentation\n\nDocumentation can be created via\n\n```commandline\nmkdocs serve\n```\n\n## Usage\n\nInstructions are provided in the documentation\'s [how-to-guides](https://LouisdeBruijn.github.io/waterfall-logging//how-to-guides/).\n\n```python\nimport pandas as pd\nfrom waterfall_logging.log import PandasWaterfall\n\nbicycle_rides = pd.DataFrame(data=[\n    [\'Shimano\', \'race\', 28, \'2023-02-13\', 1],\n    [\'Gazelle\', \'comfort\', 31, \'2023-02-15\', 1],\n    [\'Shimano\', \'race\', 31, \'2023-02-16\', 2],\n    [\'Batavia\', \'comfort\', 30, \'2023-02-17\', 3],\n], columns=[\'brand\', \'ride_type\', \'wheel_size\', \'date\', \'bike_id\']\n)\n\nbicycle_rides_log = PandasWaterfall(table_name=\'rides\', columns=[\'brand\', \'ride_type\', \'wheel_size\'],\n    distinct_columns=[\'bike_id\'])\nbicycle_rides_log.log(table=bicycle_rides, reason=\'Logging initial column values\', configuration_flag=\'\')\n\nbicycle_rides = bicycle_rides.loc[lambda row: row[\'wheel_size\'] > 30]\nbicycle_rides_log.log(table=bicycle_rides, reason="Remove small wheels",\n    configuration_flag=\'small_wheel=False\')\n\nprint(bicycle_rides_log.to_markdown())\n\n| Table   |   brand |   Δ brand |   ride_type |   Δ ride_type |   wheel_size |   Δ wheel_size |   bike_id |   Δ bike_id |   Rows |   Δ Rows | Reason                        | Configurations flag   |\n|:--------|--------:|----------:|------------:|--------------:|-------------:|---------------:|----------:|------------:|-------:|---------:|:------------------------------|:----------------------|\n| rides   |       4 |         0 |           4 |             0 |            4 |              0 |         3 |           0 |      4 |        0 | Logging initial column values |                       |\n| rides   |       2 |        -2 |           2 |            -2 |            2 |             -2 |         2 |          -1 |      2 |       -2 | Remove small wheels           | small_wheel=False     |\n```\n',
    'author': 'Louis de Bruijn',
    'author_email': 'None',
    'maintainer': 'Louis de Bruijn',
    'maintainer_email': 'None',
    'url': 'https://github.com/LouisdeBruijn/waterfall-logging',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
