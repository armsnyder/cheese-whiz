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

    def __init__(self, name='', quantity=None, descriptor='', preparation='', prep_description='', available=True, food_type=None):
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

        # TODO: Make more robust. This probably isn't going to work. Might only work for name and descriptor.
        self.food_type = None
        food_options = knowledge_base.lookup_food(self.name)
        for food in food_options:
            # if the food name contains the given name, descriptor, prep, and prep_description
            # set it as the food_type
            if self.name in food.name.lower():
                if self.descriptor in food.name.lower():
                    if self.preparation in food.name.lower():
                        if self.prep_description in food.name.lower():
                            self.food_type = food