from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import requests
import string
import re
import time
import data_oniric
import scrapper_oniric
import json

import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
#sys.path.insert(1, r'C:\Users\Administrator\Documents\Projects\scrapper_JD') # Path to use in Lightsail
sys.path.insert(1, '/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/') # Path para uso personal

import send_information


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

#driver_path = data_gadventures.DRIVER_PATH_WINDOWS # Para Lightsail
driver_path = data_oniric.DRIVER_PATH_PERSONAL # Para uso personal

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

print('Scraping for Oniric starts')
driver.get(data_oniric.URL)
#driver.maximize_window()
time.sleep(10)


print('\nSetting date filters...', end = '\t\t')
scrapper_oniric.set_search_filters(driver) # Sets date search a year in the future
print('completed')

print('\nScrolling to the end of page...', end = '\t\t')
scrapper_oniric.scroll_down(driver) # Scrolls to the end of the page
print('completed')

print('\nGetting information from page...', end = '\t\t')
scrapper_oniric.get_all_info_columns(driver)
print('completed')

print('Processing data internally...', end = '\t\t')
scrapper_oniric.process_info()
print('completed')


print('Creating JSON file...', end = '\t\t')
scrapper_oniric.create_json_file()
print('completed')
print(data_oniric.COMPLETE_JSON)

print('Sending info to GDS...', end = '\t\t')
send_information.send_information(data_oniric.COMPLETE_JSON, 'Oniric', False)
print('completed')




    
















"""
INFO FOR CHECKING
print('len columns: ', len(data_oniric.COLUMNS_INFO))
print('len boat names: ', len(data_oniric.ALL_BOAT_NAMES))
print('len departure dates: ', len(data_oniric.DEPARTURE_DATES))
print('len arrival dates: ', len(data_oniric.ARRIVAL_DATES))
print('len availabilities: ', len(data_oniric.AVAILABILITIES))
print('len hold: ', len(data_oniric.HOLD))
print('len prices: ', len(data_oniric.PRICES))


print('\n\n*** SOLARIS ***')
print('\tdeparture dates: ', len(data_oniric.DEPARTURE_DATES_SOLARIS))
print('\tlen arrival dates: ', len(data_oniric.ARRIVAL_DATES_SOLARIS))
print('\tlen availabilities: ', len(data_oniric.AVAILABILITIES_SOLARIS))
print('\tlen hold: ', len(data_oniric.HOLD_SOLARIS))
print('\tlen prices: ', len(data_oniric.PRICES_SOLARIS), end = '\n\n\n')

print('*** TREASURE ***')
print('\tdeparture dates: ', len(data_oniric.DEPARTURE_DATES_TREASURE))
print('\tlen arrival dates: ', len(data_oniric.ARRIVAL_DATES_TREASURE))
print('\tlen availabilities: ', len(data_oniric.AVAILABILITIES_TREASURE))
print('\tlen hold: ', len(data_oniric.HOLD_TREASURE))
print('\tlen prices: ', len(data_oniric.PRICES_TREASURE), end = '\n\n\n')


print('*** ARCHIPEL I ***')
print('\tdeparture dates: ', len(data_oniric.DEPARTURE_DATES_ARCHIPEL))
print('\tlen arrival dates: ', len(data_oniric.ARRIVAL_DATES_ARCHIPEL))
print('\tlen availabilities: ', len(data_oniric.AVAILABILITIES_ARCHIPEL))
print('\tlen hold: ', len(data_oniric.HOLD_ARCHIPEL))
print('\tlen prices: ', len(data_oniric.PRICES_ARCHIPEL), end = '\n\n\n')


print('*** AQUA ***')
print('\tdeparture dates: ', len(data_oniric.DEPARTURE_DATES_AQUA))
print('\tlen arrival dates: ', len(data_oniric.ARRIVAL_DATES_AQUA))
print('\tlen availabilities: ', len(data_oniric.AVAILABILITIES_AQUA))
print('\tlen hold: ', len(data_oniric.HOLD_AQUA))
print('\tlen prices: ', len(data_oniric.PRICES_AQUA), end = '\n\n\n')
"""






    














