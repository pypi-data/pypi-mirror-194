# mypy: ignore-errors
import re
from pathlib import Path

import setuptools

NAME = "aipo"
EXTENSIONS = {"uvloop", "redis"}

classes = """
    Development Status :: 2 - Pre-Alpha
    License :: OSI Approved :: BSD License
    Programming Language :: Python :: 3 :: Only
    Programming Language :: Python :: 3.10
    Programming Language :: Python :: 3.11
    Programming Language :: Python :: Implementation :: CPython
    Operating System :: POSIX
    Operating System :: Unix
    Environment :: No Input/Output (Daemon)
    Framework :: AsyncIO
    Intended Audience :: Developers
"""
classifiers = [s.strip() for s in classes.split("\n") if s]

re_meta = re.compile(r"__(\w+?)__\s*=\s*(.*)")
re_doc = re.compile(r'^"""(.+?)"""')


def add_default(m):
    attr_name, attr_value = m.groups()
    return ((attr_name, attr_value.strip("\"'")),)


def add_doc(m):
    return (("doc", m.groups()[0]),)


pats = {re_meta: add_default, re_doc: add_doc}

here = Path(__file__).parent.absolute()
with open(here / NAME / "__init__.py") as meta_fh:
    meta = {}
    for line in meta_fh:
        if line.strip() == "# -eof meta-":
            break
        for pattern, handler in pats.items():
            m = pattern.match(line.strip())
            if m:
                meta.update(handler(m))


def strip_comments(line):
    return line.split("#", 1)[0].strip()


def _pip_requirement(req):
    if req.startswith("-r "):
        _, path = req.split()
        return reqs(*path.split("/"))
    return [req]


def _reqs(*f):
    path = (Path.cwd() / "requirements").joinpath(*f)
    reqs = (strip_comments(line) for line in path.open().readlines())
    return [_pip_requirement(r) for r in reqs if r]


def reqs(*f):
    return [req for subreq in _reqs(*f) for req in subreq]


def extras(*p):
    return reqs("extras", *p)


def extras_require():
    return {x: extras(x + ".txt") for x in EXTENSIONS}


with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=NAME,
    version=meta["version"],
    description=meta["doc"],
    author=meta["author"],
    author_email=meta["contact"],
    url=meta["homepage"],
    platforms=["any"],
    license="BSD",
    keywords=meta["keywords"],
    packages=setuptools.find_packages(exclude=["t", "t/*", "docs"]),
    include_package_data=True,
    install_requires=reqs("default.txt"),
    tests_require=reqs("test.txt"),
    extras_require=extras_require(),
    python_requires=">=3.8",
    classifiers=classifiers,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    entry_points={
        "console_scripts": [
            "celery = aipo.__main__:main",
        ]
    },
)
