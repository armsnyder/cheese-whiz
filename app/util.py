# Contains all magic numbers and strings, as well as useful generic functions
# Constant values and functions are defined for easy reference

import sys


app_name = 'Cheese Whiz'
verbose = True


def warning(text, exit=False, status=1):
    """prints a custom error message to console"""
    if exit:
        sys.stderr.write("FATAL ERROR: "+text+"\n")
        sys.exit(status)
    else:
        sys.stderr.write("WARNING: "+text+"\n")
    return


def close(message=None):
    """for debugging, exits program and outputs some variable"""
    if message:
        print(message)
    sys.exit(0)


def vprint(text):
    """prints a custom message to console if in verbose mode"""
    if verbose:
        print(text)
    return