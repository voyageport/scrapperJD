from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time
import data_aqua
import scrapper_aqua

import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
#sys.path.insert(1, r'C:\Users\Administrator\Documents\Projects\scrapper_JD') # Path to use in Lightsail
sys.path.insert(1, '/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/') # Path para uso personal

import send_information

"""
    LLEVAR TODA LA INFO A ARCHIVO JSOON
"""




options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

#driver_path = data_aqua.DRIVER_PATH_WINDOWS # Para Lightsail
driver_path = data_aqua.DRIVER_PATH_PERSONAL # Para uso personal

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

print('Scraping for Oniric starts')
driver.get(data_aqua.URL)
time.sleep(5)

print('Obtaining information...', end = '')
scrapper_aqua.get_data(driver)
print('\t\tcompleted!')
driver.close()

print('Creating JSON file...', end = '')
scrapper_aqua.create_json()
print('\t\tcompleted!')
print('\n\n', data_aqua.COMPLETE_JSON, end='\n\n')

print('Sending information to API...')
send_information.send_information(data_aqua.COMPLETE_JSON, 'AquaExpeditions', False)
print('\t\tcompleted!')




"""
print('len departures: ', len(data_aqua.DEPARTURE_DATES))
print('len arrival: ', len(data_aqua.ARRIVAL_DATES))
print('len prices: ', len(data_aqua.PRICES))
print('len availability: ', len(data_aqua.AVAILABILITIES))
"""
























