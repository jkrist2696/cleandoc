# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from subprocess import run
from math import floor, ceil
from importlib.util import find_spec
from typing import Tuple
from os import path, walk, remove
from datetime import datetime
from re import findall
import logging
from sys import stdout


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


def check_modified(filepath: str, timestr: str) -> bool:
    """check_modified.

    Parameters
    ----------
    filepath : str
        filepath
    timestr : str
        timestr

    Returns
    -------
    bool

    """
    checktime = datetime.strptime(timestr, "%d-%m-%y %H:%M:%S")
    checkstamp = datetime.timestamp(checktime)
    editstamp = path.getmtime(filepath)
    return editstamp > checkstamp


def check_modified_since_docs(searchpath: str, logpath: str) -> bool:
    """check_modified_since_docs.

    Parameters
    ----------
    logpath : str
        logpath
    htmlpath : str
        htmlpath

    Returns
    -------
    bool

    """
    _none, filelist = find_pyfiles(searchpath)
    regex_docs = r"(\d\d-\d\d-\d\d \d\d:\d\d:\d\d).*Docs Location: (.*)"
    results_docs = findall_infile(regex_docs, logpath)
    print(results_docs)
    if len(results_docs) == 0:
        return True
    doctime = results_docs[0][0]
    for filepath in filelist:
        if check_modified(filepath, doctime):
            return True
    return False


def findall_infile(regex: str, filepath: str) -> list:
    """findall_infile.

    Parameters
    ----------
    regex : str
        regex
    filepath : str
        filepath

    Returns
    -------
    list

    """
    with open(filepath, "r", encoding="ascii") as file:
        filelines = file.readlines()
    filetext = "".join(filelines)
    results = findall(regex, filetext)
    return results


def get_clean_pyfiles(logpath: str) -> list[str]:
    """get_clean_pyfiles.

    Parameters
    ----------
    logpath : str
        logpath

    Returns
    -------
    list[str]

    """
    clean_pyfiles = []
    regex = r"(\d\d-\d\d-\d\d \d\d:\d\d:\d\d).*File is Clean: (.*)"
    results = findall_infile(regex, logpath)
    for result in results:
        if not check_modified(result[1], result[0]):
            clean_pyfiles.append(result[1])
    return clean_pyfiles


def config_log(logpath: str, logname: str = "cleandoc"):
    """config_log.

    Parameters
    ----------
    logpath : str
        logpath
    logname : str
        logname

    Returns
    -------
    Tuple[Any,bool]

    """
    if logging.getLogger(logname).hasHandlers():
        return logging.getLogger(logname)
    if path.exists(logpath):
        remove(logpath)
    logging.basicConfig(
        filename=logpath,
        filemode="a",
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%d-%m-%y %H:%M:%S",
        level=logging.INFO,
    )
    logger = logging.getLogger(logname)
    logger.addHandler(logging.StreamHandler(stdout))
    return logger


# if __name__ == "__main__":
