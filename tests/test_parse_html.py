__author__ = 'pantsworth'


import unittest
from app.parser import parse_html
from app.parser import get_html
from app.style_fusions import spice_classify

class TestParseHtml(unittest.TestCase):

    def test_italian(self):
        testhtml = get_html('http://allrecipes.com/recipe/worlds-best-lasagna/')
        testparse = parse_html(testhtml)
        spice_classify(testparse)

        testhtml = get_html('http://allrecipes.com/recipe/chicken-fettuccini-alfredo/')
        testparse = parse_html(testhtml)
        spice_classify(testparse)
        #
        # testhtml = get_html('http://allrecipes.com/recipe/to-die-for-fettuccine-alfredo/')
        # testparse = parse_html(testhtml)
        # spice_classify(testparse)


    def test_mexican(self):

        testhtml = get_html('http://allrecipes.com/Recipe/Chicken-Enchiladas-II/')
        testparse = parse_html(testhtml)
        spice_classify(testparse)


    def test_neutral(self):
        testhtml = get_html('http://allrecipes.com/Recipe/Baked-Lemon-Chicken-with-Mushroom-Sauce/')
        testparse = parse_html(testhtml)
        spice_classify(testparse)

    def test_east_asian(self):
        testhtml = get_html('http://allrecipes.com/Recipe/Baked-Teriyaki-Chicken/')
        testparse = parse_html(testhtml)
        spice_classify(testparse)

        testhtml = get_html('http://allrecipes.com/Recipe/Thai-Orange-Chicken/')
        testparse = parse_html(testhtml)
        spice_classify(testparse)

        testhtml = get_html('http://allrecipes.com/recipe/restaurant-style-beef-and-broccoli/')
        testparse = parse_html(testhtml)
        spice_classify(testparse)

        testhtml = get_html('http://allrecipes.com/Recipe/Sesame-Chicken/')
        testparse = parse_html(testhtml)
        spice_classify(testparse)


