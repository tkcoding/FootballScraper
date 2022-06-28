# importing necessary packages
import requests
from scrapy.selector import Selector
from scrapy import Request
from urllib.parse import urljoin
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pprint

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


import pandas as pd
LOGGER.setLevel(logging.WARNING)
service = Service('/usr/local/bin/chromedriver')
service.start()

# service = Service(r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe')
# service.start()

# for holding the resultant list
# Name
# Age
# Country
# Position
# from Club 
# To club
# Date
# Price
transfer_market_list = []

for page in range(1, 5, 1):
    
    page_url = "https://www.transfermarkt.com/transfers/neuestetransfers/statistik?land_id=0&wettbewerb_id=alle&minMarktwert=500000&maxMarktwert=200000000&plus=1&page=" + str(page)
    # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver = webdriver.Remote(service.service_url)
    driver.get(page_url)
    get_elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH,'//div[@id="yw1"]/table/tbody/tr')))
    # get_elements_age = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH,'//tbody[@id="player-table-body"]/tr/td[2]')))
    for each_item in get_elements:
        transfer_dict = {}

        try:
            transfer_dict['Name']=each_item.find_element(By.XPATH,'./td[1]/table/tbody/tr/td[2]/a').text
            transfer_dict['Age:'] = each_item.find_element(By.XPATH,'./td[2]').text
            transfer_dict['Nationality'] = each_item.find_element(By.XPATH,'./td[3]/img').get_attribute('title')
            transfer_dict['From club'] = each_item.find_element(By.XPATH,'./td[4]/table/tbody/tr/td[2]/a').get_attribute('title')
            transfer_dict['To club'] = each_item.find_element(By.XPATH,'./td[5]/table/tbody/tr/td[2]/a').get_attribute('title')
            transfer_dict['Transfer date'] = each_item.find_element(By.XPATH,'./td[6]').text
            transfer_dict['Market Value']= each_item.find_element(By.XPATH,'./td[7]').text
            transfer_dict['Fees'] = each_item.find_element(By.XPATH,'./td[8]/a').text
        except AttributeError:
            transfer_dict['Name']= None
            transfer_dict['Age:'] = None
            transfer_dict['Nationality'] = None
            transfer_dict['From club'] = None
            transfer_dict['To club'] = None
            transfer_dict['Transfer date'] = None
            transfer_dict['Market Value']= None
            transfer_dict['Fees'] = None
        except selenium.common.exceptions.NoSuchElementException:
            pass
        transfer_market_list.append(transfer_dict)

        # print('Player link : ',each_item.get_attribute('href'))
        # print('Player name ',each_item.get_attribute('title'))

    # for each_age in get_elements_age:
    #     print('Player Age ',each_age.text)

#     price = driver.find_elements_by_class_name("price")
#     description = driver.find_elements_by_class_name("description")
#     rating = driver.find_elements_by_class_name("ratings")
#     for i in range(len(title)):
#         element_list.append([title[i].text, price[i].text, description[i].text, rating[i].text])
  
# print(element_list)

print(transfer_market_list)
df = pd.DataFrame(transfer_market_list)
df.to_csv('transfermarket.csv')
#closing the driver
driver.close()