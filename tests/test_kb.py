import unittest
import os

import app.kb as kb
import app.util as util

__author__ = 'flame'


class TestStringToNumber(unittest.TestCase):

    def test_int(self):
        self.assertEqual(kb.string_to_number('1'), 1)
        self.assertEqual(kb.string_to_number('2'), 2)
        self.assertEqual(kb.string_to_number('0'), 0)
        self.assertEqual(kb.string_to_number(1), 1)
        self.assertEqual(kb.string_to_number(2), 2)

    def test_float(self):
        self.assertEqual(kb.string_to_number('1.1'), 1.1)
        self.assertEqual(kb.string_to_number('2.5'), 2.5)
        self.assertEqual(kb.string_to_number('0.0'), 0.0)
        self.assertEqual(kb.string_to_number(1.1), 1.1)
        self.assertEqual(kb.string_to_number(2.5), 2.5)

    def test_string(self):
        self.assertEqual(kb.string_to_number('abc'), 'abc')
        self.assertEqual(kb.string_to_number('abc1'), 'abc1')
        self.assertEqual(kb.string_to_number('1abc'), '1abc')
        self.assertEqual(kb.string_to_number('2b'), '2b')
        self.assertEqual(kb.string_to_number(''), '')


class TestReadTxtLinesIntoArray(unittest.TestCase):

    def setUp(self):
        test_text_1 = \
            "# some comment\n" \
            "#another comment\n" \
            "\n" \
            "this is a line\n" \
            "\n" \
            "this is ANOTHER line\n" \
            "\n" \
            "#comment###\n" \
            "\n" \
            " \n" \
            "\n"
        with open(util.relative_path('test_file.txt'), 'w') as f:
            f.write(test_text_1)

    def test_example_len(self):
        result = kb.read_txt_lines_into_list('test_file.txt')
        self.assertEqual(len(result), 3)

    def test_example_content(self):
        result = kb.read_txt_lines_into_list('test_file.txt')
        self.assertEqual(result[0], 'this is a line')
        self.assertEqual(result[1], 'this is another line')
        self.assertEqual(result[2], ' ')

    def tearDown(self):
        os.remove(util.relative_path('test_file.txt'))


class TestParseUsdaLine(unittest.TestCase):

    def test_parse_usda(self):
        self.assertEqual(kb.parse_usda_line(''), [])
        self.assertEqual(kb.parse_usda_line('\n'), [])
        self.assertEqual(kb.parse_usda_line(' \n'), [' '])
        self.assertEqual(kb.parse_usda_line('1\n'), [1])
        self.assertEqual(kb.parse_usda_line('~1~\n'), ['1'])
        self.assertEqual(kb.parse_usda_line('1^2\n'), [1, 2])
        self.assertEqual(kb.parse_usda_line('1^2^3^\n'), [1, 2, 3, ''])
        self.assertEqual(kb.parse_usda_line('^1^2^3\n'), ['', 1, 2, 3])
        self.assertEqual(kb.parse_usda_line('^1^2^3^\n'), ['', 1, 2, 3, ''])
        self.assertEqual(kb.parse_usda_line('1^^2^3^^^4\n'), [1, '', 2, 3, '', '', 4])
        self.assertEqual(
            kb.parse_usda_line('~01011~^~0100~^~Cheese, colby~^~CHEESE,COLBY~^~~^~~^~Y~^~~^0^~~^6.38^4.27^8.79^3.87\n'),
            ['01011', '0100', 'Cheese, colby', 'CHEESE,COLBY', '', '', 'Y', '', 0, '', 6.38, 4.27, 8.79, 3.87])


class TestAddStyles(unittest.TestCase):

    def test_empty_add(self):
        food = kb.Food()
        food.add_styles([], [])
        self.assertEqual(food.positive_tags, [])
        self.assertEqual(food.negative_tags, [])

    def test_no_duplicates(self):
        food = kb.Food()
        food.add_styles(['a'], ['b'])
        self.assertEqual(food.positive_tags, ['a'])
        self.assertEqual(food.negative_tags, ['b'])

    def test_duplicates_same_category(self):
        food = kb.Food()
        food.add_styles(['a', 'a', 'b'], ['c', 'c'])
        self.assertEqual(food.positive_tags, ['a', 'b'])
        self.assertEqual(food.negative_tags, ['c'])

    def test_duplicates_different_category(self):
        food = kb.Food()
        self.assertRaises(RuntimeError, food.add_styles, ['a','b'], ['b', 'c'])

    def test_duplicates_iterative_add(self):
        food = kb.Food()
        food.add_styles(['a'], [])
        food.add_styles(['a'], [])
        self.assertEqual(food.positive_tags, ['a'])
        self.assertEqual(food.negative_tags, [])


class TestQuantityInterpreter(unittest.TestCase):

    def test_quantity_interpreter(self):
        knowledge_base = kb.KnowledgeBase()
        knowledge_base._load_measurements()

        quantity = knowledge_base.interpret_quantity('1/4 cup')
        self.assertEqual(quantity.amount, 0.25)
        self.assertEqual(quantity.unit, 'cup')

        quantity = knowledge_base.interpret_quantity('27 salamanders')
        self.assertEqual(quantity.amount, '27')
        self.assertEqual(quantity.unit, 'unit')


