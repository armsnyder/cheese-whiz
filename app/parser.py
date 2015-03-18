from bs4 import BeautifulSoup
import urllib2
import nltk
import regex

import util
import recipe


def parse_ingredient(ingredient, knowledge_base):
    """
    Takes ingredient-name string from parse_html, separates ingredient into name, descriptor, preparation, and prep descriptor
    :param tupes: the ingredient-name part of tupes
    :return: ingredient name, list of descriptors, list of preparations, list of prep descriptors
    """
    # TODO: consider words with 2 POS tags (remove from consideration after being added?)
    # TODO: use context clues?
    # TODO: handle commas, ands, other syntax patterns


    name_string = 'unknown'
    rest_words = []
    descriptor_words = []
    preparation_words = []
    prep_description_words = []
    only_name_words = []

    ingredient = ingredient.replace(', or to taste', '')

    name_words = ingredient.split()
    for w in range(len(name_words)):
        query = ' '.join(name_words[w:])
        if not knowledge_base.lookup_food(query):
            rest_words = name_words[:(w+1)]
            continue
        else:
            rest_words = name_words[:w]
            name_string = ' '.join(name_words[w:])
            break

    rest_words = [remove_unicode(thing) for thing in rest_words]
    rest_string = ' '.join(rest_words)
    tokens = nltk.word_tokenize(rest_string)
    pos_tagged_tokens = nltk.pos_tag(tokens)
    for word, tag in pos_tagged_tokens:
        if name_string == 'unknown':
            if tag == 'NN':
                only_name_words.append(word)
        if tag == 'ADJ' or tag == 'JJ':
            descriptor_words.append(word)
        elif tag == 'VBD':
            preparation_words.append(word)
        elif tag == 'ADV' or tag == 'RB':
            prep_description_words.append(word)

    if name_string == 'unknown':
        if only_name_words:
            name_string = ' '.join(only_name_words)
    if not descriptor_words:
        d = 'none'
    else:
        d = ' '.join(descriptor_words)
    if not preparation_words:
        p = 'none'
    else:
        p = ' '.join(preparation_words)
    if not prep_description_words:
        pd = 'none'
    else:
        pd = ' '.join(prep_description_words)

    return name_string, d, p, pd


def parse_html(html):
    """
    Takes HTML and does some basic parsing
    :param html: html text
    :return: Title string, list of ingredient/quantity tuples, and list of step strings
    """
    soup = BeautifulSoup(html)
    if soup.find('span', {'itemprop': 'name'}):
        title = soup.find('span', {'itemprop': 'name'}).get_text()
    elif soup.find('h1', {'itemprop': 'name'}):
        title = soup.find('h1', {'itemprop': 'name'}).get_text()
    else:
        title = 'untitled'
    ingredients = soup.find_all('p', {'itemprop': 'ingredients'})
    ingredient_quantity_string_tuples = []
    for i in ingredients:
        if i.find('span', {'class': 'ingredient-amount'}):
            a = i.find('span', {'class': 'ingredient-amount'}).get_text()
        else:
            a = 'NO_UNIT'
        n = i.find('span', {'class': 'ingredient-name'}).get_text()
        ingredient_quantity_string_tuples.append((n, a))

    directions = soup.find_all('span', {'class': 'plaincharacterwrap break'})
    steps = []
    if directions:
        for d in directions:
            steps.append(d.get_text())
    else:
        steps.append('No directions.')
    return title, ingredient_quantity_string_tuples, steps


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


def url_to_recipe(url, knowledge_base):
    """
    Takes a recipe URL and returns a Recipe object
    :param url: recipe url
    :param knowledge_base: loaded knowledge base
    :return: Recipe
    """
    recipe_html = get_html(url)
    recipe_title, recipe_ingredients, recipe_steps = parse_html(recipe_html)
    return make_recipe(recipe_title, recipe_ingredients, recipe_steps, knowledge_base)


def make_recipe(title, ingredients, steps, knowledge_base):
    """
    STUB DESCRIPTION:
    Write the make_recipe function in app.parser that will take as input the output of parse_html, and output a
    Recipe object. Use the various ingredient matching functions in kb.py to achieve this.
    :param title: title of recipe
    :param ingredients: list of ingredients (strings)
    :param steps: list of steps (strings)
    :return: Recipe
    """
    ingredient_object_list = []
    for ingredient_string, quantity_string in ingredients:
        quantity = knowledge_base.interpret_quantity(quantity_string)
        i_name, i_descriptor, i_prep, i_prep_descriptor = parse_ingredient(ingredient_string, knowledge_base)
        ingredient_object_list.append(
            recipe.Ingredient(i_name, quantity, i_descriptor, i_prep, i_prep_descriptor).match_to_food(knowledge_base))
    return recipe.Recipe(title, ingredient_object_list, steps)


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


def remove_unicode(text):
    """
    Cleans ingredient text from allrecipes
    :param text: text with unicode
    :return: text without unicode
    """
    # TODO: Make sure jalapeno works with this encoding
    encoded_text = text.encode('utf-8')
    return regex.uni.sub('', encoded_text)