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

import pandas as pd
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)

# service = Service('/usr/local/bin/chromedriver')
# service.start()
service = Service(r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe')
service.start()

# for holding the resultant list
footballtransfer_list = []
  
for page in range(1, 10, 1):
    
    page_url = "http://www.footballtransfers.com/en/transfers/confirmed/" + str(page)
    print(page_url)
    # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver = webdriver.Remote(service.service_url)
    driver.get(page_url)
    get_elements = WebDriverWait(driver, 100).until(EC.visibility_of_all_elements_located((By.XPATH,'//tbody[@id="player-table-body"]/tr')))
    time.sleep(10) # Implemented this t

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
            print(footballtransfer_dict)
            footballtransfer_list.append(footballtransfer_dict)
        except selenium.common.exceptions.NoSuchElementException:
            pass
        else:
            pass
        finally:
            pass
    driver.close()

df = pd.DataFrame(footballtransfer_list)
df.to_csv('footballtransfer_transfer.csv')
