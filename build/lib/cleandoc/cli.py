# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
from os import path
import sys
from importlib import import_module
cleandocdir, _none = path.split(path.abspath(__file__))
sys.path.insert(0, path.split(cleandocdir)[0])
cd = import_module("cleandoc")
"""

from argparse import ArgumentParser
import cleandoc as cd


def cli_checks(pypath: str, dirpath: str, noclean: bool, nodoc: bool):
    """Check that command line args are compatible

    Parameters
    ----------
    pypath : str
    dirpath : str
    noclean : bool
    nodoc : bool
    """
    if len(pypath) > 0 and len(dirpath) > 0:
        raise SyntaxError("File and Directory were both specified. Only specify one.")
    if len(pypath) == 0 and len(dirpath) == 0:
        raise SyntaxError(
            "Neither File or Directory were specified. Please specify one."
        )
    if len(pypath) > 0 and noclean:
        raise SyntaxError("File was specified with -noclean so nothing occured.")
    if noclean and nodoc:
        raise SyntaxError(
            "-noclean and -nodoc options were specified so nothing occured"
        )


def cli_file(pypath: str, write: bool):
    """Run clean_pyfile

    Parameters
    ----------
    pypath : str
        _description_
    write : bool
        _description_
    ignore : bool
        _description_
    """
    if len(pypath) > 0:
        cd.clean_pyfile(pypath, write=write)


def cli_dir(dirpath: str, write: bool, ignore: bool, noclean: bool, nodoc: bool):
    """Run clean_all, gen_docs, or cleandoc_all depending on args.

    Parameters
    ----------
    dirpath : str
    ignore : bool
    write : bool
    noclean : bool
    nodoc : bool
    """
    if len(dirpath) > 0 and nodoc:
        cd.clean_all(dirpath, write=write, ignore=ignore)
    if len(dirpath) > 0 and noclean:
        cd.gen_docs(dirpath)
    if len(dirpath) > 0:
        cd.cleandoc_all(dirpath, write=write, ignore=ignore)


def main():
    """Run full command line process"""
    desc = "Run automated cleaning and/or documentation of python code"
    fileh = "Python (.py) file to clean"
    dirh = "Directory containing Python (.py) files to clean and/or document"
    writeh = "Flag to write changes to files in-place"
    ignoreh = "Flag to continue through warnings"
    nch = "Flag to prevent cleaning of py files"
    ndh = "Flag to prevent html doc creation"

    parser = ArgumentParser(prog="cleandoc", description=desc)
    parser.add_argument("-file", "-f", default="", help=fileh)
    parser.add_argument("-dir", "-d", default="", help=dirh)
    parser.add_argument("-write", "-w", action="store_true", help=writeh)
    parser.add_argument("-ignore", "-i", action="store_true", help=ignoreh)
    parser.add_argument("-noclean", "-nc", action="store_true", help=nch)
    parser.add_argument("-nodoc", "-nd", action="store_true", help=ndh)

    args = vars(parser.parse_args())
    print(f"\nCommand Line Args:\n{args}\n")
    pypath, dirpath, write, ignore, noclean, nodoc = [args[key] for key in args.keys()]

    cli_checks(pypath, dirpath, noclean, nodoc)
    cli_file(pypath, write)
    cli_dir(dirpath, write, ignore, noclean, nodoc)


if __name__ == "__main__":
    main()
