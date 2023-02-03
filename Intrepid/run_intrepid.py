from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import scrapper_intrepid
import data_intrepid
import requests
import string
import re
import time
import json

import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, r'C:\Users\Administrator\Documents\Projects\scrapper_JD') # Path to use in Lightsail
#sys.path.insert(1, '/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/') # Path para uso personal

import send_information


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

#driver_path = data_gadventures.DRIVER_PATH_WINDOWS # Para Lightsail
driver_path = data_intrepid.DRIVER_PATH_PERSONAL # Para uso personal

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

print('Starting scraping process for Intrepid')


driver.get(data_intrepid.URL)
#driver.maximize_window()
print('Scraping for Intrepid starts')
time.sleep(3)


# Click on 'X' Cookies
scrapper_intrepid.click_on_element_by_class_name(driver, data_intrepid.CLOSE_COOKIES_CLASS_NAME)

# Search for 'Galapagos Islands'
scrapper_intrepid.write_element_by_xpath(driver, data_intrepid.SEARCH_BOX_PATH, 'Galapagos Islands')

# Click on 'Adventure Cruising'
scrapper_intrepid.click_on_element_by_path(driver, data_intrepid.CHECK_BOX_ADVENTURE_CRUISING_PATH)
print("Filtered for 'Adventure Cruising'")
time.sleep(3)

# Finds the number of trips displayed on the page
total_trips_web = int(driver.find_element(By.XPATH, data_intrepid.NUMBER_OF_TRIPS_PATH).get_attribute('innerHTML'))
print('Number of trips found (web): ', total_trips_web)

# Stores all the links
scrapper_intrepid.get_all_tour_links(driver, total_trips_web)
print('All URLs stored')
time.sleep(2)


# Get all data
print('Getting all data...')
scrapper_intrepid.get_data(driver)
print('\n\nScraping process finished succesfuly\n\n')
time.sleep(3)
driver.close()

# Send info to API
print('Sending info to API...')
send_information.send_information(data_intrepid.COMPLETE_JASON, 'Intrepid')

print('\n\n***Process finished succesfuly')






"""
CODE FOR ONLY TESTING 1 LINK


scrapper_intrepid.get_data(driver)
print('Scraping process ended')
#time.sleep(2)
print(data_intrepid.COMPLETE_JASON)
#print('Sending information to API...\n')
#send_information.send_information(data_intrepid.COMPLETE_JASON, 'Intrepid')
"""










    
    

















