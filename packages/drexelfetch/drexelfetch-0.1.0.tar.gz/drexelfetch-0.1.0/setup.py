# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drexelfetch']

package_data = \
{'': ['*']}

install_requires = \
['kolorz>=0.2.5,<0.3.0', 'polars>=0.16.8,<0.17.0', 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['dfetch = drexelfetch.cli:main']}

setup_kwargs = {
    'name': 'drexelfetch',
    'version': '0.1.0',
    'description': 'A fetch tool for drexel courses',
    'long_description': '<h2 align="center"> ━━━━━━  ❖  ━━━━━━ </h2>\n\n---\n\n### ❖ Information \n  \n  DrexelFetch is an incredibly simple tool to fetch information about Drexel Courses. \n\n  *NOTE* that the data is sourced directly from the `courses.csv` file in the top level repo, and might be outdated in the future. The data was scraped and sanitized by [@Shahriyar](https://github.com/ShahriyarShawon), I just wrote a silly little python script on top to display it. \n\n  The tool was originally meant for personal use only and doesn\'t follow any "good" code practices. I make no guarantees about the correctness, error checking or the aesthetics of the code.\n\n  We ball regardless.\n  \n---\n\n### ❖ Requirements\n\n- A python Install\n- That\'s it\n- Okay maybe you\'ll need some ability to use the terminal\n- That\'s really it\n- Nano users not welcome\n\n---\n\n### ❖ Installation\n\n> Install from pip\n```sh\npip3 install drexelfetch\n```\n\n> Install from source\n- First, install [poetry](https://python-poetry.org/)\n```sh\ngit clone https://github.com/dotzenith/DrexelFetch.git\ncd DrexeFetch\npoetry build\npip3 install ./dist/drexelfetch-0.1.0.tar.gz\n```\n\n### ❖ Usage \n\n```\nUsage: dfetch [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  info    Get information about a given course\n  prereq  Find what other courses this given course is a prereq for\n```\n\nGet info about a given course\n```sh\ndfetch info "CS 260"\n```\n\nGet all the courses a given course is a prereq for\n```sh\ndfetch prereq "MATH 201"\n```\n---\n\n### ❖ What\'s New? \n0.1.0 - Initial public release\n\n---\n\n<div align="center">\n\n   <img src="https://img.shields.io/static/v1.svg?label=License&message=MIT&color=F5E0DC&labelColor=302D41&style=for-the-badge">\n\n</div>\n',
    'author': 'dotzenith',
    'author_email': 'contact@danshu.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
