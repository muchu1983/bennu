"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from setuptools import setup,find_packages

setup(
    name = "united",
    version = "0.3.0.dev9",
    keywords = ("united"),
    description = "Image wiki system",
    author = "MuChu Hsu",
    author_email = "muchu1983@gmail.com",
    license = "BSD-3-Clause License",
    url="https://github.com/muchu1983/united",
    scripts=["united.py"],
    packages = find_packages(),
    include_package_data = True,
    install_requires = ["Pillow>=3.0.0"],
    platforms = "python 3.3",
)

