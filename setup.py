"""
Author:
    Chae De La Rosa
Github:
    https://github.com/ChaeDLR
"""
import PreceptPen

from setuptools import setup, find_packages

with open("README.md", 'r', encoding="utf-8") as rm:
    readme = rm.read()

setup(
    name=PreceptPen.__title__,
    version=PreceptPen.__version__,
    description=PreceptPen.__description__,
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: Lesser General Public License ",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent"
    ],
    author=PreceptPen.__author__,
    url=PreceptPen.__url__,
    author_email=PreceptPen.__email__,
    license=PreceptPen.__license__,
    include_package_data=True,
    package_data={},
    install_requires=list(open("requirements.txt", 'r').readlines()),
    zip_safe=True,
    packages=find_packages()
)
