"""
A singular helper for DrexelFetch
"""

import subprocess
from pathlib import Path

import polars as pl


def get_courses_df() -> pl.DataFrame:
    """
    Returns a polars DataFrame sourced from the courses.csv file
    """

    git_repo = (
        subprocess.Popen(
            ["git", "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE
        )
        .communicate()[0]
        .rstrip()
        .decode("utf-8")
    )

    courses_path = Path(f"{git_repo}/courses.csv")

    return pl.read_csv(courses_path, sep=",")
