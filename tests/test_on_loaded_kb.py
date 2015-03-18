# Any tests that require a fully loaded knowledge base should go here since the loading takes time

import unittest
from app.parser import url_to_recipe
from app.cooking_tools import find_cooking_tools, find_cooking_methods
from app.style_fusions import classify_recipe
from app.style_fusions import recipe_fusion
# from app.style_fusions import testing_recipe
from app.parser import parse_ingredient
from app.recipe import Recipe, Ingredient
from app.transformations import to_vegan
import app.app
from app.transformations import to_vegetarian


class TestOnLoadedKB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.kb = app.app.load_knowledge_base()

    # def test_match_food_name_and_description(self):
    #     self.assertEqual(Ingredient('olive oil').match_to_food(self.kb).food_type.food_id, '04053')
    #     self.assertEqual(Ingredient('basil', descriptor='fresh').match_to_food(self.kb).food_type.food_id, '02044')
    #     self.assertEqual(Ingredient('basil', descriptor='dried').match_to_food(self.kb).food_type.food_id, '02003')
    #     self.assertEqual(Ingredient('butter', descriptor='salted').match_to_food(self.kb).food_type.food_id, '01001')
    #     self.assertEqual(Ingredient('garlic', preparation='crushed').match_to_food(self.kb).food_type.food_id, '11215')
    #     self.assertEqual(Ingredient('garlic powder').match_to_food(self.kb).food_type.food_id, '02020')
    #     self.assertEqual(Ingredient('graham cracker crust', descriptor='prepared')
    #                      .match_to_food(self.kb).food_type.food_id, '18399')
    #     self.assertEqual(Ingredient('condensed milk', descriptor='sweetened')
    #                      .match_to_food(self.kb).food_type.food_id, '01095')
    #
    # def test_match_food_name_only(self):
    #     self.assertEqual(Ingredient('butter').match_to_food(self.kb).food_type.food_id, '01001')
    #     self.assertEqual(Ingredient('sour cream').match_to_food(self.kb).food_type.food_id, '01179')
    #     self.assertEqual(Ingredient('egg').match_to_food(self.kb).food_type.food_id, '01123')
    #
    # def test_match_food_special_cases(self):
    #     self.assertEqual(Ingredient('beef', descriptor='ground').match_to_food(self.kb).food_type.food_id, '23567')
    #     self.assertEqual(Ingredient('onion', preparation='chopped').match_to_food(self.kb).food_type.food_id, '11282')
    #     self.assertEqual(Ingredient('ketchup').match_to_food(self.kb).food_type.food_id, '11935')
    #     self.assertEqual(Ingredient('flour').match_to_food(self.kb).food_type.food_id, '20081')
    #     self.assertEqual(Ingredient('water').match_to_food(self.kb).food_type.food_id, '14411')



    def test_fusion(self):
        made_recipe = url_to_recipe('http://allrecipes.com/Recipe/Mild-Cheesy-Chicken-Enchiladas/', self.kb)
        print "\n", made_recipe.title
        recipe_fusion(made_recipe, "to_italian", self.kb)


        made_recipe = url_to_recipe('http://allrecipes.com/Recipe/Salsa-Chicken/', self.kb)
        print "\n", made_recipe.title
        recipe_fusion(made_recipe, "to_italian", self.kb)

        made_recipe = url_to_recipe('http://allrecipes.com/recipe/chicken-enchiladas-i/', self.kb)
        print "\n", made_recipe.title
        recipe_fusion(made_recipe, "to_italian", self.kb)


        # testhtml = get_html('http://allrecipes.com/Recipe/Chicken-Enchiladas-II/')
        # print made_recipe.title

        # testparse = parse_html(testhtml)
        # spice_classify(testparse, self.kb)
        # print "italian to asian"
        # print self.kb.italian_to_asian_list

    # def test_match_food_none(self):
    #     self.assertEqual(Ingredient('asdfgph').match_to_food(self.kb).food_type, None)
    #     self.assertEqual(Ingredient('lime zest').match_to_food(self.kb).food_type, None)




    # def test_match_food_none(self):
    #     self.assertEqual(Ingredient('asdfgph').match_to_food(self.kb).food_type, None)
    #     self.assertEqual(Ingredient('lime zest').match_to_food(self.kb).food_type, None)
    #
    # def test_parse_ingredient(self):
    #     name, descriptors, prep, prep_descriptors = parse_ingredient("finely chopped fresh basil", self.kb)
    #     self.assertEqual(descriptors, 'none')
    #     self.assertEqual(prep, 'chopped')
    #     self.assertEqual(prep_descriptors, 'finely')
    #     self.assertEqual(name, 'fresh basil')
    #
    # def test_parse_ingredient_huh(self):
    #     name, descriptors, prep, prep_descriptors = parse_ingredient("finely chopped fresh spaghetti", self.kb)
    #     self.assertEqual(descriptors, 'fresh')
    #     self.assertEqual(prep, 'chopped')
    #     self.assertEqual(prep_descriptors, 'finely')
    #     self.assertEqual(name, 'spaghetti')
    #
    # def test_parse_ingredient_with_commas(self):
    #     name, descriptors, prep, prep_descriptors = parse_ingredient("boneless, skinless chicken, washed and dried", self.kb)
    #     self.assertEqual(descriptors, 'boneless skinless')
    #     self.assertEqual(prep, 'washed dried')
    #     self.assertEqual(prep_descriptors, 'none')
    #     self.assertEqual(name, 'chicken')
        
    # def test_veg(self):
    #     input_recipe = Recipe()
    #     i1 = Ingredient('beef', 1, 'raw', 'ground', 'finely', True, None)
    #     i2 = Ingredient('lettuce', 1, 'raw', '', '', True, None)
    #     i3 = Ingredient('milk', 1, 'warm', '', '', True, None)
    #
    #     i1.match_to_food(self.kb)
    #     i2.match_to_food(self.kb)
    #     i3.match_to_food(self.kb)
    #
    #     input_recipe.add_ingredients([i1, i2, i3])
    #
    #     to_vegan(self.kb, input_recipe)
    def test_veg(self):
        input_recipe = Recipe()
        i1 = Ingredient('beef', 1, 'raw', 'ground', 'finely', True, None)
        i2 = Ingredient('lettuce', 1, 'raw', '', '', True, None)
        i3 = Ingredient('milk', 1, 'warm', '', '', True, None)

        i1.match_to_food(self.kb)
        i2.match_to_food(self.kb)
        i3.match_to_food(self.kb)

        input_recipe.add_ingredients([i1, i2, i3])

        to_vegetarian(self.kb, input_recipe)

    def test_vegan(self):
        input_recipe = Recipe()
        i1 = Ingredient('beef', 1, 'raw', 'ground', 'finely', True, None)
        i2 = Ingredient('lettuce', 1, 'raw', '', '', True, None)
        i3 = Ingredient('milk', 1, 'warm', '', '', True, None)

        i1.match_to_food(self.kb)
        i2.match_to_food(self.kb)
        i3.match_to_food(self.kb)

        input_recipe.add_ingredients([i1, i2, i3])

        to_vegan(self.kb, input_recipe)
