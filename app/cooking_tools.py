__author__ = 'pantsworth'

import re
import util
import kb
import nltk

def find_cooking_tools(steps):
    """
    finds cooking tools by comparing step string to cooking_wares.txt.
    Avoids duplicates by replacing found items with empty string.
    :param steps:
    :return: list of tools as list of words
    """
    wares = kb.read_txt_lines_into_list(util.relative_path("kb_data/cooking_wares.txt"))
    tool_list = []
    for e in steps:
        e = e.lower()
        for tool in wares:
            if tool in e and tool not in tool_list:
                e = e.replace(tool, '')
                tool_list.append(tool)
                # print tool
    return tool_list


def find_cooking_methods(steps):
    """
    finds cooking methods by comparing step string to cooking_terms.txt.
    Avoids duplicates by replacing matched methods with empty string.
    :param steps:
    :return: method list as list of words
    """
    verbiage = kb.read_txt_lines_into_list(util.relative_path("kb_data/cooking_terms.txt"))
    method_list = []
    for step in steps:
        step = step.lower()
        for method in verbiage:
            if method in step and method not in method_list:
                step = step.replace(method, '')
                method_list.append(method)
    return method_list