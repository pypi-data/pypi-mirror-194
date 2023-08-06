"""
A singular helper for DrexelFetch
"""

from importlib import resources

import polars as pl


def get_courses_df() -> pl.DataFrame:
    """
    Returns a polars DataFrame sourced from the courses.csv file
    """

    with resources.as_file(
        resources.files(__package__).joinpath("courses.csv")
    ) as path:
        return pl.read_csv(path, sep=",")
