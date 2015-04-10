#!/usr/bin/python2
from distutils.core import setup

setup_args = dict(
    name="stadium",
    version="0.1",
    description="A tool for modifying the rental set of Pokemon Stadium 2 N64 ROMs",
    author="Chaise Conn",
    author_email="chaisecanz@gmail.com",
    url="https://github.com/Jdaco/stadium",
    platforms="Platform Independent",
    install_requires=[
        'urwid',
        'urwidgets>=0.2',
    ],
    packages=["stadium", "stadium.mappers"],
    scripts=["bin/stadium"],
)

setup(**setup_args)
