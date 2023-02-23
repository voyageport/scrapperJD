from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import requests
import string
import re
import time
import scrapper_andando
import data_andando
import json

import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
#sys.path.insert(1, r'C:\Users\Administrator\Documents\Projects\scrapper_JD') # Path to use in Lightsail
sys.path.insert(1, '/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/') # Path para uso personal

import send_information

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

"""
Encontrar la forma de obtener información...
"""


#driver_path = data_andando.DRIVER_PATH_WINDOWS # Para Lightsail
driver_path = data_andando.DRIVER_PATH_PERSONAL # Para uso personal

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
print('Scraping for Andando Tours starts')


for i in range(2):
    if i == 0:
        url = data_andando.URL_PASSION
    else:
        url = data_andando.URL_MARY_ANN
        
    driver.get(url)
    #driver.maximize_window()
    time.sleep(7)
    
    scrapper_andando.prepare_frame_info(driver)
    
    for j in range(3):
        #if i == 1 or i == 4:
        if j == 1:
            #scrapper_andando.click_on_element_by_path(driver, data_andando.YEAR_PATH_GENERAL.format(2))
            try:
                year = driver.find_element(By.XPATH, data_andando.YEAR_PATH_GENERAL.format(2))
                print(f'\t{year.get_attribute("innerHTML")}')
                year.click()
                time.sleep(5)
            except:
                print('No pudo 1')
        elif j == 2:
            try:
                #scrapper_andando.prepare_frame_info(driver)
                year = driver.find_element(By.XPATH, data_andando.YEAR_PATH_GENERAL.format(3))
                print(f'\t{year.get_attribute("innerHTML")}')
                year.click()
                time.sleep(5)
            except:
                print('No pudo 2')
            
        scrapper_andando.get_all_rows_info(driver)
        



    scrapper_andando.get_arrival_dates()        
    scrapper_andando.create_json(i)    
    scrapper_andando.empty_lists()



#print(data_andando.COMPLETE_JSON)

send_information.send_information(data_andando.COMPLETE_JSON, 'AndandoTours', False)

print('*** Scrapping process finished for Andando successfully')


















"""
    print('len DATES: ', len(data_andando.DATES))
    print('len ARRIVAL: ', len(data_andando.ARRIVAL_DATES))
    print('len DAYS: ', len(data_andando.DAYS))
    print('len AVAILABILITIES: ', len(data_andando.AVAILABILITIES))
    print('len PRICES: ', len(data_andando.PRICES))

if len(data_andando.DATES) == len(data_andando.ARRIVAL_DATES) == len(data_andando.DAYS):
    for i in range(len(data_andando.DATES)):
        print('{}\t\t{}\t\t{}'.format(data_andando.DATES[i], data_andando.ARRIVAL_DATES[i], data_andando.DAYS[i]))
"""