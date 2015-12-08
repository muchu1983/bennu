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
    name = "united",
    version = "0.3.0.dev31",
    keywords = ["united", "image", "wiki"],
    description = "Image wiki system",
    author = "MuChu Hsu",
    author_email = "muchu1983@gmail.com",
    license = "BSD 3-Clause License",
    url="https://github.com/muchu1983/united",
    long_description=long_description,
    packages = find_packages(),
    include_package_data = True,
    install_requires = ["Pillow>=3.0.0"],
    platforms = "python 3.3",
    entry_points={"console_scripts":["united=united.launcher:entry_point"]},
    classifiers=[
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
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia :: Graphics :: Viewers",
        ],
)




