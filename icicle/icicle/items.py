# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class FrontPageItem(Item):
    article_url = Field()
    listed_headline = Field()


class ArticlePageItem(Item):
    article_url = Field()
    article_headline = Field()
    author_url = Field()
    author = Field()
    article_text = Field()

