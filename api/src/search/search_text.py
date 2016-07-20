"""
Lambda handler for search queries. This queries the mongo db for the specified keyword.
"""
import sys
from pymongo import MongoClient, TEXT
from ConfigParser import ConfigParser
from base64 import b64decode
from pprint import pprint


def _setup_collection():
    config = ConfigParser()
    config.read("settings.cfg")
    connection = MongoClient(config.get('mongodb', 'server'))
    db = connection[config.get('mongodb', 'db')]
    return db[config.get('mongodb', 'collection')]


source_collection = _setup_collection()


def _find_doc(collection, keyword):
    """
    MongoDB search function.

    :param collection: Target MongoDB collection
    :param keyword: The keyword to search for.
    :return:
    """
    cursor = collection.find({'$text': {'$search': keyword}})
    result = []
    for document in cursor:
        result.append(
                {k: document.get(k, '') for k in ('article_url',
                                                  'listed_headline',
                                                  'article_headline',
                                                  'article_text',
                                                  'author')})
    return result


def handle_request(event, context):
    """
    Dispatches the api request to the MongoDB search function.

    :param event: lambda api parameter. Contains the search keyword.
    :param context: Unused for now.
    :return: List of articles matching the search keyword.
    """

    # keyword is base 64 encoded so we can receive it correctly through the query string
    keyword = b64decode(event['keyword'])
    return _find_doc(source_collection, keyword)


# For testing via the command line.
#
# $> python search_text.py "search string"
if __name__ == '__main__':
    pprint(_find_doc(source_collection, sys.argv[1]))
