# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from os import path
import sys
sys.path.insert(0,path.abspath("../"))
from cleandoc import cleandoc_all

scriptdir, scriptname = path.split(__file__)
cleandoc_path = path.join(path.abspath("../"), "cleandoc")
cleandoc_all(cleandoc_path)
