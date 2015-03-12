import urllib2

import util


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
    try:
        return urllib2.urlopen(formatted_url).read()
    except urllib2.URLError:
        util.warning('Invalid URL request')
        return None


def parse_html(html):
    """
    Takes HTML and does some basic parsing
    :param html: html text
    :return: ???
    """
    pass