# The "main" file for Cheese Whiz

import urllib2

import kb


def main():
    knowledge_base = kb.KnowledgeBase()
    knowledge_base.load()


def get_html(url):
    """
    Retrieves html text from a string-formatted url
    :param url: web url string
    :return: html text
    """
    if '://' not in url:
        formatted_url = 'http://' + url
    else:
        formatted_url = url
    return urllib2.urlopen(formatted_url).read()
