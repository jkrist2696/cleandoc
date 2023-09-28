# -*- coding: utf-8 -*-
# Pylint will be mad because there is no script docstring

import shutil
import webbrowser
import cleandoc as cd
import os  # this import should be before cleandoc, pylint will complain

def example_fxn_1()->str:
    """
    Set a variable that get flagged by Pylint
    """
    ISSUE_2 = 0 # pylint complains because variables in functions should be snake or lowercase
    ISSUE_2 = "setting a previous int to a string now. Mypy will complain"
    return ISSUE_2


if __name__=="__main__":
    # Create nested source file folder and copy in this script
    maindir = os.path.dirname(os.path.abspath(__file__))
    srcpath = os.path.join(maindir, "src")
    os.mkdir(srcpath)
    dirpath = os.path.join(srcpath, "readme_test")
    os.mkdir(dirpath)
    scriptpath = os.path.join(maindir, "src", "readme_test", os.path.basename(os.path.abspath(__file__)))
    shutil.copyfile(os.path.abspath(__file__), scriptpath)

    print("\n\n>>> Cleaning One Python File <<<\n")
    cd.clean_pyfile(scriptpath, write=True)
    print("\n\n>>> Cleaning All Python Files in Directory <<<\n")
    cd.clean_all(dirpath, ignore=True, write=False, skip=True)
    print("\n\n>>> Cleaning All and Generating HTML Docs <<<\n")
    try:
        # Below line runs clean_all and gen_docs functions
        # Raises a syntax warnings because ignore=False, so docs are not generated
        cd.cleandoc_all(dirpath, ignore=False, write=True, release="0.0.1")
    except SyntaxWarning as error:
        print(f"syntax warning:\n\n{error}")
    print("\n\n>>> Generating HTML Documents with Sphinx <<<\n")
    webpage = cd.gen_docs(dirpath, changed=True, release="0.0.1")

    issue_1 = "This string line is way too long. Why did you need to type this all in one line? Black is going to try to shorten this and pylint will complain. Pylint also complains because constaints in main script should be all uppercase."
    ISSUE_2 = example_fxn_1()
    ISSUE_3 = ["really","long","list","so","black","reformats","it","and","turns","the","one","line","list","into","multi","line"]

    # Delete src folder created at begining of script
    shutil.rmtree(srcpath)
    webbrowser.open(webpage)