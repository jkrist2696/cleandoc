# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as readme:
    readme_text = readme.read()

setup(
    name="cleandoc",
    version="0.0.1",
    description=(
        "Python package leveraging doq, black, pylint, mypy and sphinx"
        + " to automatically clean and document python code."
    ),
    long_description=readme_text,
    long_description_content_type="text/markdown",
    author="Jason Krist",
    author_email="jkrist2696@gmail.com",
    url="https://github.com/jkrist2696/cleandoc",
    license="GNU GPLv3",
    packages=find_packages(where="src"),
    install_requires=[
        "black>=23.3.0",
        "mypy>=1.4.1",
        "pylint>=2.17.4",
        "Sphinx>=6.2.1",
        "sphinx_rtd_theme>=1.2.2",
        "doq>=0.9.1",
    ],
    package_dir={"cleandoc": "src/cleandoc"},
    entry_points={"console_scripts": ["cleandoc=cleandoc.cli:main"]},
    python_requires=">=3.9",
)
