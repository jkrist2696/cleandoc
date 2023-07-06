# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from os import path, mkdir, remove
from shutil import rmtree, copytree, copyfile
import logging
import webbrowser
from sys import stdout
from .clean import run_black, run_pylint, run_mypy
from .doq import run_doq
from .helper import format_header, find_pyfiles
from .sphinx import run_sphinx_all, get_release


def cleandoc_all(searchpath: str, ignore: bool = False):
    """cleandoc.

    Parameters
    ----------
    searchpath : str
        searchpath
    ignore : bool
        ignore
    """
    logpath = "cleandoc_log.txt"
    if path.exists(logpath):
        remove(logpath)
    logging.basicConfig(
        filename=logpath,
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
    logger = logging.getLogger("cleandoc")
    logger.addHandler(logging.StreamHandler(stdout))
    clean_all(searchpath, ignore=ignore)
    mainpage = gen_docs(searchpath)
    logging.shutdown()
    del logger
    webbrowser.open(mainpage)


def clean_all(searchpath: str, ignore: bool = False):
    """clean_all.

    Parameters
    ----------
    searchpath : str
        searchpath
    ignore : bool
        ignore
    """
    _none1, pyfilelist = find_pyfiles(searchpath)
    logger = logging.getLogger("cleandoc")
    for i, pyfile in enumerate(pyfilelist):
        _none2, pyname = path.split(pyfile)
        checkheader = f"Checking File ({i+1}/{len(pyfilelist)}): {pyname}"
        checkstr = f"{format_header(checkheader, repeat_char='o')}\n"
        logger.info(checkstr)
        summary = clean_pyfile(pyfile)
        if (not ignore) and (len(summary) > 0):
            raise SyntaxWarning(summary)
        if len(summary) == 0:
            logger.info("File is Clean: %s\n", pyfile)


def clean_pyfile(pyfilepath: str):
    """clean_pyfile.

    Parameters
    ----------
    pyfilepath : str
        pyfilepath
    """
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
    logger = logging.getLogger("cleandoc")
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
    logger.info("location: %s", docs)
    return indexpath


# if __name__ == "__main__":
#    scriptdir, scriptname = path.split(__file__)
#    cleandoc_all(scriptdir)
