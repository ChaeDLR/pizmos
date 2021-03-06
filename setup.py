#! /usr/bin/env python3

"""
Author:
    Chae De La Rosa
Github:
    https://github.com/ChaeDLR
"""
import pizmos

from sphinx.setup_command import BuildDoc
from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as rm:
    readme = rm.read()

setup(
    name=pizmos.__title__,
    version=pizmos.__version__,
    description=pizmos.__description__,
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: Lesser General Public License ",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    author=pizmos.__author__,
    url=pizmos.__url__,
    author_email=pizmos.__email__,
    license=pizmos.__license__,
    include_package_data=True,
    package_data={},
    install_requires=list(open("requirements.txt", "r").readlines()),
    zip_safe=True,
    packages=find_packages(),
    cmdclass={"build_sphinx": BuildDoc},
    command_options={
        "build_sphinx": {
            "project": ("setup.py", pizmos.__title__),
            "version": ("setup.py", pizmos.__version__),
            "release": ("setup.py", pizmos.__release__),
            "source_dir": ("setup.py", "docs/source"),
        }
    },
)
