#!/usr/bin/env python
"""Navigator-Session.

    Asynchronous library for managing user-specific data into a session object, used by Navigator.
See:
https://github.com/phenobarbital/navigator-session
"""
import ast
from os import path
from setuptools import find_packages, setup


def get_path(filename):
    return path.join(path.dirname(path.abspath(__file__)), filename)


def readme():
    with open(get_path('README.md'), 'r', encoding='utf-8') as rd:
        return rd.read()


version = get_path('navigator_session/version.py')
with open(version, 'r', encoding='utf-8') as meta:
    # exec(meta.read())
    t = compile(meta.read(), version, 'exec', ast.PyCF_ONLY_AST)
    for node in (n for n in t.body if isinstance(n, ast.Assign)):
        if len(node.targets) == 1:
            name = node.targets[0]
            if isinstance(name, ast.Name) and \
                    name.id in (
                        '__version__',
                        '__title__',
                        '__description__',
                        '__author__',
                        '__license__', '__author_email__'):
                v = node.value
                if name.id == '__version__':
                    __version__ = v.s
                if name.id == '__title__':
                    __title__ = v.s
                if name.id == '__description__':
                    __description__ = v.s
                if name.id == '__license__':
                    __license__ = v.s
                if name.id == '__author__':
                    __author__ = v.s
                if name.id == '__author_email__':
                    __author_email__ = v.s


setup(
    name="navigator-session",
    version=__version__,
    python_requires=">=3.8.0",
    url="https://github.com/phenobarbital/navigator-session",
    description=__description__,
    keywords=['asyncio', 'session', 'aioredis', 'aiohttp'],
    platforms=['POSIX'],
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Environment :: Web Environment",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database :: Front-Ends",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: AsyncIO",
        "Framework :: aiohttp",
    ],
    author=__author__,
    author_email=__author_email__,
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    license=__license__,
    setup_requires=[
        "asyncio==3.4.3",
        "cchardet==2.1.7",
    ],
    install_requires=[
        "PyNaCl==1.5.0",
        "aiohttp==3.8.3",
        "uvloop==0.17.0",
        "asyncio==3.4.3",
        "navconfig[default]>=1.0.15",
        "jsonpickle==3.0.1",
        "aioredis==2.0.1",
        "pendulum==2.1.2",
        "python_datamodel>=0.1.18"
    ],
    tests_require=[
        'pytest>=6.0.0',
        'pytest-asyncio==0.20.2',
        'pytest-xdist==2.5.0',
        'pytest-assume==2.4.3'
    ],
    test_suite='tests',
    project_urls={  # Optional
        "Source": "https://github.com/phenobarbital/navigator-session",
        "Funding": "https://paypal.me/phenobarbital",
        "Say Thanks!": "https://saythanks.io/to/phenobarbital",
    },
)
