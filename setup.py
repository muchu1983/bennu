"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from setuptools import setup, find_packages

setup(
    name = "united",
    version = "0.3.0",
    keywords = ("united"),
    description = "Image wiki system",
    license = "BSD-3-Clause License",
    install_requires = ["Pillow>=3.0.0"],
    author = "MuChu Hsu",
    author_email = "muchu1983@gmail.com",
    packages = find_packages(),
    platforms = "any",
)