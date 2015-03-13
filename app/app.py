# The "main" file for Cheese Whiz

import kb


def load_knowledge_base():
    """
    Loads and returns knowledge base
    :return: KnowledgeBase object
    """
    knowledge_base = kb.KnowledgeBase()
    knowledge_base.load()
    return knowledge_base