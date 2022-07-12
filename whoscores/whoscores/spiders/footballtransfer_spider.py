import scrapy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from scrapy.http import Request

import pandas as pd
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.DEBUG)

service = Service('/usr/local/bin/chromedriver')
service.start()
# service = Service(r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe')
# service.start()
class footballTransfer(scrapy.Spider):
# for holding the resultant list
    name = 'footballtransfer'
    allow_domains = ['www.footballtrasnfers.com']
    start_urls = ['http://www.footballtransfers.com/']
    footballtransfer_list = []


    def __init__(self,*args,**kwargs):
        self.footballtransfer_list = []
        self.sleep_timer = 10
    def parse(self,response):
        for page in range(1, 10, 1):
            
            page_url = "http://www.footballtransfers.com/en/transfers/confirmed/" + str(page)
            print(page_url)
            driver = webdriver.Remote(service.service_url)
            driver.get(page_url)
            get_elements = WebDriverWait(driver, 100).until(EC.visibility_of_all_elements_located((By.XPATH,'//tbody[@id="player-table-body"]/tr')))
            time.sleep(self.sleep_timer) # Implemented this t

            for each_item in get_elements:
                footballtransfer_dict = {}

                try:
                    footballtransfer_dict['playerlink'] = each_item.find_element(By.XPATH,'td[1]/div/div/a').get_attribute('href')
                    footballtransfer_dict['playername'] = each_item.find_element(By.XPATH,'td[1]/div/div/a').get_attribute('title')
                    footballtransfer_dict['age'] = each_item.find_element(By.XPATH,'td[2]').text
                    footballtransfer_dict['nationality'] = each_item.find_element(By.XPATH,'td[1]/div/div/figure/img').get_attribute('alt')
                    footballtransfer_dict['From club'] = each_item.find_element(By.XPATH,'td[3]/div/div[1]/a').get_attribute('title')
                    footballtransfer_dict['To club'] = each_item.find_element(By.XPATH,'td[3]/div/div[2]/a').get_attribute('title')
                    footballtransfer_dict['Date'] = each_item.find_element(By.XPATH,'td[4]').text
                    footballtransfer_dict['MV'] = each_item.find_element(By.XPATH,'td[5]').text
                    
                    # yield Request(footballtransfer_dict['playerlink'],callback=self.player_profileParse,dont_filter=True,meta={'footballtransfer':footballtransfer_dict})
                    self.footballtransfer_list.append(footballtransfer_dict)
                except selenium.common.exceptions.NoSuchElementException:
                    pass
                else:
                    pass
                finally:
                    pass

                # if footballtransfer_dict:
                #     yield footballtransfer_dict
            driver.close()

        df = pd.DataFrame(self.footballtransfer_list)
        df.to_csv('footballtransfer_transfer.csv')
    

    def player_profileParse(self,response):
        footballtransfer_dict = response.meta['footballtransfer']
        print('#########################',footballtransfer_dict)


        