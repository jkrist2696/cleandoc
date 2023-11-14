# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from os import path
import sys

testdir = path.dirname(path.abspath(__file__))
mainpath = path.dirname(testdir)
appendpath = path.join(testdir, "../../pyprojectlib/src")
sys.path.insert(0, appendpath)

from pyprojectlib import package_project
from pyprojectlib.pyuser import User

from cleandoc import cleandoc_all

pkgname = path.basename(mainpath)
srcpath = path.join(mainpath, "src", pkgname)
cleandoc_all(srcpath)
# import pytest
# pytest.main()

package = package_project(mainpath, User(), upload=True, install=True)
