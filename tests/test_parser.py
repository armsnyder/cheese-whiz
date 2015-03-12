import unittest
from app.parser import get_html


class TestAutograder(unittest.TestCase):

    @staticmethod
    def url_to_dictionary(url):
        """
        FOR TESTING PURPOSES ONLY, takes a url and runs the various parsing functions to return a dictionary in the JSON
        representation that Miriam's autograder accepts
        :param url: url of requested recipe
        :return: dictionary in autograder-acceptable format
        """
        # TODO: Write url_to_dictionary
        html = get_html(url)
        # etc
        return {}

    @staticmethod
    def parsed_recipe_similarity(dict_1, dict_2):
        """
        FOR TESTING PURPOSES ONLY, takes two parsed recipes, compares them using a distance metric, and returns
        similarity, represented as a number between 0 and 1
        :param dict_1: First parsed recipe
        :param dict_2: Second parsed recipe
        :return: Similarity (number between 0 and 1)
        """
        # TODO: Write parsed_recipe_similarity
        return 1

    def assertSimilarRecipe(self, dict_1, dict_2):
        """
        FOR TESTING PURPOSES ONLY, takes two parsed recipes and returns True if they are similar enough
        :param dict_1: First parsed recipe
        :param dict_2: Second parsed recipe
        :return: boolean
        """
        self.assertTrue(self.parsed_recipe_similarity(dict_1, dict_2) > 0.9)

    def test_1(self):
        result_dict = self.url_to_dictionary('allrecipes.com/Recipe/Easier-Chicken-Marsala')
        correct_dict = \
            {
                'ingredients': [
                    {
                        'name': 'flour',
                        'quantity': 0.25,
                        'measurement': 'cup',
                        'descriptor': 'all-purpose',
                        'preparation': 'none',
                        'prep-description': 'none'
                    },
                    {
                        'name': 'salt',
                        'quantity': 0.5,
                        'measurement': 'teaspoon',
                        'descriptor': 'garlic',
                        'preparation': 'none',
                        'prep-description': 'none'
                    },
                    {
                        'name': 'pepper',
                        'quantity': 0.25,
                        'measurement': 'teaspoon',
                        'descriptor': 'black',
                        'preparation': 'ground',
                        'prep-description': 'none'
                    },
                    {
                        'name': 'oregano',
                        'quantity': 0.5,
                        'measurement': 'teaspoon',
                        'descriptor': 'dried',
                        'preparation': 'none',
                        'prep-description': 'none'
                    },
                    {
                        'name': 'chicken breast halves',
                        'quantity': 4,
                        'measurement': 'none',
                        'descriptor': 'boneless, skinless',
                        'preparation': 'none',
                        'prep-description': 'none'
                    },
                    {
                        'name': 'olive oil',
                        'quantity': 1,
                        'measurement': 'tablespoon',
                        'descriptor': 'none',
                        'preparation': 'none',
                        'prep-description': 'none'
                    },
                    {
                        'name': 'butter',
                        'quantity': 1,
                        'measurement': 'tablespoon',
                        'descriptor': 'none',
                        'preparation': 'none',
                        'prep-description': 'none'
                    },
                    {
                        'name': 'mushrooms',
                        'quantity': 1,
                        'measurement': 'cup',
                        'descriptor': 'fresh',
                        'preparation': 'sliced',
                        'prep-description': 'none'
                    },
                    {
                        'name': 'wine',
                        'quantity': 0.5,
                        'measurement': 'cup',
                        'descriptor': 'Marsala',
                        'preparation': 'none',
                        'prep-description': 'none'
                    }
                ],
                'primary cooking method': 'fry',
                'cooking methods': ['stir', 'dredge', 'heat', 'fry', 'stir'],
                'cooking tools': ['medium bowl', 'large skillet']
            }
        self.assertSimilarRecipe(result_dict, correct_dict)

    def test_2(self):
        # etc
        pass