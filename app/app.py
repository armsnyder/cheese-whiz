# The "main" file for Cheese Whiz

import kb


def main():
    """
    Placeholder main method for calling script with command line parameters
    """
    pass


def load_knowledge_base():
    """
    Loads and returns knowledge base
    :return: KnowledgeBase object
    """
    knowledge_base = kb.KnowledgeBase()
    knowledge_base.load()
    return knowledge_base