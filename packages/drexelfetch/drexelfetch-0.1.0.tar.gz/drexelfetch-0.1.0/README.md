<h2 align="center"> ━━━━━━  ❖  ━━━━━━ </h2>

---

### ❖ Information 
  
  DrexelFetch is an incredibly simple tool to fetch information about Drexel Courses. 

  *NOTE* that the data is sourced directly from the `courses.csv` file in the top level repo, and might be outdated in the future. The data was scraped and sanitized by [@Shahriyar](https://github.com/ShahriyarShawon), I just wrote a silly little python script on top to display it. 

  The tool was originally meant for personal use only and doesn't follow any "good" code practices. I make no guarantees about the correctness, error checking or the aesthetics of the code.

  We ball regardless.
  
---

### ❖ Requirements

- A python Install
- That's it
- Okay maybe you'll need some ability to use the terminal
- That's really it
- Nano users not welcome

---

### ❖ Installation

> Install from pip
```sh
pip3 install drexelfetch
```

> Install from source
- First, install [poetry](https://python-poetry.org/)
```sh
git clone https://github.com/dotzenith/DrexelFetch.git
cd DrexeFetch
poetry build
pip3 install ./dist/drexelfetch-0.1.0.tar.gz
```

### ❖ Usage 

```
Usage: dfetch [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  info    Get information about a given course
  prereq  Find what other courses this given course is a prereq for
```

Get info about a given course
```sh
dfetch info "CS 260"
```

Get all the courses a given course is a prereq for
```sh
dfetch prereq "MATH 201"
```
---

### ❖ What's New? 
0.1.0 - Initial public release

---

<div align="center">

   <img src="https://img.shields.io/static/v1.svg?label=License&message=MIT&color=F5E0DC&labelColor=302D41&style=for-the-badge">

</div>
