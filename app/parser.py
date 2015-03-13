from bs4 import BeautifulSoup
import urllib2

import util


def parse_html(html):
    """
    Takes HTML and does some basic parsing
    :param html: html text
    :return: Title string, list of ingredient/quantity tuples, and list of step strings
    """
    soup = BeautifulSoup(open('C:\\Users\\Neal\\Documents\\Coursework\\EECS\\337\\lasagne_html.html'))
    title = soup.find('span', {'itemprop': 'name'}).get_text()
    ingredients = soup.find_all('p', {'itemprop': 'ingredients'})
    tupes = []
    for i in ingredients:
        a = i.find('span', {'class': 'ingredient-amount'}).get_text()
        n = i.find('span', {'class': 'ingredient-name'}).get_text()
        tupes.append((n, a))

    directions = soup.find_all('span', {'class': 'plaincharacterwrap break'})
    steps = []
    for d in directions:
        steps.append(d.get_text())
    return title, tupes, steps


def url_to_dictionary(url):
    """
    FOR TESTING PURPOSES ONLY, takes a url and runs the various parsing functions to return a dictionary in the JSON
    representation that Miriam's autograder accepts
    :param url: url of requested recipe
    :return: dictionary in autograder-acceptable format
    """
    html = get_html(url)
    # etc
    pass


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
