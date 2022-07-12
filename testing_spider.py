
import requests
from scrapy.selector import Selector
from scrapy import Request
from urllib.parse import urljoin
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

import time
import requests
class SuperSpider(CrawlSpider):
    name = 'spider'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    base_url = 'http://quotes.toscrape.com'
    rules = [Rule(callback='parse_func', follow=True)]
 
    def parse_func(self, response):
        for quote in response.css('div.quote'):
            yield {
                'Author': quote.xpath('.//span/a/@href').extract_first(),
                'Quote': quote.xpath('.//span[@class= "text"]/text()').get(),
            }