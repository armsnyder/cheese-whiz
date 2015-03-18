# The "main" file for Cheese Whiz

import os
import pickle

import kb
import util
import parser


def main():
    """
    Placeholder main method for calling script with command line parameters
    """
    knowledge_base = load_knowledge_base()
    pass


def load_knowledge_base():
    """
    Loads and returns knowledge base
    :return: KnowledgeBase object
    """
    kb_object_path = util.relative_path('kb_data/kb_object.p')
    if os.path.isfile(kb_object_path):
        knowledge_base = pickle.load(open(kb_object_path, 'rb'))
    else:
        knowledge_base = kb.KnowledgeBase()
        knowledge_base.load()
        pickle.dump(knowledge_base, open(kb_object_path, 'wb'))
    return knowledge_base


def student(url):
    knowledge_base = load_knowledge_base()
    return parser.url_to_dictionary(url, knowledge_base)