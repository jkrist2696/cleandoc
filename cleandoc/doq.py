# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from subprocess import run
from re import findall
import logging
from .helper import run_capture_out, format_header, check_for_pkg, findall_infile

# check for packages called in subprocess commands in this module
check_for_pkg("doq")


def run_doq(pyfilepath: str, formatter: str = "numpy", write: bool = True):
    """Auto-Generate Docstrings with doq (py-doq) package. Doq command is
    executed via subprocess command to create docstrings where missing.

    Parameters
    ----------
    pyfilepath : str
        Full path to python (.py) file
    formatter : str
        ["numpy","google","sphinx"] : See doq documentation for formatting options
    write : bool
        True = write the auto-gen docstrings in-place

    Returns
    -------
    str
        Summary of command outputs
    """
    # Generate Simple Docstrings with doq where they dont exists
    doq_out, doq_err = run_capture_out(["doq", "-f", pyfilepath, "--formatter=numpy"])
    if (len(doq_out) + len(doq_err)) == 0:
        return ""
    if write:
        run(["doq", "-f", pyfilepath, "-w", f"--formatter={formatter}"], check=True)
        doq_str = f"{format_header('Doq Output')}\n\n\
            Simple Docstrings Added. Please Complete Them!\n"
    else:
        doq_str = f"{format_header('Doq Output')}\n{doq_out}\n{doq_err}"
    logger = logging.getLogger("cleandoc")
    logger.info(doq_str)
    return doq_str


def check_docstrings(pyfilepath: str):
    """Check if Docstrings were not edited after being auto-generated.

    Parameters
    ----------
    pyfilepath : str
        Full path of python (.py) file

    Returns
    -------
    str
        Summary of command outputs
    """
    desc_regex = r'def ([^(]*).*\r*\n *("""(.*?)(.|\n|\r)*?""")'
    var_regex = r" +([a-zA-Z0-9_]+) :.*\r*\n +([a-zA-Z0-9_]+)"
    desc_search = findall_infile(desc_regex, pyfilepath)
    check_str = ""
    for desc_found in desc_search:
        funname, docstring, desc = desc_found[0:3]
        check_sum = funname == (desc + ".")
        var_search = findall(var_regex, docstring)
        for var_found in var_search:
            check_sum += var_found[0] == var_found[1]
        if check_sum > 0:
            check_str += docstring + "\n"
    if len(check_str) == 0:
        return ""
    logger = logging.getLogger("cleandoc")
    check_str = (
        f"{format_header('Check Docstring Output')}\n\n\
        Complete the following auto-generated docstrings!\n\n"
        + check_str
    )
    logger.info(check_str)
    return check_str


# if __name__ == "__main__":
