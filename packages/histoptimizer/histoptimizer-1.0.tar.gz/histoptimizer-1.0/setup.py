# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['histoptimizer', 'histoptimizer.historical']

package_data = \
{'': ['*']}

install_requires = \
['click>=8,<9', 'numba>=0.56,<0.57', 'numpy>=1,<2', 'pandas>=1.5,<2.0']

entry_points = \
{'console_scripts': ['histobench = histoptimizer.benchmark:cli',
                     'histoptimizer = histoptimizer.cli:cli']}

setup_kwargs = {
    'name': 'histoptimizer',
    'version': '1.0',
    'description': 'A library for creating even partitions of ordered items.',
    'long_description': '[![codecov](https://codecov.io/github/delusionary/histoptimizer/branch/main/graph/badge.svg?token=FCLW50JSR9)](https://codecov.io/github/delusionary/histoptimizer)\n\n# Histoptimizer\n\n## Overview\n\nHistoptimizer is a Python library and CLI that accepts a DataFrame or ordered\nlist of item sizes, and produces a list of "divider locations" that partition\nthe items as evenly as possible into a given number of buckets, minimizing the \nvariance and standard deviation between the bucket sizes.\n\nJIT compilation and GPU support through Numba provide great speed improvements\non supported hardware, enabling problem sets of a million items or more.\n\nHistoptimizer was built in order to divide the counties of the US precisely\ninto intervals ordered by population density. That job was accomplished very\nearly on, and no other uses have been discovered. It is unclear why development\nhas continued to this point.\n\n## Usage\n\nHistoptimizer provides two APIs and two command-line tools:\n\n### NumPY array partitioner\n\nSeveral implementations of the partitioning algorithm can be called directly\nwith a list or array of item sizes and a number of buckets. They return an\narray of divider locations (dividers come _after_ the given item in 1-based\nindexing, or _before_ the given item in 0-based indexing) and the variance of\nthe given partition.\n\n```python\nfrom histoptimizer import Histoptimizer\n\nitem_sizes = [1.0, 4.5, 6.3, 2.1, 8.4, 3.7, 8.6, 0.3, 5.2, 6.9, 1.2, 2.4, 9.8, 3.7]\n\n# Get the optimal position of two dividers that partition the list above into 3 buckets.\n(dividers, variance) = Histoptimizer.partition(item_sizes, 3)\n\nprint(f"Optimal Divider Locations: {dividers} Optimal solution variance: {variance:.4}")\n```\n\n### Pandas Dataframe Partitioner\n\nYou can supply a Pandas DataFrame, the name of a size column, a list of bucket\nsizes, and a column prefix to get a version of the DataFrame with added columns\nwhere the value is the 1-based bucket number of the corresponding item \npartitioned into the number of buckets reflected in the column name.\n\n```python\nfrom histoptimizer import histoptimize\nimport pandas as pd\n\nbooks = pd.read_csv(\'books.csv\', header=0)\ndivisions, column_names = histoptimize(books, "Pages", [3], "assistant_", Histoptimizer)\ndivisions\n```\n\n|     | Title                          |   Pages | assistant_3 |\n|----:|:-------------------------------|--------:|------------:|\n|   0 | The Algorithm Design Manual    |     748 |           1 |\n|   1 | Software Engineering at Google |     599 |           1 |\n|   2 | Site Reliability Engineering   |     550 |           2 |\n|  .. | ...                            |   ...   |         ... |\n|  14 | Noise                          |     464 |           3 |\n|  15 | Snow Crash                     |     440 |           3 |\n\n\n### CLI\n\nThe CLI is a wrapper around the DataFrame functionality that can accept and\nproduce either CSV or Pandas JSON files.\n\n```\nUsage: histoptimizer [OPTIONS] FILE SIZE_COLUMN PARTITIONS\n\n  Partition ordered items in a CSV into a given number of buckets,       \n  evenly.\n\n  Given a CSV or JSON Dataframe, a size column name, and a number of     \n  buckets, Histoptimizer will add a column which gives the partition     \n  number for each row that optimally divides the given items into the    \n  buckets so as to minimize the variance from mean of the summed items   \n  in each bucket.\n\n  Additional features allow doing a list of bucket sizes in one go,      \n  sorting items beforehand, and producing output with only relevant      \n  columns.\n\n  Example:\n\n      > histoptimizer books.csv state_name population 10\n\n      Output:\n\n      state_name, population, partition_10     Wyoming, xxxxxx, 1        \n      California, xxxxxxxx, 10\n\nOptions:\n  -l, --limit INTEGER             Take the first {limit} records from    \n                                  the input, rather than the whole       \n                                  file.\n  -a, --ascending, --asc / -d, --descending, --desc\n                                  If a sort column is provided,\n  --print-all, --all / --no-print-all, --brief\n                                  Output all columns in input, or with   \n                                  --brief, only output the ID, size,     \n                                  and buckets columns.\n  -c, --column-prefix TEXT        Partition column name prefix. The      \n                                  number of buckets will be appended.    \n                                  Defaults to partion_{number of\n                                  buckets}.\n  -s, --sort-key TEXT             Optionally sort records by this        \n                                  column name before partitioning.       \n  -i, --id-column TEXT            Optional ID column to print with       \n                                  brief output.\n  -p, --partitioner TEXT          Use the named partitioner\n                                  implementation. Defaults to "numba".   \n                                  If you have an NVidia GPU use "cuda"   \n                                  for better performance\n  -o, --output FILENAME           Send output to the given file.\n                                  Defaults to stdout.\n  -f, --output-format [csv|json]  Specify output format. Pandas JSON or  \n                                  CSV. Defaults to CSV\n  --help                          Show this message and exit.\n```\n\n### Benchmarking CLI\n\nThe Benchmarking CLI can be used to produce comparative performance metrics for \nvarious implementations of the algorithm.\n\n```\nUsage: histobench [OPTIONS] PARTITIONER_TYPES [ITEM_SPEC] [BUCKET_SPEC]\n                  [ITERATIONS] [SIZE_SPEC]\n\n  Histobench is a benchmarking harness for testing Histoptimizer partitioner\n  performance.\n\n  By Default it uses random data, and so may not be an accurate benchmark for\n  algorithms whose performance depends upon the data set.\n\n  The PARTITIONER_TYPES parameter is a comma-separated list of partitioners to\n  benchmark, which can be specified as either:\n\n  1. A standard optimizer name, or 2. filepath:classname\n\n  To specify the standard cuda module and also a custom variant, for example,\n\nOptions:\n  --debug-info / --no-debug-info\n  --force-jit / --no-force-jit\n  --report PATH\n  --sizes-from PATH\n  --tables / --no-tables\n  --verbose / --no-verbose\n  --help                          Show this message and exit.\n```\n\n',
    'author': 'Kelly Joyner',
    'author_email': 'de@lusion.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://histoptimizer.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
