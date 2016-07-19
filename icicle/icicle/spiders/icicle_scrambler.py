from scrapy import Spider, Request
from scrapy.selector import Selector
from bs4 import BeautifulSoup

from icicle.items import FrontPageItem, ArticlePageItem

class GuardianSpider(Spider):
    name = "guardian-icicles"
    allowed_domains = ["www.theguardian.com"]
    start_urls = ["https://www.theguardian.com/au"]

    def start_requests(self):
        yield Request('https://www.theguardian.com/au', self.parse)

    def purify_to_text(self, marked_up_string):
        return BeautifulSoup(marked_up_string, "lxml").get_text()

    def parse_article(self, response, article_url):
        item = ArticlePageItem()

        item['article_url'] = article_url
        # item['author_url'] = Selector(response).xpath('//a[@rel="author"]/@href').extract()[0]
        # item['author'] = Selector(response).xpath('//a[@rel="author"]/span[@itemprop="name"]/text').extract()[0]
        item['article_headline'] = self.purify_to_text(Selector(response).xpath('//h1[@itemprop="headline"]').extract()[0])
        item['article_text'] = ''.join([self.purify_to_text(markup) for markup in Selector(response).xpath('//div[@itemprop="articleBody"]/p').extract()])

        yield item

    def callback_with_article_url(self, article_url):
        return lambda response: self.parse_article(response, article_url)

    def parse(self, response):
        """
        Parses the returned page from the urls listed under start_requests
        :param response:
        :return:
        """
        articles = Selector(response).xpath('//div[@class="fc-item__container"]/a[@data-link-name="article"]')

        for article in articles:
            item = FrontPageItem()
            article_url = article.xpath('@href').extract()[0]
            item['article_url'] = article_url
            item['listed_headline'] = article.xpath('text()').extract()[0]
            yield item
            yield Request(article_url, self.callback_with_article_url(article_url))

