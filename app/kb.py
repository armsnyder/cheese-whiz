# All code relating to the system's knowledge base goes here
# The KnowledgeBase class contains the data itself
# All other methods are just useful helper functions
# TODO: We should decide definitively how to represent preparation_terms and preparation_descriptors

from compiler.ast import flatten

from enums import Nutrient
from enums import FoodGroup
import util


class KnowledgeBase:
    def __init__(self):
        self.foods = []
        self.preparation_terms = set()
        self.preparation_descriptors = set()  # TODO: Is it ok that this is just a separate list?
        self.cooking_wares = set()
        self.measurements = {}
        self.common_substitutions = []

    def load(self):
        """
        Loads parsed knowledge base data from modifiable data text files into global fields
        Typically called right after object initialization
        """
        self.__load_foods()
        util.vprint('Loading cooking terminology')
        self.__load_preparation_terms()
        self.__load_preparation_descriptors()
        self.__load_cooking_wares()
        self.__load_measurements()
        self.__load_common_substitutions()
        util.vprint('Finished loading:')
        util.vprint('\t%s foods' % str(len(self.foods)))
        util.vprint('\t%s preparation terms' % str(len(self.preparation_terms)))
        util.vprint('\t%s preparation descriptors' % str(len(self.preparation_descriptors)))
        util.vprint('\t%s cooking wares' % str(len(self.cooking_wares)))
        util.vprint('\t%s measurements' % str(len(self.measurements)))
        util.vprint('\t%s common substitutions' % str(len(self.common_substitutions)))

    def __load_foods(self):
        util.vprint('Loading nutrient data')
        nutritional_data = self.__load_nutritional_data()
        util.vprint('Loading food data')
        with open(util.relative_path('kb_data/sr27asc/FOOD_DES.txt')) as food_des_txt:
            food_des_lines = food_des_txt.readlines()
            for food_des_line in food_des_lines:
                parsed_line = parse_usda_line(food_des_line)
                new_food = Food(parsed_line[0], parsed_line[1], parsed_line[2])
                if new_food.food_group in food_group_blacklist:
                    continue
                if new_food.food_id in food_id_blacklist:
                    continue
                if new_food.food_id in nutritional_data:
                    new_food.nutritional_data = nutritional_data[new_food.food_id]
                self.foods.append(new_food)

    def __load_preparation_terms(self):
        self.preparation_terms = set(read_txt_lines_into_list('kb_data/preparation_terms.txt'))

    def __load_preparation_descriptors(self):
        self.preparation_descriptors = set(read_txt_lines_into_list('kb_data/preparation_descriptors.txt'))

    def __load_cooking_wares(self):
        self.cooking_wares = set(read_txt_lines_into_list('kb_data/cooking_wares.txt'))

    def __load_measurements(self):
        raw_measurement_list = read_txt_lines_into_list('kb_data/measurements.txt')
        for raw_measurement in raw_measurement_list:
            parsed_in_out = raw_measurement.split('=')
            full_name = parsed_in_out[0]
            abbreviations = parsed_in_out[1]
            if len(parsed_in_out) != 2:
                util.warning('Incorrect substitution string: ' + raw_measurement)
                continue
            abbreviation_list = abbreviations.split(',')
            if not len(abbreviation_list):
                util.warning('Incorrect substitution string: ' + raw_measurement)
                continue
            self.measurements[full_name] = abbreviation_list

    def __load_common_substitutions(self):
        raw_sub_list = read_txt_lines_into_list('kb_data/common_substitutions.txt')
        for raw_sub in raw_sub_list:
            parsed_in_out = raw_sub.split('=')
            if len(parsed_in_out) != 2:
                util.warning('Incorrect substitution string: ' + raw_sub)
                continue
            self.common_substitutions.append(self.__format_raw_sub(parsed_in_out[0], parsed_in_out[1]))

    @staticmethod
    def __format_raw_sub(raw_food_in, raw_food_out):
        # TODO: Write this function. It should output a complete CommonSubstitution object.
        food_in = raw_food_in
        food_out = raw_food_out
        return CommonSubstitution(food_in, food_out)

    @staticmethod
    def __load_nutritional_data():
        result = {}
        with open(util.relative_path('kb_data/sr27asc/NUT_DATA.txt')) as nut_data_txt:
            nut_data_lines = nut_data_txt.readlines()
            for nut_data_line in nut_data_lines:
                parsed_line = parse_usda_line(nut_data_line)
                food_id = parsed_line[0]
                nut_id = parsed_line[1]
                nut_data = parsed_line[2:]
                if nut_id not in nutritional_data_whitelist:
                    continue
                if food_id not in result:
                    result[food_id] = {}
                result[food_id][nut_id] = nut_data
        return result


class Food:
    def __init__(self, food_id=None, food_group=None, name=None, nutritional_data=None):
        self.food_id = food_id
        self.food_group = food_group
        self.name = name
        self.nutritional_data = nutritional_data
        self.positive_tags = []
        self.negative_tags = []


class CommonSubstitution:
    def __init__(self, food_in=None, food_out=None):
        self.food_in = food_in
        self.food_out = food_out


class FoodQuantity:
    def __init__(self, name=None, quantity=None):
        self.name = name
        self.quantity = quantity


class Quantity:
    def __init__(self, amount=None, unit=None):
        self.amount = amount
        self.unit = unit


def read_txt_lines_into_list(file_name):
    """
    Given a filename, returns a list with each cell being a line from the file
    Lines that have no content or begin with a '#' (comments) are skipped
    Converts to lowercase
    :param file_name: filename of source
    :return: list of file lines
    """
    result = []
    with open(util.relative_path(file_name)) as source_file:
        source_lines = source_file.readlines()
        for line in source_lines:
            if len(line) and line[-1] == '\n':
                line = line[:-1]
            if len(line) and line[0] != '#':
                result.append(line.lower())
    return result


def parse_usda_line(text):
    """
    Parses USDA database text format into a list
    :param text: raw database text
    :return: list
    """
    if len(text) and text[-1] == '\n':
        text = text[:-1]
    if not len(text):
        return []
    result = text.split('^')
    for i in range(len(result)):
        if len(result[i]) and result[i][0] == '~':
            result[i] = result[i][1:-1]
        else:
            result[i] = string_to_number(result[i])
    return result


def string_to_number(string):
    """
    Attempts to transform a string into a number
    :param string: string to be cast to number
    :return: number representation of string
    """
    try:
        string_float = float(string)
    except ValueError:
        return string
    try:
        string_int = int(string)
    except ValueError:
        return string_float
    if string_int == string_float:
        return string_int
    return string_float


nutritional_data_whitelist = \
    [
        Nutrient.PROTEIN,
        Nutrient.FAT,
        Nutrient.STARCH,
        Nutrient.WATER,
        Nutrient.SUGAR,
        Nutrient.FIBER
    ]

food_group_blacklist = \
    [
        FoodGroup.BABY_FOODS,
        FoodGroup.BREAKFAST_CEREALS,
        FoodGroup.FAST_FOODS,
        FoodGroup.MEALS_ENTREES_AND_SIDE_DISHES,
        FoodGroup.RESTAURANT_FOODS
    ]

food_id_blacklist = \
    [

    ]

food_id_blacklist = flatten(food_id_blacklist)