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
from .doq import run_doq
from .helper import format_header, find_pyfiles, get_clean_pyfiles, config_log
from .sphinx import run_sphinx_all, get_release

reload(logging)


def cleandoc_all(searchpath: str, ignore: bool = False):
    """cleandoc.

    Parameters
    ----------
    searchpath : str
        searchpath
    ignore : bool
        ignore
    """
    skiplist = get_clean_pyfiles("cleandoc_log.txt")
    config_log("cleandoc_log.txt")
    clean_all(searchpath, ignore=ignore, skip=skiplist)
    mainpage = gen_docs(searchpath)
    webbrowser.open(mainpage)
    logging.shutdown()


def clean_all(
    searchpath: str, ignore: bool = False, skip: Union[bool, List[str]] = False
):
    """clean_all.

    Parameters
    ----------
    searchpath : str
        searchpath
    ignore : bool
        ignore
    """
    if skip is True:
        skip = get_clean_pyfiles("cleandoc_log.txt")
    elif skip is False:
        skip = []
    _none1, pyfilelist = find_pyfiles(searchpath)
    logger = config_log("cleandoc_log.txt")
    for i, pyfile in enumerate(pyfilelist):
        _none2, pyname = path.split(pyfile)
        if pyfile in skip:
            header = f"Skipping File ({i+1}/{len(pyfilelist)}): {pyname}"
            headerstr = f"{format_header(header, repeat_char='o')}\n"
            logger.info(headerstr)
            logger.info("File is Clean: %s\n", pyfile)
            continue
        header = f"Checking File ({i+1}/{len(pyfilelist)}): {pyname}"
        headerstr = f"{format_header(header, repeat_char='o')}\n"
        logger.info(headerstr)
        summary = clean_pyfile(pyfile)
        if (not ignore) and (len(summary) > 0):
            logger.error("%s\n", pyfile)
            logging.shutdown()
            raise SyntaxWarning(f"{pyfile}\n{summary}")
        if len(summary) == 0:
            logger.info("File is Clean: %s\n", pyfile)


def clean_pyfile(pyfilepath: str):
    """clean_pyfile.

    Parameters
    ----------
    pyfilepath : str
        pyfilepath
    """
    config_log("cleandoc_log.txt")
    realpath = path.realpath(pyfilepath)
    summary = run_doq(realpath)
    summary += run_black(realpath)
    summary += run_pylint(realpath)
    summary += run_mypy(realpath)
    return summary


def gen_docs(pkgpath: str):
    """gen_docs.

    Parameters
    ----------
    pkgpath : str
        pkgpath
    """
    logger = config_log("cleandoc_log.txt")
    logger.info("%s\n", format_header("Gen Docs Output", repeat_char="o"))
    logger.debug("    pkgpath: %s", pkgpath)
    basepath, pkgname = path.split(pkgpath)
    docpath = path.join(basepath, f"_{pkgname}_working_docs")
    confpath = path.join(docpath, "source", "conf.py")
    docs = path.join(basepath, "docs")
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
    indexpath = path.join(docs, "index.html")
    logger.info("Location: %s\n", docs)
    return indexpath


# if __name__ == "__main__":
#    scriptdir, scriptname = path.split(__file__)
#    cleandoc_all(scriptdir)
