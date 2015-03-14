import unittest
import os

import app.kb as kb
import app.util as util
import app.recipe as recipe

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
        self.assertRaises(RuntimeError, food.add_styles, ['a', 'b'], ['b', 'c'])

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
        self.assertEqual(quantity.amount, 27)
        self.assertEqual(quantity.unit, 'unit')


class TestIngredientLookup(unittest.TestCase):

    def setUp(self):
        food_names = \
            [
                'Butter, salted',
                'Butter, whipped, with salt',
                'Butter oil, anhydrous',
                'Cheese, blue',
                'Cheese, brick',
                'Cheese, brie',
                'Cheese, camembert'
                'Cheese, cottage, creamed, large or small curd',
                'Cheese, cottage, creamed, with fruit',
                'Cheese, cottage, nonfat, uncreamed, dry, large or small curd',
                'Cheese, cottage, lowfat, 2% milkfat',
                'Cheese, cottage, lowfat, 1% milkfat',
                'Basil, fresh',
                'Spices, basil, dried',
                "CAMPBELL'S Homestyle Harvest Tomato with Basil Soup",
                'PREGO Pasta, Organic Tomato and Basil Italian Sauce, ready-to-serve',
                'PREGO Pasta, Tomato, Basil and Garlic Italian Sauce, ready-to-serve',
                'MORNINGSTAR FARMS Tomato & Basil Pizza Burger, frozen, unprepared',
                'GARDENBURGER Sun-Dried Tomato Basil Burger, frozen, unprepared'
            ]
        self.kb = kb.KnowledgeBase()
        self.kb.foods = [kb.Food(None, None, name) for name in food_names]

    def test_basil(self):
        self.kb._add_style_tags('basil', ['italian'], [])
        affected_items = [food for food in self.kb.foods if food.positive_tags == ['italian']]
        self.assertEqual(len(affected_items), 7)

    def test_cheese(self):
        correct_cheese_list = \
            [
                'Cheese, blue',
                'Cheese, brick',
                'Cheese, brie',
                'Cheese, camembert'
                'Cheese, cottage, creamed, large or small curd',
                'Cheese, cottage, creamed, with fruit',
                'Cheese, cottage, nonfat, uncreamed, dry, large or small curd',
                'Cheese, cottage, lowfat, 2% milkfat',
                'Cheese, cottage, lowfat, 1% milkfat'

            ]
        test_cheese_list = [food.name for food in self.kb.lookup_food('cheese')]
        self.assertEqual(test_cheese_list, correct_cheese_list)

    def test_lowfat_cheese(self):
        correct_cheese_list = \
            [
                'Cheese, cottage, lowfat, 2% milkfat',
                'Cheese, cottage, lowfat, 1% milkfat'
            ]
        test_cheese_list = [food.name for food in self.kb.lookup_food('lowfat cheese')]
        self.assertEqual(test_cheese_list, correct_cheese_list)


class TestFractionToDecimal(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(util.fraction_to_decimal('1'), 1)
        self.assertEqual(util.fraction_to_decimal('1.5'), 1.5)
        self.assertEqual(util.fraction_to_decimal('1/2'), 0.5)
        self.assertEqual(util.fraction_to_decimal('a'), 1)
        self.assertEqual(util.fraction_to_decimal('3 cups'), 1)


class TestSubstitutionParser(unittest.TestCase):

    def test_substitutions(self):
        knowledge_base = kb.KnowledgeBase()
        knowledge_base._load_measurements()
        a = kb.KnowledgeBase._format_raw_sub(knowledge_base, '1 cup  Beer', '1 cup nonalcoholic beer OR 1 cup chicken broth')
        i1 = recipe.Ingredient('beer', quantity=kb.Quantity(1, 'cup'))
        i2 = recipe.Ingredient('nonalcoholic beer', quantity=kb.Quantity(1, 'cup'))
        i3 = recipe.Ingredient('chicken broth', quantity=kb.Quantity(1, 'cup'))
        b = kb.CommonSubstitution(i1, [i2, i3])
        self.assertSameSubObj(a, b)

    def assertSameSubObj(self, so1, so2):
        self.assertEqual(so1.food_in.name, so2.food_in.name)
        self.assertEqual(so1.food_in.quantity.amount, so2.food_in.quantity.amount)
        self.assertEqual(so1.food_in.quantity.unit, so2.food_in.quantity.unit)
        self.assertEqual(so1.food_in.preparation, so2.food_in.preparation)

        if len(so1.food_out) == len(so2.food_out):
            for i in range(len(so1.food_out)):
                self.assertEqual(so1.food_out[i].name, so2.food_out[i].name)
                self.assertEqual(so1.food_out[i].quantity.amount, so2.food_out[i].quantity.amount)
                self.assertEqual(so1.food_out[i].quantity.unit, so2.food_out[i].quantity.unit)
                self.assertEqual(so1.food_out[i].preparation, so2.food_out[i].preparation)
        self.assertEqual(test_cheese_list, correct_cheese_list)


class TestFractionToDecimal(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(util.fraction_to_decimal('1'), 1)
        self.assertEqual(util.fraction_to_decimal('1.5'), 1.5)
        self.assertEqual(util.fraction_to_decimal('1/2'), 0.5)
        self.assertEqual(util.fraction_to_decimal('a'), 1)
        self.assertEqual(util.fraction_to_decimal('3 cups'), 1)