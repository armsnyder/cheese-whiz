# Any tests that require a fully loaded knowledge base should go here since the loading takes time

import unittest
from app.recipe import Ingredient
from app.kb import KnowledgeBase


class TestOnLoadedKB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.kb = KnowledgeBase()
        cls.kb.load()

    def test_match_food_name_and_description(self):
        self.assertEqual(Ingredient('olive oil').match_to_food(self.kb).food_type.food_id, '04053')
        self.assertEqual(Ingredient('basil', descriptor='fresh').match_to_food(self.kb).food_type.food_id, '02044')
        self.assertEqual(Ingredient('basil', descriptor='dried').match_to_food(self.kb).food_type.food_id, '02003')
        self.assertEqual(Ingredient('butter', descriptor='salted').match_to_food(self.kb).food_type.food_id, '01001')
        self.assertEqual(Ingredient('garlic', preparation='crushed').match_to_food(self.kb).food_type.food_id, '11215')
        self.assertEqual(Ingredient('garlic powder').match_to_food(self.kb).food_type.food_id, '02020')
        self.assertEqual(Ingredient('graham cracker crust', descriptor='prepared')
                         .match_to_food(self.kb).food_type.food_id, '18399')
        self.assertEqual(Ingredient('condensed milk', descriptor='sweetened')
                         .match_to_food(self.kb).food_type.food_id, '01095')

    def test_match_food_name_only(self):
        self.assertEqual(Ingredient('butter').match_to_food(self.kb).food_type.food_id, '01001')
        self.assertEqual(Ingredient('sour cream').match_to_food(self.kb).food_type.food_id, '01179')
        self.assertEqual(Ingredient('egg').match_to_food(self.kb).food_type.food_id, '01123')
        self.assertEqual(Ingredient('flour').match_to_food(self.kb).food_type.food_id, '20081')

    def test_match_food_special_cases(self):
        self.assertEqual(Ingredient('beef', descriptor='ground').match_to_food(self.kb).food_type.food_id, '23567')
        self.assertEqual(Ingredient('onion', preparation='chopped').match_to_food(self.kb).food_type.food_id, '11282')
        self.assertEqual(Ingredient('ketchup').match_to_food(self.kb).food_type.food_id, '11935')
        self.assertEqual(Ingredient('flour').match_to_food(self.kb).food_type.food_id, '20081')
        self.assertEqual(Ingredient('water').match_to_food(self.kb).food_type.food_id, '14411')

    def test_match_food_none(self):
        self.assertEqual(Ingredient('asdfgph').match_to_food(self.kb).food_type, None)
        self.assertEqual(Ingredient('lime zest').match_to_food(self.kb).food_type, None)