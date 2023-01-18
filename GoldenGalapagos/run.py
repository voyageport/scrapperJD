from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
    
#sys.path.insert(1, r'C:\Users\Administrator\Documents\Projects\scrapper_JD') # Path to use in Lightsail
sys.path.insert(1, '/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/') # Personal testing path

import send_information
import json
import time
import data
import scrapper

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

no_of_tries = 0

#driver_path = data.DRIVER_PATH_WINDOWS # Para usar en Lightsail
driver_path = data.DRIVER_PATH_PERSONAL # Para uso personal

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 


def manipulate_page(driver):
    
    driver.get(data.URL)
    driver.maximize_window()
    print('Scraping for Golden Galapagos starts')
    
    time.sleep(30)
 

    
    # Click on End Date
    scrapper.click_on_element_by_path(driver, data.END_DATE_PATH)
    print('Setting date filters...')
    time.sleep(3)
    
    # Click on Year
    scrapper.click_on_element_by_class_name(driver, data.YEAR_CLASS_NAME)
    
    #Clck on specific year (+2)
    scrapper.click_on_element_by_path(driver, data.YEAR_SELECTION_PATH)
    print('   Year selected')
    
    # Click on first day of month
    scrapper.click_on_element_by_class_name(driver, data.DAY_SELECTION_CLASS_NAME)
    print('   Day selected')
    

    """
    # Click on Month
    scrapper.click_on_element_by_class_name(driver, data.MONTH_CLASS_NAME)
    
    # Click on specific month (+6 months)
    scrapper.click_on_element_by_path(driver, data.MONTH_SELECTION_PATH)
    print('   Month selected')
    """    
    
    # Filter for 2 passengers
    scrapper.click_on_element_by_path(driver, data.GUESTS_PATH)
    scrapper.click_on_element_by_path(driver, data.GUESTS_2_PATH)
    
    
    # Click 'Search' button
    scrapper.click_on_element_by_path(driver, data.SEARCH_BUTTON_PATH)
    print('Searching...')
    time.sleep(15)
    
    
    """
    print('Obtaining information...')

    # Grab info
    scrapper.take_all_info(driver, data.ALL_DATA_PATH)
    """
    

    print('Getting cabins information...')
    cabinas = driver.find_elements(By.CSS_SELECTOR, data.CABINAS_CSS_SELECTOR)  # Gets all cabins numbers and names
    print('Getting availabilitis information...')
    availabilities = driver.find_elements(By.CLASS_NAME, data.AVAILABILITIES_CLASS_NAME) # Gets all availabilities
    print('Getting promotions information...')
    lista_cabin_cards = driver.find_elements(By.CLASS_NAME, 'cabin-card')

    
    print('Processing data...')
    scrapper.process_cabins_and_availabilities(cabinas, availabilities, lista_cabin_cards) # Store cabins and availabilities in lists (or stacks)



try:
    manipulate_page(driver)
except:
    """
    Program only makes 2 tries before failure
    """
    print('Try #2')
    manipulate_page(driver)
    


for ships in range(data.TOTAL_SHIPS):
    try:
        """
        Gets the number of dates on each ship and stores it on list data.CRUISE_AND_DATES
        """
        # Código para solo un barco
        
        texto_columnas = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/section/div/div/div[5]/div/div/div[2]/div[{}]/div[3]'.format(ships+1))
        texto_columnas = texto_columnas.text
        texto_columnas = texto_columnas.split(' ')
        dates_by_cruise = 0
        
        for i in range(len(texto_columnas)):
            if texto_columnas[i] == 'Available:':
                dates_by_cruise += 1 # Almacena el número de fechas por barco
        
        #cruises_and_dates.append(dates_by_cruise) # Arreglo en el que el índice es el barco y el valor es el número de días por barco
        data.CRUISES_AND_DATES.append(dates_by_cruise)
    
    except:
        data.TOTAL_SHIPS -= 1
        #data.BARCOS[2] = 'oceanspray'

#print('Fechas por bote: ', data.CRUISES_AND_DATES)

lower_limit_dates = 0 # Allows for data to be stored by ship
upper_limit_dates = 0

#limite_inferior_fechas = 0
#limite_superior_fechas = 0

print('Processing data from: ')
for k in range(data.TOTAL_SHIPS): # k is the number of ship
    print('   {}'.format(data.BARCOS[k]))
    #time.sleep(5) For better visualization
    """
    Cabins and availabilities are separated by the number of dates on each ship
    """
    lower_limit_dates = data.CRUISES_AND_DATES[k] + lower_limit_dates
    upper_limit_dates = data.CRUISES_AND_DATES[k + 1]
    scrapper.get_data(driver, lower_limit_dates, upper_limit_dates, k)
    

#print('Data promo: ', data.PROMOS_FINAL)

#print(data.COMPLETE_JSON) # Print of the final json file

print('\n\nScraping ended')



driver.close()



#print(data.COMPLETE_JSON)



scrapper.string_to_json_file(data.COMPLETE_JSON) # Creates a json file with all the data
# process_json.string_to_json_file(data.COMPLETE_JSON) function in old directory


data = scrapper.string_to_json_return(data.COMPLETE_JSON)

print('\n*** Changing json file format\n')
final_json = scrapper.change_json_format(data) # Changes the format of the json file to the one that can be sent to the API
final_json = json.loads(final_json)

#print(final_json)


print('\n*** Sending info to API\n')
send_information.send_information(final_json) # Sends the information to the API

print('\n\nProcess finished succesfully')

























