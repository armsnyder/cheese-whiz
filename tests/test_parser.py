import unittest
import tests.autograder
import app.parser as parser
from app.parser import parse_ingredient
import app.app
from app.recipe import Ingredient


ideal_grade = 0.9


class TestAutograder(unittest.TestCase):

    def test_parser_with_autograder(self):
        autograder_results = tests.autograder.main_for_test()
        for recipe in autograder_results:
            score = (recipe[0] + recipe[1] + recipe[2] + recipe[3]) / 4.0
            print 'Scored: %s %s %s %s' % (recipe[0], recipe[1], recipe[2], recipe[3])
            # self.assertGreater(score, ideal_grade)


class TestIngredientNameParser(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.knowledge_base = app.app.load_knowledge_base()

    def test_parse_3(self):
        name, descriptors, prep, prep_descriptors = parse_ingredient("butter", self.knowledge_base)
        self.assertEqual(descriptors, 'none')
        self.assertEqual(prep, 'none')
        self.assertEqual(prep_descriptors, 'none')
        self.assertEqual(name, 'butter')

    def test_parse_5(self):
        name, descriptors, prep, prep_descriptors = parse_ingredient("minced garlic", self.knowledge_base)
        self.assertEqual(descriptors, 'none')
        self.assertEqual(prep, 'minced')
        self.assertEqual(prep_descriptors, 'none')
        self.assertEqual(name, 'garlic')

    def test_parse_6(self):
        name, descriptors, prep, prep_descriptors = parse_ingredient("soy sauce", self.knowledge_base)
        self.assertEqual(descriptors, 'none')
        self.assertEqual(prep, 'none')
        self.assertEqual(prep_descriptors, 'none')
        self.assertEqual(name, 'soy sauce')

    def test_parse_1(self):
        name, descriptors, prep, prep_descriptors = parser.parse_ingredient("Mustard, Ground", self.knowledge_base)
        self.assertEqual(descriptors, 'none')
        self.assertEqual(prep, 'none')
        self.assertEqual(prep_descriptors, 'none')
        self.assertEqual(name, 'ground mustard')

    def test_parse_2(self):
        name, descriptors, prep, prep_descriptors = parse_ingredient("finely chopped basil", self.knowledge_base)
        self.assertEqual(descriptors, 'none')
        self.assertEqual(prep, 'chopped')
        self.assertEqual(prep_descriptors, 'finely')
        self.assertEqual(name, 'basil')

    def test_parse_4(self):
        name, descriptors, prep, prep_descriptors = parse_ingredient("Black Pepper, Ground", self.knowledge_base)
        self.assertEqual(descriptors, 'ground')
        self.assertEqual(prep, 'none')
        self.assertEqual(prep_descriptors, 'none')
        self.assertEqual(name, 'black pepper')

    def test_parse_7(self):
        name, descriptors, prep, prep_descriptors = parse_ingredient("boneless chicken thighs, with skin", self.knowledge_base)
        self.assertTrue('boneless' in descriptors and 'with skin' in descriptors)
        self.assertEqual(prep, 'none')
        self.assertEqual(prep_descriptors, 'none')
        self.assertEqual(name, 'chicken thighs')



    # def test_parse_ingredient(self):
    #     name, descriptors, prep, prep_descriptors = parser.parse_ingredient("finely chopped fresh basil", self.knowledge_base)
    #     self.assertEqual(descriptors, 'none')
    #     self.assertEqual(prep, 'chopped')
    #     self.assertEqual(prep_descriptors, 'finely')
    #     self.assertEqual(name, 'fresh basil')
    #
    # def test_parse_ingredient_huh(self):
    #     name, descriptors, prep, prep_descriptors = parser.parse_ingredient("finely chopped fresh spaghetti", self.knowledge_base)
    #     self.assertEqual(descriptors, 'fresh')
    #     self.assertEqual(prep, 'chopped')
    #     self.assertEqual(prep_descriptors, 'finely')
    #     self.assertEqual(name, 'spaghetti')
    #
    # def test_parse_with_commas(self):
    #     name, descriptors, prep, prep_descriptors = parser.parse_ingredient("boneless, skinless chicken, washed and dried", self.knowledge_base)
    #     self.assertEqual(descriptors, 'boneless skinless')
    #     self.assertEqual(prep, 'washed dried')
    #     self.assertEqual(prep_descriptors, 'none')
    #     self.assertEqual(name, 'chicken')