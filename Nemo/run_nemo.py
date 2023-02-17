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
import data_nemo
import scrapper_nemo
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
driver_path = data_nemo.DRIVER_PATH_PERSONAL # Para uso personal

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(data_nemo.URL)
time.sleep(3)

try:
    k = 2
    while True:
    #while k <= 4: # For running only some months        
        """
        Gets the information
        """
        scrapper_nemo.get_boat_name(driver)
        #print('len names: ', len(data_nemo.ALL_BOAT_NAMES))
        scrapper_nemo.get_dates(driver)
        #print('len start: ', len(data_nemo.START_DATES))
        #print('len end: ', len(data_nemo.END_DATES))
        """
        if len(data_nemo.START_DATES) == len(data_nemo.END_DATES):
            for i in range(len(data_nemo.START_DATES)):
                print('start: {}\t\tend:{}'.format(data_nemo.START_DATES[i], data_nemo.END_DATES[i]))
        """
        
        scrapper_nemo.get_availabilities(driver)
        print('\n\n')
        
        """
        for i in range(len(data_nemo.AVAILABILITIES)):
            print(data_nemo.AVAILABILITIES[i])
        """

        
        scrapper_nemo.create_json()
        
        
        
        """        
        Goes to the next month
        """
        #scrapper_nemo.click_on_element_by_path(driver, data_nemo.MONTH_SELECTOR_PATH)
        #time.sleep(2)
        scrapper_nemo.click_on_element_by_path(driver, data_nemo.SPECIFIC_MONTH_GENERAL_PATH.format(k))
        k += 1
        time.sleep(10)
        
        scrapper_nemo.empty_lists()

except:
    print('Falló')


#print('\n\n', data_nemo.COMPLETE_JSON)

print('Sending info to API...', end='\t\t')
send_information.send_information(data_nemo.COMPLETE_JSON, 'Nemo', False)
print('\n\n*** Scrapping process for Nemo completed')

































