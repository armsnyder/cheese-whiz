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
    recipe_title = (made_recipe.title()).lower()

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
    return recipe_type


def sauce_status(sauce_words, made_recipe):
    pass

def spice_classify(made_recipe, knowledge_base):
    sauce_words = kb.read_specific_lines(util.relative_path("kb_data/style_substitutions.txt"), "#sauce_words", "#end_sauce_words")
    classification = classify_recipe(made_recipe.title)
    print "classification of recipe: ", classification
    recipe_steps = made_recipe.steps
    print "Recipe Steps: ", recipe_steps
    sauce_status = False
    result = ""

    for step in recipe_steps:
        if "soy sauce" in step:
            step = step.replace("soy sauce", '')
        if "taco sauce" in step:
            step = step.replace("taco sauce", '')
        if " sauce " in step:
            sauce_status = True
            break
        for sauce in sauce_words:
            if sauce in step:
                print sauce
                sauce_status = True
                break
            elif sauce in recipe_steps[0]:
                print sauce
                sauce_status = True
                break

    ingredient_list = []
    for item in made_recipe.ingredients:
        print item.name, item.quantity.amount, item.quantity.unit
        ingredient_list.append(item.name)

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
        print "mexican_red_result: "
        print red_result
        white_result = SequenceMatcher(None, ingredient_list, mexican_white).ratio()
        print "mexican_white_result: "
        print white_result

        if white_result > red_result:
            result = "mexican_white"
        else:
            result = "mexican_red"

    if (sauce_status == False) and (classification == "mexican"):
        result = "mexican_no_sauce"

    # recipe_fusion(made_recipe, result, fusion_style, knowledge_base)
    return result




def testing_recipe(from_recipe):
    for ingredient_objects in from_recipe.ingredients:
        print ingredient_objects.name




def recipe_fusion(made_recipe, fusion_style, knowledge_base):
    sauce_type = spice_classify(made_recipe, knowledge_base)
    print "sauce type: ", sauce_type

    mexican_spices = kb.read_specific_lines(util.relative_path("kb_data/style_substitutions.txt"), "#mexican_spices", "#end_mexican_spices")
    mexican_ingredients = kb.read_specific_lines(util.relative_path("kb_data/style_substitutions.txt"), "#mexican_ingredients", "#end_mexican_ingredients")

    italian_spices = kb.read_specific_lines(util.relative_path("kb_data/style_substitutions.txt"), "#italian_spices", "#end_italian_spices")
    italian_ingredients = kb.read_specific_lines(util.relative_path("kb_data/style_substitutions.txt"), "#italian_ingredients", "#end_italian_ingredients")


    asian_spices = kb.read_specific_lines(util.relative_path("kb_data/style_substitutions.txt"), "#asian_spices", "#end_asian_spices")
    asian_ingredients = kb.read_specific_lines(util.relative_path("kb_data/style_substitutions.txt"), "#asian_ingredients", "#end_asian_ingredients")


    italian_red = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#italian_red", "#end_italian_red")
    italian_white = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#italian_white", "#end_italian_white")
    italian_green = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#italian_pesto", "#end_italian_pesto")
    mexican_red = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#mexican_red", "#end_mexican_red")
    mexican_white = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#mexican_white", "#end_mexican_white")
    asian_orange = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#asian_orange", "#asian_orange_end")
    asian_brown = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#asian_brown", "#asian_brown_end")
    asian_sesame = kb.read_specific_lines(util.relative_path("kb_data/italian_red_sauce.txt"), "#asian_sesame", "#asian_sesame_end")

    # mexican to italian

    fusion_style = "to_italian"

    if "mexican" in sauce_type:
        for spice in mexican_spices:
            for e in range(len(made_recipe.ingredients)):
                if spice in made_recipe.ingredients[e].name:
                    print "matched spice: ", spice, made_recipe.ingredients[e].name
                    print "amount: ", made_recipe.ingredients[e].quantity.amount, made_recipe.ingredients[e].quantity.unit
                if spice in made_recipe.ingredients[e].name and spice not in italian_spices:
                    print "not in italian:", made_recipe.ingredients[e].name
                    spicesub = randrange(1,len(knowledge_base.italian_spices_subs))
                    print "replaced: ", made_recipe.ingredients[e].name, " with ", knowledge_base.italian_spices_subs[spicesub].food_out[0].name
                    replaced_ingredient = made_recipe.ingredients[e].name
                    made_recipe.ingredients[e] = knowledge_base.italian_spices_subs[spicesub].food_out[0]
                    made_recipe.replace_ingredient_in_steps(replaced_ingredient, knowledge_base.italian_spices_subs[spicesub].food_out[0].name)
                    for e in range(len(made_recipe.steps)): print made_recipe.steps[e]


        for sub in knowledge_base.mexican_to_italian_list:
            for e in range(len(made_recipe.ingredients)):
                if sub.food_in.name in made_recipe.ingredients[e].name.lower():
                    subbed_ingredient = made_recipe.ingredients[e].name.lower()
                    print "item to sub: " + subbed_ingredient
                    print "replace with: " + sub.food_out[0].name
                    made_recipe.ingredients[e] = sub.food_out[0]
                    made_recipe.replace_ingredient_in_steps(subbed_ingredient, sub.food_out[0].name)


        # for i in made_recipe.ingredients: print i.name
        for e in range(len(made_recipe.steps)): print made_recipe.steps[e]

        made_recipe.change_title("Italian " + made_recipe.title)

    if sauce_type == "mexican_no_sauce":

        print "mexican_no_sauce: sub foods"
        # for i in knowledge_base.mexican_to_italian_list:
        #     print i.food_in.name, i.food_out[0].name
        for sub in knowledge_base.mexican_to_italian_list:
            for e in range(len(made_recipe.ingredients)):
                if sub.food_in.name in made_recipe.ingredients[e].name.lower():
                    subbed_ingredient = made_recipe.ingredients[e].name.lower()
                    print "item to sub: " + subbed_ingredient
                    print "replace with: " + sub.food_out[0].name
                    made_recipe.ingredients[e] = sub.food_out[0]
                    made_recipe.replace_ingredient_in_steps(subbed_ingredient, sub.food_out[0].name)

        # for i in made_recipe.ingredients: print i.name
        for e in range(len(made_recipe.steps)): print made_recipe.steps[e]

        made_recipe.change_title("Italian " + made_recipe.title)


    if "asian" in sauce_type and "italian" in fusion_style:

        for sub in knowledge_base.asian_to_italian_list:
            for e in range(len(made_recipe.ingredients)):
                if sub.food_in.name in made_recipe.ingredients[e].name.lower():
                    subbed_ingredient = made_recipe.ingredients[e].name.lower()
                    print "item to sub: " + subbed_ingredient
                    print "replace with: " + sub.food_out[0].name
                    made_recipe.ingredients[e] = sub.food_out[0]
                    made_recipe.replace_ingredient_in_steps(subbed_ingredient, sub.food_out[0].name)

        for e in range(len(made_recipe.steps)): print made_recipe.steps[e]
        made_recipe.change_title("Italian " + made_recipe.title)

    return made_recipe

        # this isn't done at all.
        # for (ingredient, substitution) in kb.mexican_to_italian:




