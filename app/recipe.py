class Recipe:

    def __init__(self, ingredients=None, steps=None):
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

    def __init__(self, name='', quantity=None, descriptor='', preparation='', prep_description='', available=True,
                 food_type=None):
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
        attempts = [
            lambda: self._match_attempt_1(knowledge_base),
            lambda: self._match_attempt_2(knowledge_base),
            lambda: self._match_attempt_3(knowledge_base),
            lambda: self._match_attempt_4(knowledge_base),
            ]
        for attempt in attempts:
            attempt()
            if self.food_type:
                break
        return self

    def _match_attempt_1(self, knowledge_base):
        query_string = ' '.join([self.name, self.descriptor, self.preparation, self.prep_description])
        self._match_attempt_base(knowledge_base, query_string)

    def _match_attempt_2(self, knowledge_base):
        query_string = ' '.join([self.name, self.descriptor, self.preparation])
        self._match_attempt_base(knowledge_base, query_string)

    def _match_attempt_3(self, knowledge_base):
        query_string = ' '.join([self.name, self.descriptor])
        self._match_attempt_base(knowledge_base, query_string)

    def _match_attempt_4(self, knowledge_base):
        self._match_attempt_base(knowledge_base, self.name)

    def _match_attempt_base(self, knowledge_base, query_string):
        food_options = knowledge_base.lookup_food(query_string)
        old_food_options = []
        if len(food_options) > 1:
            old_food_options.extend(food_options)
            food_options = knowledge_base.lookup_food(query_string + ' raw')
        if not len(food_options):
            food_options = []
            food_options.extend(old_food_options)
        if len(food_options) > 1:
            for food_option in food_options:
                if not self.food_type or len(food_option.name) < len(self.food_type.name):
                    self.food_type = food_option
            return
        if len(food_options) == 1:
            self.food_type = food_options[0]