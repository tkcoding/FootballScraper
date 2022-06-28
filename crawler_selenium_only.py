# importing necessary packages
import requests
from scrapy.selector import Selector
from scrapy import Request
from urllib.parse import urljoin
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
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

import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)

# service = Service('/usr/local/bin/chromedriver')
# service.start()
service = Service(r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe')
service.start()

# for holding the resultant list
footballtransfer_list = []
  
for page in range(1, 3, 1):
    
    page_url = "http://www.footballtransfers.com/en/transfers/confirmed/" + str(page)
    print(page_url)
    # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver = webdriver.Remote(service.service_url)
    driver.get(page_url)

    get_elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH,'//tbody[@id="player-table-body"]/tr')))
    get_elements_age = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH,'//tbody[@id="player-table-body"]/tr/td[2]')))
    for each_item in get_elements:
        print('Player link : ',each_item.find_element(By.XPATH,'td[1]/div/div/a').get_attribute('href'))
        print('Player name : ',each_item.find_element(By.XPATH,'td[1]/div/div/a').get_attribute('title'))

    # for each_age in get_elements_age:
    #     print('Player Age ',each_age.text)
    # time.sleep(5)
#     price = driver.find_elements_by_class_name("price")
#     description = driver.find_elements_by_class_name("description")
#     rating = driver.find_elements_by_class_name("ratings")
#     for i in range(len(title)):
#         element_list.append([title[i].text, price[i].text, description[i].text, rating[i].text])
  
# print(element_list)
  
#closing the driver
driver.close()