__author__ = 'Pantsworth'

import util
import kb
from difflib import SequenceMatcher
from random import randrange
import recipe

def classify_recipe(made_recipe):
    """
    grabs a recipe and classifies it as italian, mexican, asian, or neutral
    :param made_recipe:
    :return:
    """
    italian_titles = kb.read_txt_lines_into_list(util.relative_path("kb_data/italian_titles.txt"))
    mexican_titles = kb.read_txt_lines_into_list(util.relative_path("kb_data/mexican_titles.txt"))
    east_asian_titles = kb.read_txt_lines_into_list(util.relative_path("kb_data/east_asian_titles.txt"))
    recipe_title = made_recipe.title.lower()

    recipe_type = "neutral"
    for potential_title in italian_titles:
        if potential_title in recipe_title:
            recipe_type = "italian"
    for potential_title in mexican_titles:
        if potential_title in recipe_title:
            recipe_type = "mexican"
    for potential_title in east_asian_titles:
        if potential_title in recipe_title:
            recipe_type = "asian"

    print "\n" + recipe_title
    return recipe_type



def spice_classify(parsed_html, knowledge_base):
    sauce_words = kb.read_specific_lines(util.relative_path("kb_data/style_substitutions.txt"), "#sauce_words", "#end_sauce_words")
    classification = classify_recipe(parsed_html[0])
    recipe_steps = parsed_html
    sauce_status = False
    result = ""

    for step in recipe_steps[2]:
        if "soy sauce" in step or "taco sauce":
            step = step.replace("soy sauce", '')
            step = step.replace("taco sauce", '')
        if " sauce " in step:
            sauce_status = True
            break
        for sauces in sauce_words:
            if sauces in step or recipe_steps[0]:
                sauce_status = True
                break

    ingredient_list = []
    for (item, amount) in parsed_html[1]:
        ingredient_list.append(item)

    if sauce_status == True and classification == "italian":
        # print "italian with sauce"
        italian_red = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#italian_red", "#end_italian_red")
        italian_white = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#italian_white", "#end_italian_white")
        italian_green = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#italian_pesto", "#end_italian_pesto")

        italian_red_result = SequenceMatcher(None, ingredient_list, italian_red).ratio()
        print "italian red:"
        print italian_red_result

        italian_white_result = SequenceMatcher(None, ingredient_list, italian_white).ratio()
        print "italian white:"
        print italian_white_result

        italian_green_result = SequenceMatcher(None, ingredient_list, italian_green).ratio()
        print "italian green:"
        print italian_green_result

        if italian_white_result > italian_red_result:
            result = "italian_white"
        else:
            result = "italian_red"


    if sauce_status == True and classification == "asian":
        # print "asian with sauce"
        asian_orange = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#asian_orange", "#asian_orange_end")
        asian_brown = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#asian_brown", "#asian_brown_end")
        asian_sesame = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#asian_sesame", "#asian_sesame_end")
        # asian_teriyaki = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#asian_teriyaki", "#asian_teriyaki_end")

        orange_result = SequenceMatcher(None, ingredient_list, asian_orange).ratio()
        print "asian_orange: "
        print orange_result

        brown_result = SequenceMatcher(None, ingredient_list, asian_brown).ratio()
        print "asian_brown: "
        print brown_result

        sesame_result = SequenceMatcher(None, ingredient_list, asian_sesame).ratio()
        print "asian_sesame: "
        print sesame_result

        # teriyaki_result = SequenceMatcher(None, ingredient_list, asian_teriyaki).ratio()
        # print "asian_teriyaki: "
        # print teriyaki_result


        if (orange_result > brown_result) and (orange_result > sesame_result):
            result = "asian_orange"
        elif (sesame_result > orange_result) and (sesame_result >brown_result):
            result = "asian_sesame"
        else:
            result = "asian_brown"

    if sauce_status == False and classification == "asian":
        result = "asian_no_sauce"

    if sauce_status == True and classification == "mexican":
        # print "mexican with sauce"
        mexican_red = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#mexican_red", "#end_mexican_red")
        mexican_white = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#mexican_white", "#end_mexican_white")

        red_result = SequenceMatcher(None, ingredient_list, mexican_red).ratio()
        print "red_result: "
        print red_result
        white_result = SequenceMatcher(None, ingredient_list, mexican_white).ratio()
        print "white_result: "
        print white_result

        if white_result > red_result:
            result = "mexican_white"
        else:
            result = "mexican_red"

    if sauce_status == False and classification == "mexican":
        result = "mexican_no_sauce"

    remove_spices(parsed_html, result, knowledge_base)
    return result


# def testing_recipe(from_recipe):
#     print from_recipe.ingredients


def remove_spices(parsed_results, sauce_type, knowledge_base):

    type_fusion = "to_italian"

    mexican_spices = kb.read_specific_lines(util.relative_path("kb_data/style_substitutions.txt"), "#mexican_spices", "#end_mexican_spices")
    mexican_ingredients = kb.read_specific_lines(util.relative_path("kb_data/style_substitutions.txt"), "#mexican_ingredients", "#end_mexican_ingredients")
    mexican_to__italian = kb.read_specific_lines(util.relative_path("kb_data/style_substitutions.txt"), "#mexican_to_italian", "#end_mexican_to_italian")

    italian_spices = kb.read_specific_lines(util.relative_path("kb_data/style_substitutions.txt"), "#italian_spices", "#end_italian_spices")
    asian_spices = kb.read_specific_lines(util.relative_path("kb_data/style_substitutions.txt"), "#asian_spices", "#end_asian_spices")

    # mexican to italian

    if sauce_type != "mexican_no_sauce":
        fusion_method = randrange(1, 4)

        if fusion_method==1:
            print 1
            #replace sauce with red sauce

        if fusion_method==2:
            print 2

            #replace sauce with italian white

        if fusion_method==3:
            print 3

            #replace with pesto

        if fusion_method==4:
            print 4
            #replace with dry italian herbs


        for spice in mexican_spices:
            for (item, amount) in parsed_results[1]:
                if spice in item:
                    print item

        # this isn't done at all.
        # for (ingredient, substitution) in kb.mexican_to_italian:




