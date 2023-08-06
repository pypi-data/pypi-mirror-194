"""
The main logic script for DrexelFetch
"""

from typing import Optional

import polars as pl

from drexelfetch.helpers import get_courses_df

classes = get_courses_df()
course_ids = set(classes.get_column("course number"))


def info(course: str) -> Optional[dict]:
    """
    Returns dict with info about a given course

    :param course - The name of a given course, ex. CS 164
    """

    if course not in course_ids:
        return None

    course_info = classes.filter(pl.col("course number") == course).to_dict(
        as_series=False
    )
    return {key: value[0] for key, value in course_info.items()}


def prereq(course: str) -> Optional[list]:
    """
    Returns a list of courses where the param "course" is a prereq

    :param course - The name of a given course, ex. CS 164
    """

    if course not in course_ids:
        return None

    course_preqs = classes.filter(pl.col("prereqs").str.contains(course))
    return list(course_preqs.get_column("course number"))
