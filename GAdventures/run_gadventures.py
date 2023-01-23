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
import data_gadventures
import scrapper_gadventures
import json

import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
#sys.path.insert(1, r'C:\Users\Administrator\Documents\Projects\scrapper_JD') # Path to use in Lightsail
sys.path.insert(1, '/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/') # Path para uso personal

import send_information

"""
*** YA ESTÁ LISTO PARA ACTTUALIZAR DATOS EN GDS
TO DO:
    1. Revisar envío de precios
    2. Incluir promociones
"""


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

#driver_path = data_gadventures.DRIVER_PATH_WINDOWS # Para Lightsail
driver_path = data_gadventures.DRIVER_PATH_PERSONAL # Para uso personal

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(data_gadventures.URL)
driver.maximize_window()
print('Scraping for G Adventures starts')

# Click con 'View all Galápagos tours
scrapper_gadventures.click_on_element_by_class_name(driver, data_gadventures.VIEW_ALL_TOURS_BUTTON_CLASS_NAME)

time.sleep(7)

# Stores all the tour titles
scrapper_gadventures.store_trip_names(driver)

time.sleep(5)

# Stores the info of all buttons that redirects to specific tours
tour_buttons = driver.find_elements(By.CLASS_NAME, 'search-btn')

time.sleep(5)

# Call to get all data from pages
scrapper_gadventures.get_data_part_1(driver, tour_buttons)

#print('\n\n*** ', data_gadventures.COMPLETE_JSON)

time.sleep(2)
print('Storing JSON to file...')
scrapper_gadventures.json_to_file()    

# Closes the websitee
driver.close()


time.sleep(2)
print('Sending information to API')
#send_information.send_information(data_gadventures.COMPLETE_JSON)
send_information.send_information(data_gadventures.COMPLETE_JSON, 'GAdventures')


print('Process finished succesfully')

    
    
            
    
    
    
    
