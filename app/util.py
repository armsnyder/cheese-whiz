# Contains all magic numbers and strings, as well as useful generic functions
# Constant values and functions are defined for easy reference

import sys
import os


app_name = 'Cheese Whiz'
verbose = True


def warning(text, exit=False, status=1):
    """
    prints a custom error message to console
    :param text: text to print
    :param exit: if True, system throws FATAL ERROR and exits
    :param status: status code to return on system exit
    """
    if exit:
        sys.stderr.write("FATAL ERROR: "+text+"\n")
        sys.exit(status)
    else:
        sys.stderr.write("WARNING: "+text+"\n")


def close(message=None):
    """
    for debugging, exits program and outputs some variable
    :param message: text to print on exit
    """
    if message:
        print(message)
    sys.exit(0)


def vprint(text):
    """
    prints a custom message to console if in verbose mode
    :param text: text to print
    """
    if verbose:
        print(text)


def relative_path(path):
    """
    Get file path relative to calling script's directory
    :param path: filename or file path
    :return: full path name, relative to script location
    """
    return os.path.join(os.path.join(os.getcwd(), os.path.dirname(__file__)), path)