__author__ = 'pantsworth'


import unittest
from app.parser import parse_html
from app.parser import get_html
from app.cooking_tools import find_cooking_tools, find_cooking_methods



class TestParseHtml(unittest.TestCase):

    def test_parse_html(self):
        testhtml = get_html('http://allrecipes.com/recipe/worlds-best-lasagna/')
        testparse = parse_html(testhtml)
        find_cooking_tools(testparse[2])
        find_cooking_methods(testparse[2])