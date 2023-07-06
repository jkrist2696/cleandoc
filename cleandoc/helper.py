# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from subprocess import run
from math import floor, ceil
from importlib.util import find_spec
from typing import Tuple
from os import path, walk


def check_for_pkg(packagename: str):
    """check_for_pkg.

    Parameters
    ----------
    packagename : str
        packagename
    """
    spec = find_spec(packagename)
    if spec is None:
        errorstr = (
            f"{packagename} is not installed! Please "
            f"install the package before rerunning the script."
        )
        raise ModuleNotFoundError(errorstr)


def run_capture_out(cmd: list[str], shell: bool = False) -> Tuple[str, str]:
    """run_capture_out.

    Parameters
    ----------
    cmd : list[str]
        cmd

    Returns
    -------
    Tuple[str, str]

    """
    proc = run(cmd, capture_output=True, encoding="utf-8", check=False, shell=shell)
    return proc.stdout, proc.stderr


def format_header(name: str, repeat_char: str = "-", linelen: int = 68) -> str:
    """format_header.

    Parameters
    ----------
    name : str
        name
    repeat_char : str
        repeat_char
    linelen : int
        linelen

    Returns
    -------
    str

    """
    start = repeat_char * floor((linelen - len(name) - 2) / 2)
    end = repeat_char * ceil((linelen - len(name) - 2) / 2)
    header = f"{start} {name} {end}"
    return header


def find_pyfiles(searchpath: str) -> Tuple[list[str], list[str]]:
    """find_pyfiles.

    Parameters
    ----------
    searchpath : str
        searchpath

    Returns
    -------
    Tuple[list[str], list[str]]

    """
    pathlist = []
    filelist = []
    for root, _none1, files in walk(searchpath):
        contains_py = False
        for filename in files:
            _none2, fileext = path.splitext(filename)
            if ".py" == fileext:
                contains_py = True
                filepath = path.join(root, filename)
                filelist.append(filepath)
        if contains_py:
            pathlist.append(root)
    return pathlist, filelist


# def read_log(logpath):
#    getmtime(pypath)
#    return goodfileslist

# if __name__ == "__main__":
