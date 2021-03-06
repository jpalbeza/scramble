# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class MongoDBPipeline(object):
    """
    Writes FrontPageItem or ArticlePageItem into MongoDb.
    """

    def __init__(self):
        connection = pymongo.MongoClient(
                settings['MONGODB_SERVER']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                raise DropItem("Invalid field!")
        if valid:
            self.collection.update_one({'article_url': item['article_url']},
                                       {'$set': dict(item)},
                                       upsert=True)
            log.msg("Article added to MongoDB database!", level=log.DEBUG, spider=spider)
        return item
