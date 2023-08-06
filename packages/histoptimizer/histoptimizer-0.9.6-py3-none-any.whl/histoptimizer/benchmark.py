"""Implements Histoptimizer benchmark CLI.

The CLI is a simple tool for measuring and comparing the performance of various
implementations of Histoptimizer. It is not likely to be useful unless you are
developing such implementations. If you are just using the tool:
cuda > numba > dynamic.

Copyright (C) 2020 by Kelly Joyner (de@lusion.org)

Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
THIS SOFTWARE.
"""
import platform
import uuid
import re
import sys
import time
from math import ceil, log10
import importlib.machinery
import importlib.util

import click
import numpy as np
import pandas as pd

from histoptimizer import Histoptimizer
from histoptimizer.cli import parse_set_spec
from histoptimizer.cuda import CUDAOptimizer
from histoptimizer.historical.cuda_2 import CUDAOptimizerItemPairs
from histoptimizer.historical.enumerate import EnumeratingOptimizer
from histoptimizer.historical.recursive import RecursiveOptimizer
from histoptimizer.historical.recursive_cache import RecursiveCacheOptimizer
from histoptimizer.numba_optimizer import NumbaOptimizer

partitioners = {c.name: c for c in (
    Histoptimizer,
    CUDAOptimizer,
    NumbaOptimizer,
    CUDAOptimizerItemPairs,
    EnumeratingOptimizer,
    RecursiveOptimizer,
    RecursiveCacheOptimizer,
)}


def get_system_info() -> dict:
    """

    """
    system = {
        'system': platform.system()
    }

    return system


def partitioner_pivot(df: pd.DataFrame, partitioner) -> pd.DataFrame:
    """
    Given a DataFrame of results produced by histobench, and the name of a
    partitioner, isolate results of that partitioner and create a pivot table
    on bucket, so that the frame becomes a grid with # items in rows and
    # buckets in columns.

    Args:
        df (DataFrame)
            Results DataFrame.
        partitioner (str)
            partitioner name to isolate.

    Returns:
        Pivoted Dataframe with performance data for the specified partitioner.
    """
    return df[df.partitioner == partitioner].groupby(
        ['num_items', 'buckets'],
        as_index=False) \
        .mean(numeric_only=True) \
        .pivot(index=['num_items'],
               columns='buckets',
               values='elapsed_seconds')


def benchmark(partitioner_list: list, item_list: list, bucket_list: list,
              iterations: int = 1,
              begin_range: int = 1, end_range: int = 10,
              specified_items_sizes: list = None, verbose: bool = False,
              include_items_in_results: bool = False) \
        -> pd.DataFrame:
    """Benchmark a given list of partitioners against the same data.

    The caller can specify that the partitioners be

    Args:
        partitioner_list
            List of partitioner functions to benchmark.
        item_list
            A list of item counts to benchmark.
        bucket_list
            A list bucket counts to benchmark.
        iterations
            Number of iterations to test each item_list x bucket_list
            combination.
        begin_range
            For random item generation, the lower bound of the random
            size values.
        end_range
            For random item generation, the upper bound of the random
            size values.
        specified_items_sizes
            An ordered list of item sizes. Must be as long as
            the max value of item_list.
        verbose
            If true, log debugging information.
        include_items_in_results
            If true, include the items used in the test in every result row.

    Returns:
        pandas.DataFrame: DataFrame containing one row for each
            partitioner x item size x bucket size x iteration.

        Each row contains the following columns:

            partitioner (str)
                Name of the partitioner used in this run.
            num_items
                Number of items in this run.
            buckets
                Number of buckets in this run.
            iteration
                Iteration number for this run.
            item_set_id
                32-bit hex form of a random UUID generated when the items
                used in the problem were generated.
            variance
                Variance of the discovered solution.
            elapsed_seconds
                Number of seconds to find the solution.
            dividers (list)
                Divider locations for the optimal solution.
            items
                List of items sizes for this run, if `include_item_sizes`
                is `True`


    Raises:
    """
    r = pd.DataFrame(
        columns=['partitioner', 'num_items', 'buckets', 'iteration',
                 'variance', 'elapsed_seconds', 'dividers', 'item_set_id'])
    dividers = None

    for num_items in item_list:
        for num_buckets in bucket_list:
            results = []
            for i in range(1, iterations + 1):
                item_set_id = uuid.uuid4().hex
                if specified_items_sizes is None:
                    items = np.random.randint(begin_range, end_range + 1,
                                              size=num_items)
                else:
                    items = specified_items_sizes[:num_items]
                for partitioner in partitioner_list:
                    start = time.time()
                    dividers, variance = partitioner.partition(items,
                                                               num_buckets)
                    end = time.time()
                    new_result = {
                        'partitioner': partitioner.name,
                        'num_items': num_items,
                        'buckets': num_buckets,
                        'iteration': i,
                        'item_set_id': item_set_id,
                        'variance': variance,
                        'elapsed_seconds': end - start,
                        'dividers': dividers,
                    }

                    if include_items_in_results:
                        new_result['items'] = items

                    results.append(new_result)

            r = pd.concat([r, pd.DataFrame.from_records(results)])
            mean = r[(r.num_items == num_items) & (
                    r.buckets == num_buckets)].groupby('partitioner').mean(
                numeric_only=True)
            if verbose:
                click.echo(
                    f'Items: {num_items} Buckets: {num_buckets}'
                    f' Mean values over {iterations} iterations:')
                click.echo(f'Partitioner\t\tTime (ms)\t\tVariance\t\tDividers')
                for partitioner, record in mean.iterrows():
                    click.echo(
                        f'{partitioner}\t\t\t'
                        f'{record.elapsed_seconds * 1000:.2f}'
                        f'\t\\t\t{record.variance:.4f}\t\t{list(dividers)}')
    return r


def echo_tables(partitioner_list: list, r: pd.DataFrame):
    """
    Output (via click.echo) a table of results for the given partitioner.

    Args:
        partitioner_list: List of partitioners to generate output for.
        r: A DataFrame of results produced by the benchmark function.
    """
    for partitioner in (p.name for p in partitioner_list):
        grid = partitioner_pivot(r, partitioner)
        # wide enough for the widest value.
        items_width = ceil(log10(max([grid.index.max(), 10]))) + 2
        # Max digits we have + ".000" + 2 spaces
        width = ceil(log10(max([grid.max().max(), 10]))) + 6
        click.echo(
            f'Partitioner: {partitioner}\n{"".rjust(items_width)}' + ''.join(
                [str(x).rjust(width) for x in grid.columns]))
        for num_items in grid.index:
            click.echo(str(num_items).rjust(items_width) + ''.join(
                [f'{float(grid[grid.index == num_items][x]):.3f}'.rjust(width)
                 for x in grid.columns]))
        click.echo()


def get_sizes_from(file_path: str) -> np.ndarray:
    """
    Read sizes from the given file path.

    Args:
        file_path: Path to a CSV file with one column, or a JSON file where each
            object has one attribute. The values in the field must cast
            to float.

    Returns:
        A list of item sizes in the same order as read from the file.
    Raises:
        ValueError if the file does not contain CSV with a single column or a
            JSON dataframe with a single attribute.
    """
    specified_items_sizes = None
    if file_path is not None:
        if '.json' in file_path:
            specified_items = pd.read_json(file_path, orient='records')
        elif '-' == file_path:
            specified_items = pd.read_csv(sys.stdin)
        else:
            specified_items = pd.read_csv(file_path)
        if len(specified_items.columns) != 1:
            raise ValueError(
                f'Files specified with --sizes-from must contain a CSV or JSON'
                f'DataFrame with one (1) column. Found {len(specified_items)}'
                f'columns instead.')
        try:
            specified_items_sizes = np.array(
                specified_items[specified_items.columns[0]], dtype=np.float32)
        except ValueError as e:
            raise ValueError(
                f'Files specified with --sizes-from must contain a single'
                f'column of Float32-coercible values: {str(e)}')
    return specified_items_sizes


def write_report(r: pd.DataFrame, report: str):
    """Write the given results DataFrame to the given file.

    If the filename ends in '.json', JSON is generated, otherwise CSV. The
    special value '-' can be used to write the results to stdout.

    Args:
        r: Results DataFrame
        report: Path to report file.
    Returns:
        Nothing
    Raises:
        IOError if the file cannot be opened for writing.
    """
    if ".json" in report.lower():
        r.to_json(report, orient="records")
    elif report == '-':
        r.to_csv(sys.stdout, index=False)
    else:
        r.to_csv(report, index=False)


@click.command()
@click.argument('partitioner_types', type=str, required=True)
@click.argument('item_spec', type=str, default="15")
@click.argument('bucket_spec', type=str, default="8")
@click.argument('iterations', type=int, default=1)
@click.argument('size_spec', type=str, default='1-10')
@click.option('--debug-info/--no-debug-info', type=bool, default=False)
@click.option('--force-jit/--no-force-jit', type=bool, default=True)
@click.option('--report', type=click.Path(writable=True, allow_dash=True))
@click.option('--sizes-from', type=click.Path(exists=True, allow_dash=True),
              default=None)
@click.option('--tables/--no-tables', type=bool, default=False)
@click.option('--verbose/--no-verbose', type=bool, default=False)
@click.option('--include-items/--no-include-items', type=bool, default=False)
def cli(partitioner_types, item_spec, bucket_spec, iterations, size_spec,
        debug_info, force_jit, report, sizes_from, tables, verbose,
        include_items):
    """
    Histobench is a benchmarking harness for testing Histoptimizer partitioner
    performance.

    By Default it uses random data, and so may not be an accurate benchmark for
    algorithms whose performance depends upon the data set.

    The PARTITIONER_TYPES parameter is a comma-separated list of partitioners
    to benchmark, which can be specified as either:

    1. A standard optimizer name, or
    2. filepath:classname

    To specify the standard cuda module and also a custom variant, for example,
    one could use: cuda,./old_optimizers/cuda_20221130.py:CUDAOptimizer20221130



    Args:

    Returns:

    Raises:

    """

    partitioner_list = get_partitioners(partitioner_types)
    specified_items_sizes = get_sizes_from(sizes_from)

    item_variable_dict = {}
    if specified_items_sizes is not None:
        item_variable_dict['n'] = len(specified_items_sizes)

    bucket_list = parse_set_spec(bucket_spec)
    item_list = parse_set_spec(item_spec, item_variable_dict)
    if match := re.match(r'(\d+)-(\d+)$', size_spec):
        begin_range, end_range = map(int, match.groups())
        if end_range < begin_range:
            begin_range, end_range = end_range, begin_range
    else:
        raise ValueError(
            "Size spec must be two numbers separated by a dash: e.g. 1-10")

    if force_jit:
        for p in {'cuda', 'cuda_1', 'cuda_2', 'cuda_3', 'dynamic_numba',
                  'dynamic_numba_2'} & {p.name for p in partitioner_list}:
            partitioners[p].partition([1, 2, 3], 2)

    r = benchmark(partitioner_list, item_list, bucket_list,
                  iterations, begin_range, end_range, specified_items_sizes,
                  verbose, include_items)

    if tables:
        echo_tables(partitioner_list, r)

    if report is not None:
        write_report(r, report)


def get_partitioners(partitioner_types):
    """Return a list of partitioners for the given types string.
    """
    partitioner_list = []
    for p in partitioner_types.split(','):
        if m := re.match(r'(?P<filename>.*):(?P<classname>.*)', p):
            loader = importlib.machinery.SourceFileLoader('mymodule',
                                                          m.group('filename'))
            spec = importlib.util.spec_from_loader('mymodule', loader)
            mymodule = importlib.util.module_from_spec(spec)
            loader.exec_module(mymodule)
            partitioner_list.append(getattr(mymodule, (m.group('classname'))))
        else:
            partitioner_list.append(partitioners[p])
    return partitioner_list


if __name__ == '__main__':
    cli(sys.argv[1:])
