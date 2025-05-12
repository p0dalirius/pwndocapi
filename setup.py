#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : setup.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022

import setuptools

long_description = "A Python native library to automate reporting vulnerabilities into pwndoc."

setuptools.setup(
    name="pwndocapi",
    version="1.3.4",
    description="Python API client for PwnDoc",
    url="https://github.com/p0dalirius/pwndocapi",
    author="Podalirius",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="podalirius@protonmail.com",
    packages=setuptools.find_packages(),
    license="GPL2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.4",
)
