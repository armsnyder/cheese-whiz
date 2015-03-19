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
    tag_name = ['NN', 'NNP', 'NNPS', 'NNS', 'PRP', 'PRP$']
    tag_des = ['JJ']
    tag_prep = ['VBD', 'VBN']
    tag_prep_des = ['ADV', 'RB', 'RBR', 'RBS']
    special_cases = {
        'des': ['ground'],
        'prep': [],
        'prep_des': []
        }
    name_string = 'unknown'
    rest_words = []
    descriptor_words = []
    preparation_words = []
    prep_description_words = []
    only_name_words = []

    ingredient = ingredient.lower()
    ingredient = ingredient.replace(', or to taste', '')
    ingredient = ingredient.replace(' or to taste', '')
    ingredient = ingredient.replace(', to taste', '')
    ingredient = ingredient.replace(' to taste', '')
    ingredient = remove_unicode(ingredient)
    i_tokens = nltk.pos_tag(nltk.word_tokenize(ingredient))
    # for i in range(len(i_tokens)):
    #     ii = i_tokens[i][0]
    #     if ii in special_cases:
    #         i_tokens = i_tokens[:i].append((ii, special_cases[ii])).append(i_tokens[i+1:])
    for i in range(len(i_tokens)):
        if i_tokens[i][0] == ',' and i != 0 and i != len(i_tokens)-1:
            if i_tokens[i-1][1] in tag_name:
                i_tokens = i_tokens[i+1:] + i_tokens[:i]
                break
    for w in range(len(i_tokens)):
        query = ' '.join([t[0] for t in i_tokens[w:]])
        if knowledge_base.lookup_food(query):
            rest_words = i_tokens[:w]
            name_string = ' '.join([t[0] for t in i_tokens[w:]])
            break

    for i in range(len(rest_words)):
        tag = rest_words[i][1]
        word = rest_words[i][0]
        if name_string == 'unknown':
            if tag == 'NN':
                only_name_words.append(word)
        if tag in tag_des or word in special_cases['des']:
            descriptor_words.append(word)
        elif tag in tag_prep or word in special_cases['prep']:
            preparation_words.append(word)
        elif tag in tag_prep_des or word in special_cases['prep_des']:
            prep_description_words.append(word)
        elif tag == 'IN':
            descriptor_words.append(word)
            if i < len(rest_words) - 1:
                descriptor_words.append(rest_words[i+1][0])
                i += 1
        elif tag == 'CC':
            prep_description_words.append(word)
        else:
            descriptor_words.append(word)

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
    title = title.lower()
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


def get_first_recipe_from_search_results(html):
    soup = BeautifulSoup(html)
    if soup.find('a', href=True, id='ctl00_CenterColumnPlaceHolder_rptResults_ctl00_ucResultContainer_ucRecipeGrid_imgLink'):
        first_recipe = soup.find('a', href=True, id='ctl00_CenterColumnPlaceHolder_rptResults_ctl00_ucResultContainer_ucRecipeGrid_imgLink')
        result = 'http://allrecipes.com' + str(first_recipe['href'])
        return result
    return 'http://allrecipes.com/recipe/grilled-peanut-butter-and-jelly-sandwich/'


def url_to_dictionary(url, knowledge_base):
    """
    FOR TESTING PURPOSES ONLY, takes a url and runs the various parsing functions to return a dictionary in the JSON
    representation that Miriam's autograder accepts
    :param url: url of requested recipe
    :return: dictionary in autograder-acceptable format
    """
    final_recipe = url_to_recipe(url, knowledge_base)
    result = {
        'ingredients': [ingredient_to_dictionary(i) for i in final_recipe.ingredients],
        'primary cooking method': final_recipe.primary_method,
        'cooking methods': final_recipe.methods,
        'cooking tools': final_recipe.tools
    }
    return result


def ingredient_to_dictionary(ingredient):
    result = {
        'name': ingredient.name,
        'quantity': ingredient.quantity.amount,
        'measurement': ingredient.quantity.unit,
        'descriptor': ingredient.descriptor,
        'preparation': ingredient.preparation,
        'prep-description': ingredient.prep_description
    }
    return result


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
    result = recipe.Recipe(title, ingredient_object_list, steps)
    result.methods = find_cooking_methods(steps, knowledge_base)
    result.tools = find_cooking_tools(steps, knowledge_base)
    result.primary_method = find_primary_method(result.methods)
    return result


def find_primary_method(methods):
    method_index = []
    for i in range(len(methods)):
        method_index.append((methods[i], sort_methods(methods[i], i, len(methods))))
    return sorted(method_index, key=lambda x: x[1], reverse=True)[0][0]


def sort_methods(method, i, n):
    top_methods = ['bake',
                   'broil',
                   'grill',
                   'poach',
                   'roast',
                   'barbeque',
                   'smoke',
                   'braise',
                   'stew',
                   'fry',
                   'panfry',
                   'cook',
                   'scald',
                   'microwave',
                   'sautee',
                   'saute',
                   'deep-fry',
                   'simmer',
                   'cure',
                   'sear',
                   'blacken',
                   'brown',
                   'boil']
    rank = i * 75 / n
    for j in range(len(top_methods)):
        if top_methods[j] in method:
            rank += (len(top_methods) - j) * 100 / len(top_methods)
            break
    return rank


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
    try:
        decoded_text = text.decode('unicode_escape')
    except UnicodeDecodeError:
        util.warning('UnicodeDecodeError on decode: '+text)
        decoded_text = ''
    except UnicodeEncodeError:
        util.warning('UnicodeEncodeError on decode: '+text)
        decoded_text = ''
    try:
        encoded_text = decoded_text.encode('utf-8')
    except UnicodeDecodeError:
        util.warning('UnicodeDecodeError on encode: '+text)
        encoded_text = ''
    except UnicodeEncodeError:
        util.warning('UnicodeEncodeError on encode: '+text)
        encoded_text = ''
    return regex.uni.sub('', encoded_text)
