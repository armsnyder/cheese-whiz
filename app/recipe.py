import nltk
import re


class Recipe:

    def __init__(self, title=None, ingredients=None, steps=None):
        self.title = title
        self.ingredients = []
        self.steps = []
        if ingredients:
            self.add_ingredients(ingredients)
        if steps:
            self.add_steps(steps)

    def add_ingredients(self, ingredients_list):
        self.ingredients.extend(ingredients_list)

    def add_steps(self, steps_list):
        self.steps.extend(steps_list)


class Ingredient:

    def __init__(self, name='none', quantity=None, descriptor='none', preparation='none', prep_description='none',
                 available=True, food_type=None):
        self.name = name
        self.quantity = quantity  # kb.Quantity object
        self.descriptor = descriptor
        self.preparation = preparation
        self.prep_description = prep_description
        self.available = available
        self.food_type = food_type

    def match_to_food(self, knowledge_base):
        """
        Set the food_type field based on information in the other fields
        @:param knowledge_base: knowledge_base object to search in
        """
        self.food_type = None
        words = []
        for word in [self.prep_description, self.preparation, self.descriptor, self.name]:
            if word == 'none':
                words.append('')
            else:
                words.append(word)
        attempts = [
            lambda: self._match_special_cases(knowledge_base),
            lambda: self._match_attempt(knowledge_base, ' '.join([words[0], words[1], words[2], words[3]])),
            lambda: self._match_attempt(knowledge_base, ' '.join([words[1], words[2], words[3]])),
            lambda: self._match_attempt(knowledge_base, ' '.join([words[2], words[3]])),
            lambda: self._match_attempt(knowledge_base, words[3]),
            ]
        for attempt in attempts:
            attempt()
            if self.food_type:
                break
        return self

    def _match_attempt(self, knowledge_base, query_string):
        food_options = sorted(knowledge_base.lookup_food(query_string),
                              key=lambda x: self._rank_food(x, query_string), reverse=True)
        if len(food_options):
            self.food_type = food_options[0]

    def _match_special_cases(self, knowledge_base):
        full_name = ' '.join([self.prep_description, self.preparation, self.descriptor, self.name])
        if 'ground' in full_name and 'beef' in full_name and '%' not in full_name:
            self._match_attempt(knowledge_base, 'Beef, ground, 85% lean meat')
        if self.name == 'flour' and self.descriptor == 'none':
            self._match_attempt(knowledge_base, 'wheat flour all-purpose enriched bleached')
        if self.name == 'water':
            self._match_attempt(knowledge_base, 'tap water')

    @staticmethod
    def _rank_food(food_option, query_string):
        """
        Sorting function used to rank search results
        :param food_option: Food object candidate
        :param query_string: desired food name string
        :return: rank (int)
        """

        rank = 0
        tokenizer = nltk.tokenize.RegexpTokenizer(r'[\w\d]+')

        food_option_tokens = tokenizer.tokenize(food_option.name.lower())
        food_option_bigrams = nltk.bigrams(food_option_tokens)

        if food_option.common_name:
            food_common_tokens = tokenizer.tokenize(food_option.common_name.lower())
        else:
            food_common_tokens = tokenizer.tokenize('')
        food_common_bigrams = nltk.bigrams(food_common_tokens)

        query_tokens = tokenizer.tokenize(query_string.lower())
        query_bigrams = nltk.bigrams(query_tokens)

        option_count = len(food_option_tokens)
        common_count = len(food_common_tokens)

        # Favor shorter food names
        rank -= (option_count + common_count) / 2

        # Favor foods containing full query terms
        for token in query_tokens:
            if token in food_option_tokens or token in food_common_tokens:
                rank += 1

        # Favor foods with query terms appearing closer to the beginning of the food name
        for i in range(max(option_count, common_count)):
            if len(food_option_tokens) > i and food_option_tokens[i] in query_tokens:
                rank += int((option_count-i)*3/option_count)
                break
            if len(food_common_tokens) > i and food_common_tokens[i] in query_tokens:
                rank += int((common_count-i)*3/common_count)
                break

        # Favor foods with query terms appearing in-order
        for query_bigram in query_bigrams:
            if query_bigram in food_option_bigrams or query_bigram in food_common_bigrams:
                rank += 2

        # Favor raw foods
        if 'raw' in food_option_tokens:
            rank += 4
        if 'whole' in food_option_tokens:
            rank += 1
        return rank