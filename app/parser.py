from bs4 import BeautifulSoup
import urllib2
import nltk

import util
import recipe


def parse_html(html):
    """
    Takes HTML and does some basic parsing
    :param html: html text
    :return: Title string, list of ingredient/quantity tuples, and list of step strings
    """
    soup = BeautifulSoup(html)
+    if soup.find('span', {'itemprop': 'name'}):
+        title = soup.find('span', {'itemprop': 'name'}).get_text()
+    elif soup.find('h1', {'itemprop': 'name'}):
+        title = soup.find('h1', {'itemprop': 'name'}).get_text()
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


def parse_ingredient(tupes):
    """
    Takes ingredient-name string from parse_html, separates ingredient into name, descriptor, preparation, and prep descriptor
    :param tupes: the ingredient-name part of tupes
    :return: ingredient name, list of descriptors, list of preparations, list of prep descriptors
    """
    # TODO: consider words with 2 POS tags (remove from consideration after being added?)
    # TODO: use context clues?
    # TODO: use only accepted ingredients names as the basis for name (rather than all nouns)
    # TODO: Change from lists to a single string object
    # Look for commas, ands, other syntax patterns

    ingredients = tupes

    name = []
    descriptor = []
    preparation = []
    prep_description = []

    for i in ingredients:
        tokens = nltk.word_tokenize(i[0])
        pos_tagged_tokens = nltk.pos_tag(tokens)
        for word, tag in pos_tagged_tokens:
            if tag == 'NN':
                name.append(word)
            elif tag == 'ADJ':
                descriptor.append(word)
            elif tag == 'VBD':
                preparation.append(word)
            elif tag == 'ADV':
                prep_description.append(word)
    return name, descriptor, preparation, prep_description


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


def make_recipe(title, ingredients, steps):
    """
    STUB DESCRIPTION:
    Write the make_recipe function in app.parser that will take as input the output of parse_html, and output a
    Recipe object. Use the various ingredient matching functions in kb.py to achieve this.
    :param title: title of recipe
    :param ingredients: list of ingredients (strings)
    :param steps: list of steps (strings)
    :return: Recipe
    """
    return recipe.Recipe()  # Stub


def format_for_autograder(url):
    """
    Formats our recipe representation as a dictionary to be read by autograder
    :param url: Recipe url
    :return: JSON for autograder
    """
    pass


def find_cooking_tools(steps, knowledge_base):
    """
    finds cooking tools by comparing step string to cooking_wares.txt.
    Avoids duplicates by replacing found items with empty string.
    :param steps:
    :return: list of tools as list of words
    """
    wares = knowledge_base.cooking_wares
    tool_list = []
    for e in steps:
        e = e.lower()
        for tool in wares:
            if tool in e and tool not in tool_list:
                e = e.replace(tool, '')
                tool_list.append(tool)
                # print tool
    return tool_list


def find_cooking_methods(steps, knowledge_base):
    """
    finds cooking methods by comparing step string to cooking_terms.txt.
    Avoids duplicates by replacing matched methods with empty string.
    :param steps:
    :return: method list as list of words
    """
    verbiage = knowledge_base.cooking_terms
    method_list = []
    for step in steps:
        step = step.lower()
        for method in verbiage:
            if method in step and method not in method_list:
                step = step.replace(method, '')
                method_list.append(method)
    return method_list
