import requests
from scrapy.selector import Selector
from scrapy import Request
from urllib.parse import urljoin
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

import time
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
service = Service('/path/to/chromedriver')
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait as wait
import time

import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)
service = Service('/usr/local/bin/chromedriver')
service.start()
# Note option 1:
# https://stackoverflow.com/questions/63722538/scrapyselenium-how-to-crawl-a-different-page-list-once-im-done-with-one
# Note option 2 (uses selenium without scrapy)
# https://www.geeksforgeeks.org/how-to-scrape-multiple-pages-using-selenium-in-python/
driver = webdriver.Remote(service.service_url)
driver.get('https://www.footballtransfers.com/en/transfers/latest-football-transfers')
class WSSpider(CrawlSpider):
    name = 'WSSpider'

    def __init__(self, url , *args, **kwargs):
        self.name = 'WSSpider'
        self.start_urls  = [url]
        self.allowed_domains = ['www.footballtransfers.com']
        self.player_list = {}
        # self.rules = [
        #     Rule(               
        #         LinkExtractor(
        #             # allow= 'confirmed/'
        #         ),callback='parse_item', follow=True)]
        self.rules = (
            Rule(
                LinkExtractor(
                    # restrict_xpaths=(
                    #     '//div[@class="responsive-table"]'
                    # ),
                    # allow= [r'(stat)(\/)(page)(\/)(\d+)$',r'stat$']
                ),
                callback='parse_item',
                follow=True,
            ),
        )
        super().__init__(*args, **kwargs)

    def parse_item(self, response):
        player_name = None
        print('###############',response.url)
        # TODO : This will loop through the pages , therefore use the driver.get to get for each page using selenium
        player_name_list = response.xpath('//tbody[@id="player-table-body"]/tr/td[1]/div/div/a')
        for player in player_name_list:
            print(player.xpath('./@title'))
            # self.player_list[player.get_attribute('title')] = player.get_attribute('href')
            yield {'player_name':player.xpath('./@title')}
        # player_transfer_list = response.xpath('//tbody[@id="player-table-body"]/tr')
        # for player in player_transfer_list:
        #     print(player.xpath('./td[1]/div/div').get())
        #     player_name = player.xpath('./td[1]/span/text()').get()
        # Loop through each of the row and get the name,age,fromclub,toclub,date,price 
driver.quit()
