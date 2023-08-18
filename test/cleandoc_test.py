# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from os import path, system, chdir, getcwd
import sys
from importlib import import_module

scriptdir, scriptname = path.split(__file__)
testdir = path.split(path.abspath(__file__))[0]
mainpath = path.split(testdir)[0]
cleandoc_path = path.join(mainpath, "src", "cleandoc")
try:
    import cleandoc as cd
except ImportError:
    sys.path.insert(0, path.join(mainpath, "src"))
    cd = import_module("cleandoc")

clitest = (
    "C:/ProgramData/Anaconda3/Scripts/activate.bat && conda activate "
    + f"py39 && cd %userprofile% && cleandoc -f {__file__} -w"
)
print(f"\nCommand Line Test Command:\n{clitest}\n")
out = system(clitest)
print(f"\nCommand Line Test Exit Code: {out}\n")
cd.cleandoc_all(cleandoc_path, write=False)

# Clean my other packages
currentdir = getcwd()
chdir("./test")
SNIPSEARCH = path.join(scriptdir, "../../snipsearch/src/snipsearch")
cd.cleandoc_all(SNIPSEARCH, write=False)
TEST = path.join(scriptdir, "./test_pkgs/fake_pkg_1")
cd.cleandoc_all(TEST)
chdir(currentdir)
