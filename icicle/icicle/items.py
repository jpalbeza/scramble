from scrapy import Item, Field


class FrontPageItem(Item):
    """ Model for an article appearing in the front page. """
    article_url = Field()
    listed_headline = Field()


class ArticlePageItem(Item):
    """Model for items int eh article page."""
    article_url = Field()
    article_headline = Field()
    author_url = Field()
    author = Field()
    article_text = Field()

