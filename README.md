# Cheese Wiz
by Kristen Amaddio, Neal Kfoury, Michael Nowakowski, and Adam Snyder  
Northwestern University  
EECS 337  
Professor Lawrence Birnbaum

### Overview
A recipe transformer, capable of converting recipes to/from vegetarian, changing the style of cuisine, converting
to/from healthy versions of recipes, and much more! Just give it a web address for your favorite recipe, and Cheese
Wiz will handle the rest.

#### Recipe Parsing
Our program first looks up a recipe URL, which must be from allrecipes.com. It extracts basic information like ingredients, quantities, and steps. It then performs several parsing and language processing methods to separate the basic recipe text into numerical quantities, units, ingredient names, ingerdient descriptions, ingredient preparations, preparation descriptions, cooking methods, and cooking tools.

#### Recipe Mutation
Once the recipe has been fully parsed, the user has the option to perform a number of mutations.

##### Style
The user may choose to make a recipe into a Mexican, Italian, or South Asian variant of the same recipe, which is accomplished by substituting ingredients and adding additional spices to match the correct palate.

##### Healthy / Unhealthy
The user may wish to make the recipe more (or less) healthy. A healthier recipe is accomplished by querying the knowledge base on each ingredient for a lower-fat or less-sugar version of each ingredient. A less healthy recipe is accomplished by looking for similar ingredients that are higher in far and sugar.

##### Vegetarian / Vegan
If the user requests a vegetarian or vegan version of the recipe, our program checks the food group of each ingredient, which it finds in the knowledge base, to ensure it is safe. If it is not, it refers primarily to a list of substitutions.

##### Availability
The user has the option to specify that an ingredient is not available to him or her. The program then queries a list of common substitutions *and* searches the knowledge base for similar ingredients based on chemical makeup of the food. The user is provided a list of substitution options for the ingredient. If none of these ingredients are available still, the user can request that the program re-query allrecipes for a new recipe that does not contain these unavailable ingredients.

#### Knowledge Base
Our ingredient knowledge base is based largely on the [USDA Nutrient Database](http://ndb.nal.usda.gov/ndb/search/list). Immediately after parsing an ingredient, we attempt to match it to a food from this database so that we have access to its nutritional information.

We also have a set of text files containing rules and definitions. We compiled these lists using a combination of hard-coding and web scraping with beautifulsoup4 and regular expressions. The knowledge base loads these lists and, in many cases, performs language processing methods to transform them into useful objects that may be used in the code.

**cooking_terms.txt**  
A list of cooking terminology, such as "broil" or "stir," which are used for extracting cooking methods from recipe steps.

**cooking_wares.txt**  
A list of cooking tools, such as "skillet" or "microwave safe bowl," which are used for extracting tools from recipe steps.

**measurements.txt**  
A list of measurement units and unit abbreviation equalities, such as "slice" or "teaspoon = tsp.," which are used for extracting units from quantity strings throughout the code.

**common_substitutions.txt**  
A list of ingredient equalities, completely raw and unparsed, which support multiple substitution options. This is useful mostly for substituting ingredients based on the user's kitchen stock.

**vegan_substitutions.txt**  
A list of ingredient equalities, completely raw and unparsed, which support multiple substitution options. This is used as a basic starting point reference for the vegan substitution function.

**vegetarian_substitutions.txt**  
A list of ingredient equalities, completely raw and unparsed, which support multiple substitution options. This is used as a basic starting point reference for the vegetarian substitution function.

**italian_style.txt**  
A list of ingredient equality statements, completely raw and unparsed, that define exchanges one might make to make a recipe *more* Italian.

**mexican_style.txt**  
A list of ingredient equality statements, completely raw and unparsed, that define exchanges one might make to make a recipe *more* Mexican.

**east_asian_style.txt**  
A list of ingredient equality statements, completely raw and unparsed, that define exchanges one might make to make a recipe *more* East Asian.

### Running the Program
To run the program with a graphical interface, simply run the program with no command line arguments:  
```
python cheese-whiz.py
```
To run the program in the command line, run it with a URL argument:
```
python cheese-whiz.py http://allrecipes.com/Recipe/Baked-Flan
```

### Packages
For convenience, we have included a requirements.txt file in the root directory to install external libraries. To install these dependencies, run this command:
```
pip install -r requirements.txt
```

#### Standard Libraries
We used a number of built-in Python libraries. Without going into detail, here they are:
* re
* Tkinter
* ttk
* platform
* subprocess
* threading
* Queue
* time
* compiler
* urllib2
* sys
* os

#### External Packages
In addition to the standard Python libraries, several packages modules were used to improve performance.

**nltk**  
Natural Language Toolkit used for tokenizing natural language and labeling parts of speech

**beautifulsoup4**  
A web scraper used for pulling html content out of tags
