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
    'version': '0.9.6',
    'description': 'A library for creating even partitions of ordered items.',
    'long_description': '[![codecov](https://codecov.io/github/delusionary/histoptimizer/branch/main/graph/badge.svg?token=FCLW50JSR9)](https://codecov.io/github/delusionary/histoptimizer)\n\n# Histoptimizer\n\n## Overview\n\nHistoptimizer is a Python library and CLI that accepts a DataFrame or ordered\nlist of item sizes, and produces a list of "divider locations" that partition\nthe items as evenly as possible into a given number of buckets, minimizing the \nvariance and standard deviation between the bucket sizes.\n\nJIT compilation and GPU support through Numba provide great speed improvements\non supported hardware.\n\nThe problem that motivated its creation was: given a list of the ~3117\ncounties in the U.S., ordered  by some attribute (voting averages,\npopulation density, median age, etc.), distribute them into a number\nof buckets of approximately equal population, as evenly as possible.\n\nThat job being done, it is of questionable further use. It is fun to work on,\nthough. So.\n\n## Usage\n\nHistoptimizer provides two APIs and two command-line tools:\n\n### NumPY array partitioner\n\nSeveral implementations of the partitioning algorithm can be called directly\nwith a list or array of item sizes and a number of buckets. They return an\narray of divider locations (dividers come _after_ the given item in 1-based\nindexing, or _before_ the given item in 0-based indexing) and the variance of\nthe given partition.\n\n### Pandas Dataframe Partitioner\n\nYou can supply a Pandas DataFrame, the name of a size column, a list of bucket\nsizes, and a column prefix to get a version of the DataFrame with added columns\nwhere the value is the 1-based bucket number of the corresponding item \npartitioned into the number of buckets reflected in the column name.\n\n### CLI\n\nThe CLI is a wrapper around the DataFrame functionality that can accept and\nproduce either CSV or Pandas JSON files.\n\n```\nUsage: histoptimizer [OPTIONS] FILE ID_COLUMN SIZE_COLUMN PARTITIONS\n\n  Given a CSV, a row name column, a size column, sort key, and a number of\n  buckets, optionally sort the CSV by the given key, then distribute the\n  ordered keys as evenly as possible to the given number of buckets.\n\n  Example:\n\n      > histoptimizer states.csv state_name population 10\n\n      Output:\n\n      state_name, population, partition_10     Wyoming, xxxxxx, 1\n      California, xxxxxxxx, 10\n\nOptions:\n  -l, --limit INTEGER             Take the first {limit} records from the\n                                  input, rather than the whole file.\n  -a, --ascending, --asc / -d, --descending, --desc\n                                  If a sort column is provided,\n  --print-all, --all / --no-print-all, --brief\n                                  Output all columns in input, or with\n                                  --brief, only output the ID, size, and\n                                  buckets columns.\n  -c, --column-prefix TEXT        Partition column name prefix. The number of\n                                  buckets will be appended. Defaults to\n                                  partion_{number of buckets}.\n  -s, --sort-key TEXT             Optionally sort records by this column name\n                                  before partitioning.\n  -t, --timing / --no-timing      Print partitioner timing information to\n                                  stderr\n  -i, --implementation TEXT       Use the named partitioner implementation.\n                                  Defaults to "dynamic_numba". If you have an\n                                  NVidia GPU use "cuda" for better performance\n  -o, --output FILENAME           Send output to the given file. Defaults to\n                                  stdout.\n  -f, --output-format [csv|json]  Specify output format. Pandas JSON or CSV.\n                                  Defaults to CSV\n  --help                          Show this message and exit.\n```\n\n### Benchmarking CLI\n\nThe Benchmarking CLI can be used to produce comparative performance metrics for \nvarious implementations of the algorithm.\n\n```\nUsage: histobench [OPTIONS] PARTITIONER_TYPES [ITEM_SPEC] [BUCKET_SPEC]\n                  [ITERATIONS] [SIZE_SPEC]\n\n  Histobench is a benchmarking harness for testing Histoptimizer partitioner\n  performance.\n\n  By Default it uses random data, and so may not be an accurate benchmark for\n  algorithms whose performance depends upon the data set.\n\n  The PARTITIONER_TYPES parameter is a comma-separated list of partitioners to\n  benchmark, which can be specified as either:\n\n  1. A standard optimizer name, or 2. filepath:classname\n\n  To specify the standard cuda module and also a custom variant, for example,\n\nOptions:\n  --debug-info / --no-debug-info\n  --force-jit / --no-force-jit\n  --report PATH\n  --sizes-from PATH\n  --tables / --no-tables\n  --verbose / --no-verbose\n  --help                          Show this message and exit.\n```\n\n## JIT SIMD Compilation and CUDA acceleration\n\nHistoptimizer supports Just-in-time compilation for both CPU and NVidia CUDA\nGPUs using Numba. For larger problems these implementations can be hundreds or\nthousands of times faster than the pure Python implementation.\n',
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
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
