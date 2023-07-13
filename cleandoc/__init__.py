# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from os import path, mkdir
from shutil import rmtree, copytree, copyfile
import logging
from importlib import reload
import webbrowser
from typing import Union, List
from .clean import run_black, run_pylint, run_mypy
from .doq import run_doq, check_docstrings
from .helper import format_header, find_pyfiles, get_clean_pyfiles, config_log
from .helper import check_modified_since_docs
from .sphinx import run_sphinx_all, get_release

reload(logging)


def cleandoc_all(
    searchpath: str, ignore: bool = False, write: bool = True, openhtml: bool = True
):
    """Run clean_all and gen_docs functions. Check modified files since last
    document generation to skip checking of some files. Open docs in browser
    after creation or checking.

    Parameters
    ----------
    searchpath : str
        directory of python package (nested dirs of modules)
    ignore : bool
        keyword argument passed to clean_all function
    """
    searchpath = path.abspath(searchpath)
    skiplist = get_clean_pyfiles("cleandoc_log.txt")
    createdocs = check_modified_since_docs(searchpath, "cleandoc_log.txt")
    config_log("cleandoc_log.txt")
    clean_all(searchpath, ignore=ignore, write=write, skip=skiplist)
    mainpage = gen_docs(searchpath, create=createdocs)
    if openhtml is True:
        webbrowser.open(mainpage)
    logging.shutdown()


def clean_all(
    searchpath: str,
    ignore: bool = False,
    write: bool = True,
    skip: Union[bool, List[str]] = False,
):
    """Run clean_pyfile function on all .py files in searchpath.

    Parameters
    ----------
    searchpath : str
        Directory to search in all nested folders for .py files
    ignore : bool
        True to ignore Syntax warnings found, False to raise them
    write : bool
        keyword argument passed to clean_pyfile function
    skip : Union[bool, List[str]]
        List of .py files to skip cleaning.
        Or True to find list of clean pyfiles within function.
    """
    searchpath = path.abspath(searchpath)
    if skip is True:
        skip = get_clean_pyfiles("cleandoc_log.txt")
    elif skip is False:
        skip = []
    _none1, pyfilelist = find_pyfiles(searchpath)
    logger = config_log("cleandoc_log.txt")
    for i, pyfile in enumerate(pyfilelist):
        _none2, pyname = path.split(pyfile)
        if pyfile in skip:  # type: ignore
            header = f"Skipping File ({i+1}/{len(pyfilelist)}): {pyname}"
            headerstr = f"{format_header(header, repeat_char='o')}\n"
            logger.info(headerstr)
            logger.info("File is Clean: %s\n", pyfile)
            continue
        header = f"Checking File ({i+1}/{len(pyfilelist)}): {pyname}"
        headerstr = f"{format_header(header, repeat_char='o')}\n"
        logger.info(headerstr)
        summary = clean_pyfile(pyfile, write=write)
        if (not ignore) and (len(summary) > 0):
            logger.error("%s\n", pyfile)
            logging.shutdown()
            raise SyntaxWarning(f"{pyfile}\n{summary}")
        if len(summary) == 0:
            logger.info("File is Clean: %s\n", pyfile)


def clean_pyfile(pyfilepath: str, write: bool = True):
    """Clean a .py file by checking docstrings then running doq, black,
    pylint, and mypy.

    Parameters
    ----------
    pyfilepath : str
        Full path of python (.py) file
    Returns
    -------
    str
        Summary of all command outputs concatenated together
    """
    config_log("cleandoc_log.txt")
    pyfilepath = path.abspath(pyfilepath)
    realpath = path.realpath(pyfilepath)
    summary = check_docstrings(realpath)
    summary += run_doq(realpath, write=write)
    summary += run_black(realpath, write=write)
    summary += run_pylint(realpath)
    summary += run_mypy(realpath)
    return summary


def gen_docs(pkgpath: str, create: bool = True):
    """Auto-generate sphinx html documentation for a python package.

    Parameters
    ----------
    pkgpath : str
        Full path to directory containing all python modules to document.
        Directory name will be used as package name.
    create : bool
        True to create docs or False to skip and log their location
    Returns
    -------
    str
        Path of index.html file, the home page of the sphinx docs
    """
    pkgpath = path.abspath(pkgpath)
    logger = config_log("cleandoc_log.txt")
    basepath, pkgname = path.split(pkgpath)
    docs = path.join(basepath, "docs")
    indexpath = path.join(docs, "index.html")
    if create is False:
        logger.info("%s\n", format_header("Skipping Gen Docs", repeat_char="o"))
        logger.info("Docs Location: %s\n", docs)
        return indexpath
    logger.info("%s\n", format_header("Gen Docs Output", repeat_char="o"))
    logger.debug("    pkgpath: %s", pkgpath)
    docpath = path.join(basepath, f"_{pkgname}_working_docs")
    confpath = path.join(docpath, "source", "conf.py")
    confpath_old = path.join(docs, "conf.txt")
    release = get_release(confpath_old)
    if path.exists(docpath):
        rmtree(docpath)
    mkdir(docpath)
    run_sphinx_all(docpath, confpath, pkgpath, release)
    htmlpath = path.join(docpath, "build", "html")
    if path.exists(docs):
        rmtree(docs)
    copytree(htmlpath, docs)
    copyfile(confpath, confpath_old)
    rmtree(docpath)
    logger.info("Docs Location: %s\n", docs)
    return indexpath


# if __name__ == "__main__":
#    scriptdir, scriptname = path.split(__file__)
#    cleandoc_all(scriptdir)
