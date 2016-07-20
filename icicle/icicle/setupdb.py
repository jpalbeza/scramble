from pymongo import MongoClient, TEXT

from scrapy.conf import settings


def _setup_index(collection):
    collection.create_index([('article_text', TEXT),
                             ('article_headline', TEXT),
                             ('listed_headline', TEXT),
                             ('author', TEXT)])
    print collection.index_information()


def _setup():
    connection = MongoClient(
            settings['MONGODB_SERVER']
    )
    db = connection[settings['MONGODB_DB']]
    collection = db[settings['MONGODB_COLLECTION']]
    _setup_index(collection)


if __name__ == '__main__':
    _setup()
