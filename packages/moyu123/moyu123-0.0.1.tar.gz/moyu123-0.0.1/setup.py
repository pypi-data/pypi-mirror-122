# -*- coding: utf-8 -*-
# @Time    : 2020-9-16 15:56:22
# @Author  : master SU
# @Site    :
# @File    : setup.py
# @Software: PyCharm
# @Description:
#
#

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="moyu123",
    version="0.0.1",
    author="moyu123",
    description="python常用工具集",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

)
