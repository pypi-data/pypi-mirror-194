# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     setup
   Author :        sss
   date：          2023-2-24
-------------------------------------------------
   Change Activity:
                   2023-2-24:
-------------------------------------------------
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlite_tool", # Replace with your own username
    version="0.0.2",
    author="sss758",
    author_email="author@example.com",
    description="A simple sqlite package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
