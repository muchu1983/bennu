# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from setuptools import setup,find_packages

with open("README.txt") as file:
    long_description = file.read()

setup(
    name = "bennu",
    version = "0.4.1a10",
    author = "MuChu Hsu",
    author_email = "muchu1983@gmail.com",
    maintainer = "MuChu Hsu",
    maintainer_email = "muchu1983@gmail.com",
    url="https://github.com/muchu1983/bennu",
    description = "muchu's utility module",
    long_description=long_description,
    download_url="https://pypi.python.org/pypi/bennu",
    platforms = "python 3.4",
    license = "BSD 3-Clause License",
    packages = find_packages(),
    include_package_data = True,
    install_requires = ["Pillow>=3.0.0", "Flask>=0.10.1", "pymongo>=3.2.2", "selenium>=2.53.2"],
    entry_points = {"console_scripts":["bennu=bennu.launcher:entry_point"]},
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: Chinese (Traditional)",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP",
        ],
)




