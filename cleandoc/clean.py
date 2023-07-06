# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

import logging
from .helper import run_capture_out, format_header, check_for_pkg

for pkg in ["black", "pylint", "mypy"]:
    check_for_pkg(pkg)


def run_black(pyfilepath: str, write: bool = True):
    """run_black.

    Parameters
    ----------
    pyfilepath : str
        pyfilepath
    write : bool
        write
    """
    # Auto-format code with black
    black_out, black_err = run_capture_out(["black", pyfilepath, "--diff"])
    if write:
        black_out, black_err = run_capture_out(["black", pyfilepath])
    black_str = f"{format_header('Black Output')}\n{black_out}\n{black_err}"
    if "1 file left unchanged." not in black_str:
        logger = logging.getLogger("cleandoc")
        logger.info(black_str)
        return black_str
    return ""


def run_pylint(pyfilepath: str):
    """run_pylint.

    Parameters
    ----------
    pyfilepath : str
        pyfilepath
    """
    # Check code cleanliness with pylint
    pylint_out, pylint_err = run_capture_out(["pylint", pyfilepath])
    pylint_str = f"{format_header('Pylint Output')}\n{pylint_out}\n{pylint_err}"
    if "Your code has been rated at 10.00/10" not in pylint_str:
        logger = logging.getLogger("cleandoc")
        logger.info(pylint_str)
        return pylint_str
    return ""


def run_mypy(pyfilepath: str):
    """run_mypy.

    Parameters
    ----------
    pyfilepath : str
        pyfilepath
    """
    # Check variable type hints with mypy
    mypy_args = ["mypy", pyfilepath, "--check-untyped-defs", "--ignore-missing-imports"]
    mypy_out, mypy_err = run_capture_out(mypy_args)
    mypy_str = f"{format_header('Mypy Output')}\n{mypy_out}\n{mypy_err}"
    if "Success: no issues found" not in mypy_str:
        logger = logging.getLogger("cleandoc")
        logger.info(mypy_str)
        return mypy_str
    return ""


# if __name__ == "__main__":
