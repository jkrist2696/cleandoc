# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from os import getlogin, path, sep, remove
from re import findall, sub
import logging
from .helper import check_for_pkg, find_pyfiles, run_capture_out, format_header

for pkg in ["sphinx", "sphinx_rtd_theme"]:
    check_for_pkg(pkg)


def run_sphinx_all(docpath: str, confpath: str, pkgpath: str, release: str):
    """run_sphinx_all.

    Parameters
    ----------
    docpath : str
        docpath
    confpath : str
        confpath
    pkgpath : str
        pkgpath
    release : str
        release
    """

    basepath, pkgname = path.split(pkgpath)
    summary = run_quickstart(docpath, pkgname, release)
    srcpath = path.join(docpath, "source")
    pathlist, _none2 = find_pyfiles(pkgpath)
    logger = logging.getLogger("cleandoc")
    logger.debug("    pathlist: %s", pathlist)
    for pypath in pathlist:
        initpath = path.join(pypath, "__init__.py")
        if not path.exists(initpath):
            with open(initpath, "w", encoding="ascii") as initfile:
                initfile.write("")
    summary += run_apidoc(srcpath, [pkgpath])
    edit_conf(confpath, [basepath, pkgpath] + pathlist)
    edit_index(srcpath, pkgname)
    summary += run_make(docpath)
    if len(summary) > 0:
        raise SyntaxError(summary)


def run_quickstart(docpath: str, pkgname: str, release: str) -> str:
    """run_quickstart.

    Parameters
    ----------
    docpath : str
        docpath
    pkgname : str
        pkgname
    release : str
        release
    """
    qs_args = [
        "sphinx-quickstart",
        docpath,
        "--sep",
        "-p",
        pkgname,
        "-a",
        getlogin(),
        "-r",
        release,
        "-v",
        release,
        "-l",
        "English",
    ]
    logger = logging.getLogger("cleandoc")
    logger.debug(" ".join(qs_args))
    qs_out, qs_err = run_capture_out(qs_args)
    qs_str = f"\n{format_header('Sphinx Quickstart Output')}\n{qs_out}\n{qs_err}"
    if ("error" in qs_str.lower()) or ("warning" in qs_str.lower()):
        logger.info(qs_str)
        return qs_str
    return ""


def run_apidoc(srcpath: str, pathlist: list[str]) -> str:
    """run_apidoc.

    Parameters
    ----------
    srcpath : str
        srcpath
    pathlist : list[str]
        pathlist
    """
    apidoc_args = ["sphinx-apidoc", "-M", "-o", srcpath] + pathlist
    logger = logging.getLogger("cleandoc")
    logger.debug(" ".join(apidoc_args))
    apidoc_out, apidoc_err = run_capture_out(apidoc_args)
    apidoc_str = (
        f"\n{format_header('Sphinx Apidoc Output')}\n{apidoc_out}\n{apidoc_err}"
    )
    if ("error" in apidoc_str.lower()) or ("warning" in apidoc_str.lower()):
        logger.info(apidoc_str)
        return apidoc_str
    return ""


def run_make(docpath: str) -> str:
    """run_make.

    Parameters
    ----------
    docpath : str
        docpath
    """
    make_args = ["cd", f"{docpath}", "&&", "make", "html"]
    logger = logging.getLogger("cleandoc")
    logger.debug(" ".join(make_args))
    make_out, make_err = run_capture_out(make_args, shell=True)
    make_str = f"\n{format_header('Sphinx Make Output')}\n{make_out}\n{make_err}"
    if ("error" in make_str.lower()) or ("warning" in make_str.lower()):
        logger.info(make_str)
        return make_str
    return ""


def get_release(confpath: str) -> str:
    """get_release.

    Parameters
    ----------
    confpath : str
        confpath

    Returns
    -------
    str

    """

    if not path.exists(confpath):
        return "0.0.1"
    with open(confpath, "r", encoding="ascii") as conffile:
        conftext = conffile.readlines()
    release_found = findall(r"release = '([\d\.]*)'", "".join(conftext))
    if len(release_found) == 0:
        return "0.0.1"
    release = release_found[0]
    logger = logging.getLogger("cleandoc")
    logger.debug("    last sphinx release found: %s", release)
    release_split = release.split(".")
    release_split[2] = str(int(release_split[2]) + 1)
    release = ".".join(release_split)
    return release


def edit_conf(confpath: str, pathlist: list[str]):
    """edit_conf.

    Parameters
    ----------
    confpath : str
        confpath
    pathlist : list[str]
        pathlist
    """
    with open(confpath, "r", encoding="ascii") as conffile:
        conflines_orig = conffile.readlines()
    conflines = add_conf_paths(conflines_orig, pathlist)
    conftext_orig = "".join(conflines)
    conftext = add_conf_settings(conftext_orig)
    with open(confpath, "w", encoding="ascii") as conffile:
        conffile.write(conftext)


def add_conf_paths(conflines: list[str], pathlist: list[str]):
    """add_conf_paths.

    Parameters
    ----------
    conflines : list[str]
        conflines
    pathlist : list[str]
        pathlist
    """
    importlines = ["from sys import path\n"]
    fixpaths = [dirpath.replace(sep, "/") for dirpath in pathlist]
    pathlines = [f'path.insert(0, "{fixpath}")\n' for fixpath in fixpaths]
    conflines_out = importlines + pathlines + conflines
    return conflines_out


def add_conf_settings(conftext: str) -> str:
    """add_conf_settings.

    Parameters
    ----------
    conftext : str
        conftext

    Returns
    -------
    str

    """
    sphinxexts = """
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',]

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
"""
    conftext = sub(r"extensions = \[\]", sphinxexts, conftext)
    conftext_out = sub(
        r"html_theme = 'alabaster'", "html_theme = 'sphinx_rtd_theme'", conftext
    )
    return conftext_out


def edit_index(srcpath: str, pkgname: str):
    """edit_index.

    Parameters
    ----------
    srcpath : str
        srcpath
    """
    add_modules = f":caption: Contents:\n    \n   {pkgname}"
    indexpath = path.join(srcpath, "index.rst")
    modulespath = path.join(srcpath, "modules.rst")
    if path.exists(modulespath):
        remove(modulespath)
    with open(indexpath, "r", encoding="ascii") as indexfile:
        indexlines = indexfile.readlines()
    indextext = "".join(indexlines)
    indextext = sub(r":caption: Contents:", add_modules, indextext)
    indextext = sub(r":maxdepth: 4", ":maxdepth: 10", indextext)
    with open(indexpath, "w", encoding="ascii") as indexfile:
        indexfile.write(indextext)


# if __name__ == "__main__":
