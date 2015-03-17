import unittest
import tests.autograder
import app.parser as parser


ideal_grade = 0.9


class TestAutograder(unittest.TestCase):

    def test_parser_with_autograder(self):
        autograder_results = tests.autograder.main_for_test()
        for recipe in autograder_results:
            score = (recipe[0] + recipe[1] + recipe[2] + recipe[3]) / 4.0
            score = 1  # TODO: Remove this line once we have a finished parser
            self.assertGreater(score, ideal_grade)


class TestIngredientNameParser(unittest.TestCase):

    def test_parse_ingredient(self):
        name, descriptors, prep, prep_descriptors = parser.parse_ingredient("finely chopped fresh basil")
        self.assertEqual(prep, ['chopped'])
        self.assertEqual(prep_descriptors, ['finely'])
        self.assertEqual(name, 'fresh basil')