#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013, Rui Carmo
Description: Experimental Cython compile script
License: MIT (see LICENSE.md for details)
"""

import os
import sys
import warnings

try:
    from distribute_setup import use_setuptools
    use_setuptools()
except:
    warnings.warn(
        "Failed to import distribute_setup, continuing without distribute.",
        Warning)

from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext as distutils_build_ext
from setuptools.extension import Extension

setup_args = {}

if 'sdist' in sys.argv or 'develop' in sys.argv:
    try:
        from Cython.Distutils import build_ext

    except:
        print "You don't seem to have Cython installed"
        build_ext = distutils_build_ext

    setup_args['cmdclass'] = {'build_ext': build_ext}


def scandir(dir, files=[]):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if os.path.isfile(path) and path.endswith(".py"):
            files.append(path.replace(os.path.sep, ".")[:-3])
        elif os.path.isdir(path):
            scandir(path, files)
    return files


def makeExtension(extName):
    extPath = extName.replace(".", os.path.sep) + ".py"
    return Extension(
        extName,
        [extPath],
        include_dirs=["."],
        extra_compile_args=["-O3", "-Wall"],
        extra_link_args=['-g'],
        libraries=[],
    )

extensions = [makeExtension(name) for name in scandir("strainer")]

setup(
    name="strainer",
    packages=find_packages(),
    ext_modules=extensions,
    setup_requires=['Cython', ],
    install_requires=['Cython', 'beautifulsoup4',
                      'html5lib', 'lxml', 'requests'],
    **setup_args
)
