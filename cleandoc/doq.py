# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from subprocess import run
import logging
from .helper import run_capture_out, format_header, check_for_pkg

check_for_pkg("doq")


def run_doq(pyfilepath: str, formatter: str = "numpy"):
    """run_doq.

    Parameters
    ----------
    pyfilepath : str
        pyfilepath
    formatter : str
        formatter
    """
    # Generate Simple Docstrings with doq where they dont exists
    doq_out, doq_err = run_capture_out(["doq", "-f", pyfilepath, "--formatter=numpy"])
    if (len(doq_out) + len(doq_err)) == 0:
        return ""
    run(["doq", "-f", pyfilepath, "-w", f"--formatter={formatter}"], check=True)
    doq_str = f"{format_header('Doq Output')}\n\n\
      Simple Docstrings Added. Please Complete Them!\n"
    logger = logging.getLogger("cleandoc")
    logger.info(doq_str)
    return doq_str


# if __name__ == "__main__":
