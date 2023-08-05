"""Conversion functions for sqlite3.Row"""

from typing import Union, Generator

DictOrTuple = Union[dict, tuple]
DictGenerator = Generator[dict, None, None]
TupleGenerator = Generator[tuple, None, None]
DictOrTupleGenerator = Union[DictGenerator, TupleGenerator]


def convert_sqliterow(row, as_dict) -> DictOrTuple:
    """Call dict/tuple converter on sqlite3.Row"""
    return sqliterow_to_dict(row) if as_dict else sqliterow_to_tuple(row)


def sqliterow_to_dict(row) -> dict:
    """Convert sqlite3.Row instance to dict"""
    return dict(zip(row.keys(), tuple(row)))


def sqliterow_to_tuple(row) -> tuple:
    """Convert sqlite3.Row instance to tuple"""
    return tuple(row)


def convert_sqliterows(rows, as_dict) -> DictOrTupleGenerator:
    """Call dict/tuple converter on several sqlite3.Row"""
    return sqliterows_to_dicts(rows) if as_dict else sqliterows_to_tuples(rows)


def sqliterows_to_dicts(rows) -> Generator[dict, None, None]:
    """Convert sqlite3.Row instances to dicts"""
    for row in rows:
        yield sqliterow_to_dict(row)


def sqliterows_to_tuples(rows) -> Generator[tuple, None, None]:
    """Convert sqlite3.Row instances to tuples"""
    for row in rows:
        yield sqliterow_to_tuple(row)
