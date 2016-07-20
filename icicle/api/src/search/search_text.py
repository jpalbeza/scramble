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
    keyword = b64decode(event['keyword'])
    return _find_doc(source_collection, keyword)


if __name__ == '__main__':
    pprint(_find_doc(source_collection, sys.argv[1]))
