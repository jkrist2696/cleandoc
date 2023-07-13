# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from os import path
import sys
from importlib import import_module

# sys.path.insert(0, path.abspath("../"))
# from cleandoc import cleandoc_all  # noqa: E402 # pylint: disable=C0413
sys.path.insert(0, path.abspath("../"))
cd = import_module("cleandoc")

scriptdir, scriptname = path.split(__file__)
cleandoc_path = path.join(path.abspath("../"), "cleandoc")
# clean_all(cleandoc_path, ignore = True, skip=True)
# gen_docs(cleandoc_path)
# logging.shutdown()
cd.cleandoc_all(cleandoc_path)
