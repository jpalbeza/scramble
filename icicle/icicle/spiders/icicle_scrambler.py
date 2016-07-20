from scrapy import Spider, Request
from scrapy.selector import Selector
from bs4 import BeautifulSoup

from icicle.items import FrontPageItem, ArticlePageItem


class GuardianSpider(Spider):
    """
    Custom spider for scraping https://www.theguardian.com/au.
    """

    name = "guardian-icicles"
    allowed_domains = ["www.theguardian.com"]
    start_urls = ["https://www.theguardian.com/au"]

    def start_requests(self):
        """
        Starting point of the web crawl
        :return:
        """
        yield Request('https://www.theguardian.com/au', self.parse)

    @staticmethod
    def _purify_to_text(marked_up_string):
        """
        Remove superfluous content such as ads and html.

        :param marked_up_string: String with html markups and ads.
        :return: String without html and ads.
        """
        return BeautifulSoup(marked_up_string, "lxml").get_text()

    @staticmethod
    def _safe_get_first(maybe_empty_array):
        """
        Making sure we don't have any exceptions when trying to get from an empty array.

        :param maybe_empty_array: An array that is possibly empty.
        :return: The first content of the array. if the array is empty, returns an empty string.
        """
        return (maybe_empty_array or [''])[0]

    def parse_article(self, response):
        """
        Parses an article page and yields the result as an ArticleItem.

        @url https://www.theguardian.com/environment/2016/jul/20/june-2016-14th-consecutive-month-of-record-breaking-heat-says-us-agencies
        @returns items 1 1
        @scrapes article_url author_url author article_headline article_text
        """
        article_page_item = ArticlePageItem()

        article_page_item['article_url'] = response.url

        article_page_item['author_url'] = \
            self._safe_get_first(Selector(response).xpath('//a[@rel="author"]/@href').extract())

        article_page_item['author'] = \
            self._purify_to_text(
                    self._safe_get_first(
                            Selector(response).xpath('//a[@rel="author"]').extract()))

        article_page_item['article_headline'] = \
            self._purify_to_text(
                    self._safe_get_first(
                            Selector(response).xpath('//h1[@itemprop="headline"]').extract()))

        article_text_blocks = Selector(response).xpath('//div[@itemprop="articleBody"]/p').extract()
        article_page_item['article_text'] = ''.join([self._purify_to_text(markup) for markup in article_text_blocks])

        yield article_page_item

    def parse(self, response):
        """
        Parses the front page. Looks for the list of articles and yields:
        1. a FrontPageItem for further processing down the pipeline
        2. a Request for further crawling of the found url

        @url https://www.theguardian.com/au
        @returns items 20 70
        @returns requests 20 70
        @scrapes article_url listed_headline
        """

        articles = Selector(response).xpath('//div[@class="fc-item__container"]/a[@data-link-name="article"]')

        for article in articles:
            front_page_item = FrontPageItem()
            article_url = article.xpath('@href').extract()[0]
            front_page_item['article_url'] = article_url
            front_page_item['listed_headline'] = article.xpath('text()').extract()[0]

            # FrontPageItem for further processing down the pipeline.
            yield front_page_item

            # Request for further crawling to the article page.
            yield Request(article_url, self.parse_article)
