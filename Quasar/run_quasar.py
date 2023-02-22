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
import data_quasar
import scrapper_quasar
import json

import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
#sys.path.insert(1, r'C:\Users\Administrator\Documents\Projects\scrapper_JD') # Path to use in Lightsail
sys.path.insert(1, '/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/') # Path para uso personal

import send_information

"""
TO DO:
    1. Preguntar si se necesitan precios a pesar de la falta de disponibilidad específica

Ya está lista la obtención de toda la información necesaria
"""


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

#driver_path = data_quasar.DRIVER_PATH_WINDOWS # Para Lightsail
driver_path = data_quasar.DRIVER_PATH_PERSONAL # Para uso personal

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
print('Scraping for Quasar starts')


print('\nStarting process for Grace')
for i in range(2):
    if i == 0:
        print('\tGetting info 2023...')
        driver.get(data_quasar.URL_GRACE_2023)
        #driver.maximize_window()
        time.sleep(5)
        
    elif i == 1:
        print('\tGetting info 2024...')
        driver.get(data_quasar.URL_GRACE_2024)
        #driver.maximize_window()
        time.sleep(5)
        
    print('\tProcessing info...')
    scrapper_quasar.get_dates(driver)
    scrapper_quasar.get_availabilities(driver, data_quasar.AVAILABILITY_PATH_GENERAL_GRACE)
    scrapper_quasar.get_hold(driver, data_quasar.HOLD_PATH_GENERAL_GRACE)
    scrapper_quasar.get_prices(driver, data_quasar.PRICES_GENERAL_PATH_GRACE, 'Grace')
    scrapper_quasar.get_charter_promo(driver, data_quasar.CHARTER_GENERAL_PATH_GRACE)
scrapper_quasar.create_json('Grace')

scrapper_quasar.empty_lists()
    

print('\nStarting process for Evolution')
for i in range(2):
    if i == 0:
        print('\tGetting info 2023...')
        driver.get(data_quasar.URL_EVOLUTION_2023)
        #driver.maximize_window()
        time.sleep(5)
        
    elif i == 1:
        print('\tGetting info 2024...')
        driver.get(data_quasar.URL_EVOLUTION_2024)
        #driver.maximize_window()
        time.sleep(5)
        
    print('\tProcessing info...')
    scrapper_quasar.get_dates(driver)
    scrapper_quasar.get_availabilities(driver, data_quasar.AVAILABILITY_PATH_GENERAL_EVOLUTION)
    scrapper_quasar.get_hold(driver, data_quasar.HOLD_PATH_GENERAL_EVOLUTION)
    scrapper_quasar.get_prices(driver, data_quasar.PRICES_GENERAL_PATH_GRACE, 'Evolution')
    scrapper_quasar.get_charter_promo(driver, data_quasar.CHARTER_GENERAL_PATH_EVOLUTION)
scrapper_quasar.create_json('Evolution')


"""
print('len start:', len(data_quasar.START_DATES))
print('len end:', len(data_quasar.END_DATES))
print('len availa:', len(data_quasar.AVAILABILITIES))
print('len holds:', len(data_quasar.HOLDS))
print('len charter:', len(data_quasar.CHARTER_PRICES))
"""

#print('***\n', data_quasar.COMPLETE_JSON)

send_information.send_information(data_quasar.COMPLETE_JSON, 'Quasar', False)

"""
len() of Evolution prices 
print('\n\nlen A1: ', len(data_quasar.PRICES_A1))
print('len A2: ', len(data_quasar.PRICES_A2))
print('len A3: ', len(data_quasar.PRICES_A3))
print('len C1: ', len(data_quasar.PRICES_C1))
print('len C2: ', len(data_quasar.PRICES_C2))
print('len C3: ', len(data_quasar.PRICES_C3))
print('len C4: ', len(data_quasar.PRICES_C4))
print('len C5: ', len(data_quasar.PRICES_C5))
print('len C6: ', len(data_quasar.PRICES_C6))
print('len C7: ', len(data_quasar.PRICES_C7))
print('len C8: ', len(data_quasar.PRICES_C8))
print('len C9: ', len(data_quasar.PRICES_C9))
print('len D1: ', len(data_quasar.PRICES_D1))
print('len D2: ', len(data_quasar.PRICES_D2))
print('len D3: ', len(data_quasar.PRICES_D3))
print('len D4: ', len(data_quasar.PRICES_D4))
"""












