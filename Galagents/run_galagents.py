from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import data_galagents
import scrapper_galagents

import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
#sys.path.insert(1, r'C:\Users\Administrator\Documents\Projects\scrapper_JD') # Path to use in Lightsail
sys.path.insert(1, '/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/') # Path para uso personal

import send_information

"""
TO DO:
    1. Obtener números de cabinas para organizar JSON
"""


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

#driver_path = data_gadventures.DRIVER_PATH_WINDOWS # Para Lightsail
driver_path = data_galagents.DRIVER_PATH_PERSONAL # Para uso personal

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# Gets the info
scrapper_galagents.get_info(driver)


#print(data_galagents.COMPLETE_JSON)
print('\nInfo obtained succesfully')
print('\nSending information to API...')
send_information.send_information(data_galagents.COMPLETE_JSON, 'Galagents')


    
    





























"""
FOR SCRAPING THE GALAGENTS WEBSITE

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

#driver_path = data_gadventures.DRIVER_PATH_WINDOWS # Para Lightsail
driver_path = data_galagents.DRIVER_PATH_PERSONAL # Para uso personal

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(data_galagents.URL)
#driver.maximize_window()
print('\nScraping for GALAGENTS starts')

scrapper_galagents.close_chat_bot(driver)
print('Manipulating search filters...')
scrapper_galagents.search_filters_manipulation(driver)
print('Obtaining information...')
scrapper_galagents.get_data(driver)
"""









