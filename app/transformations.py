import recipe
from enums import FoodGroup


def to_vegan(knowledge_base, from_recipe):
    """
    Takes a Recipe input and output vegan Recipe.
    First, fun the to_vegetarian function.
    Loop through ingredients, checking food group (look in enums.py) for no-no groups. If the ingredient is of
    a no-no-group, check for a substitution in kb.vegan_substitutions (not yet written). If no suitable substitution
    can be found, replace with a quantity of TVP of equal weight.
    :param from_recipe: knowledge_base, old recipe
    :return: new recipe
    """
    veg_recipe = to_vegetarian(knowledge_base, from_recipe)

    for ingredient in veg_recipe.ingredients:
        if ingredient.food_type.food_group == FoodGroup.DAIRY_AND_EGG_PRODUCTS:
            found = False
            # Look for substitution in kb.vegan_substitutes
            for name, substitution in knowledge_base.vegan_substitutions:
                if name == ingredient.name:
                    vegan_ingredient = substitution
                    found = True
            if not found:
                vegan_ingredient = 'textured vegetable protein'
            recipe.ingredients.append(vegan_ingredient)
        else:
            recipe.ingredients.append(ingredient)

    return recipe.Recipe()


def to_vegetarian(knowledge_base, from_recipe):
    """
    Takes a Recipe input and output vegetarian Recipe.
    Loop through ingredients, checking food group (look in enums.py) for no-no groups. If the ingredient is of a
    no-no-group, check for a substitution in kb.vegetarian_substitutions (not yet written). If no suitable substitution
    can be found, replace with a quantity of TVP of equal weight.
    :param from_recipe: knowledge_base, old recipe
    :return: new recipe
    """
    for ingredient in from_recipe.ingredients:
        if ingredient.food_type.food_group in (FoodGroup.POULTRY_PRODUCTS, FoodGroup.SAUSAGES_AND_LUNCHEON_MEATS,
                                               FoodGroup.PORK_PRODUCTS, FoodGroup.BEEF_PRODUCTS,
                                               FoodGroup.FINFISH_AND_SHELLFISH_PRODUCTS,
                                               FoodGroup.LAMB_VEAL_AND_GAME_PRODUCTS):
            # Look for substitution in kb.vegetarian_substitutes
            for name, substitution in knowledge_base.vegetarian_substitutions:
                found = False
                if name == ingredient.name:
                    veg_ingredient = substitution
                    found = True
            if not found:
                veg_ingredient = 'textured vegetable protein'
            recipe.ingredients.append(veg_ingredient)
        else:
            recipe.ingredients.append(ingredient)

    return recipe.Recipe()


def make_healthy(from_recipe):
    """
    STUB DESCRIPTION:
    Write make_healthy function to take a Recipe input and output a healthier Recipe.
    Loop through Ingredients in Recipe, and apply USDA lookup function from #62.
    Think of other ways also.
    :param from_recipe: old recipe
    :return: new recipe
    """
    return recipe.Recipe()  # Stub


def make_unhealthy(from_recipe):
    """
    STUB DESCRIPTION:
    Take a Recipe input, and return a Recipe that has been made unhealthy.
    For each Ingredient in the Recipe, query the USDA database for similar foods, and choose the least healthy alternative.
    If no changes can be found, add Cheese Whiz.
    :param from_recipe: old recipe
    :return: new recipe
    """
    return recipe.Recipe()  # Stub


def lookup_healthy_ingredient(from_ingredient):
    """
    STUB DESCRIPTION:
    Write a function that takes an Ingredient input and outputs a healthier Ingredient, using simple search terms
    like "low fat," if it finds one in the USDA. If no result is found, return None.
    :param from_ingredient:
    :return: Ingredient, or None
    """
    return recipe.Ingredient()  # Stub


def lookup_alternative_recipe(from_recipe, unavailable_ingredient_list):
    """
    STUB DESCRIPTION:
    Write lookup_alternative_recipe function to take args: Recipe, list of unavailable Ingredients
    (returned from transform_availability #60)
    It should query allrecipes.com using the advanced search to specify the recipe title and missing ingredients.
    If helper functions are needed, write them as stubs and make new issues for them.
    :param from_recipe: old recipe
    :param unavailable_ingredient_list: unavailable ingredients list
    :return: new recipe URL
    """
    return 'url'  # Stub


def transform_availability(old_recipe, old_ingredient):
    """
    STUB DESCRIPTION:
    Write transform_availability function to take an Ingredient argument and return a list of Ingredient objects
    that are possible substitutions, complete with quantity info.
    First check our knowledge base for common substitutions, then move on to using nutritional data / food group to
    find suitable alternatives.
    Make new issues for any useful helper functions.
    :param old_recipe: recipe containing ingredient
    :param old_ingredient: ingredient to transform
    :return: list of possible substitution Ingredient objects
    """
    possible_substitutions = []
    return possible_substitutions


def transform_style(old_recipe, target_style):
    """
    STUB DESCRIPTION:
    Write transform_style function to take a recipe and a target style as inputs and output another recipe object
    (in the desired style).
    Loop through the ingredients in the recipe. For each ingredient, check if it exists in the knowledge base style
    transform list for the desired style. If it does, make the exchange.
    The tricky bit will be finding the correct Food object to substitute in from the USDA database.
    Feel free to think up helper functions, write stubs, and make new issues for them.
    :param old_recipe: recipe
    :param target_style: style string
    :return: new recipe
    """
    return recipe.Recipe()  # Stub
