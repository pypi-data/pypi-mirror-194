#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   setup.py
@Author  :   Raighne.Weng
@Version :   0.7.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Setup module
'''

import setuptools

# read the contents of your README file
with open("readme.md", "r", encoding="utf8") as rd:
    long_description = rd.read()

setuptools.setup(
    name="datature",
    version="0.7.0",
    author="Raighne Weng",
    author_email="raighne@datature.io",
    long_description_content_type="text/markdown",
    long_description=long_description,
    description="Python bindings for the Datature API",
    packages=setuptools.find_namespace_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests", "google-crc32c", "pyhumps", "pyyaml", "inquirer", "tqdm",
        "halo", "filetype", "opencv-python"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License"
    ],
    entry_points={
        'console_scripts': ['datature=datature.cli.main:main'],
    },
)
