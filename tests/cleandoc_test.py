# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from os import path, system
import sys
from importlib import import_module

scriptdir, scriptname = path.split(__file__)
testdir, _none = path.split(path.abspath(__file__))
mainpath, _none = path.split(testdir)
cdpath = path.join(mainpath, "cleandoc")
sys.path.insert(0, mainpath)
cd = import_module("cleandoc")

clipath = path.join(cdpath, "cli.py")
clitest = f"python {clipath} -f {__file__} -w"
print(f"\nCommand Line Test Command:\n{clitest}\n")
out = system(clitest)
print(f"\nCommand Line Test Return Code: {out}\n")
cd.cleandoc_all(cdpath)
