"""
The CLI interface for DrexelFetch
"""

import typer
from kolorz import make_kolorz

import drexelfetch.fetch as fetch

app = typer.Typer(add_completion=False)
colors = make_kolorz()

"""
course number,course name,credits,prereqs,desc
"""


@app.command()
def info(course: str = typer.Argument(..., help="The course name, ex. CS 164")):
    """
    Get information about a given course
    """
    course_info = fetch.info(course)
    if course_info is None:
        print("Course not found")
        return

    print(
        f"{colors.red}{'Course ID:' : <14}{colors.end} {course_info['course number']}"
    )
    print(
        f"{colors.blue}{'Course Name:' : <14}{colors.end} {course_info['course name']}"
    )
    print(f"{colors.orange}{'Credits:' : <14}{colors.end} {course_info['credits']}")
    print(
        f"{colors.green}{'Prerequisites:' : <14}{colors.end} {course_info['prereqs']}"
    )
    print(f"{colors.yellow}{'Description:' : <14}{colors.end} {course_info['desc']}")


@app.command()
def prereq(course: str = typer.Argument(..., help="The course name, ex. CS 164")):
    """
    Find what other courses this given course is a prereq for
    """
    prereqs = fetch.prereq(course)

    if prereqs is None:
        print("Course not found")
    elif len(prereqs) < 1:
        print("This course is not a prereq to any other course")
    else:
        for course in prereqs:
            print(course)


def main():
    app()
