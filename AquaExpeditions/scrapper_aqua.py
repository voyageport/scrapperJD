from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from data_aqua import COMPLETE_JSON

import time
import data_aqua

def get_data(driver):
    month = 1 # Keeps track of month for clicking
    
    year_number = 1 # Keeps track of year for clicking on month's path
    indicador = 3

    for i in range(12): # Gets info for every month
    #for i in range(2): # For testing with only 1 month
        try:
            """
            Clicks on specific months and gets the info 
            """
            driver.get(data_aqua.URL)
            time.sleep(5)
            set_destination_filters(driver) # Sets the first filters of the page
            driver.find_element(By.XPATH, data_aqua.MONTH_SELECTOR_PATH).click()
            time.sleep(2)
    
            months = driver.find_element(By.XPATH, data_aqua.MONTHS_PATH.format(indicador, year_number, month))
            months.click()
            time.sleep(2)
            
            set_suite(driver)
            search(driver)
                
            month += 1
            time.sleep(5)
            
            
            get_dates_info(driver)
            
        
        except:
            #print(f'Failed on: {month}')
            month += 1
            pass
            #indicador = 5
            #year_number += 1
            #month = 1


    get_data_2024(driver)

def get_data_2024(driver):
    month = 1
    for i in range(12):
        try:
            driver.get(data_aqua.URL)
            time.sleep(5)
            set_destination_filters(driver) # Sets the first filters of the page
            driver.find_element(By.XPATH, data_aqua.MONTH_SELECTOR_PATH).click()
            time.sleep(2)
        
            year_2024 = driver.find_element(By.XPATH, data_aqua.YEAR_2024_PATH)
            year_2024.click()
            time.sleep(2)
        
            months = driver.find_element(By.XPATH, data_aqua.MONTHS_PATH.format(3, 2, month))
            months.click()
            time.sleep(2)
            
            set_suite(driver)
            search(driver)
                
            month += 1
            time.sleep(5)
            
            get_dates_info(driver)
            
            
        except:
            month += 1
            pass
                    
def set_destination_filters(driver):
    """
    Sets first filters of the page and leaves it ready for automation of date picking
    """
    driver.find_element(By.XPATH, data_aqua.DESTINATION_SELECTOR_PATH).click()
    time.sleep(1)
    driver.find_element(By.XPATH, data_aqua.GALAPAGOS_PATH).click()
    time.sleep(1)

def set_suite(driver):
    cabin_selector = driver.find_element(By.XPATH, data_aqua.SUITE_SELECTOR_PATH)
    cabin_selector.click()
    time.sleep(3)
    cabin = driver.find_element(By.XPATH, data_aqua.SUITE_SPECIFIC_PATH)
    cabin.click()
    
    """
    try:
        month_selector = driver.find_element(By.XPATH, data_aqua.MONTH_SELECTOR_PATH)
        month_selector.click()
        time.sleep(5)
    except:
        print('Falló dentro de set_suite')
    """
        

def search(driver):
    search_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/main/div[2]/div/div[1]/div/form/div[4]/div/button')
    search_button.click()
    time.sleep(2)

def get_dates_info(driver):
    
    time.sleep(3)
    
    tour_indicator = 1 # Goes tour-by-tour
    date_indicator = 2 # Goes day-by-day on each tour
    

    for i in range(20):   
        try:    
                tour = driver.find_element(By.XPATH, data_aqua.DATES_PATH_GENERAL.format(tour_indicator, date_indicator))

                clean_date(tour.get_attribute('innerHTML'))
                get_price(driver, tour_indicator)
                get_availability(tour.get_attribute('innerHTML'))
                
                date_indicator += 1
        except:
            tour_indicator += 1
            date_indicator = 2
            
    

def clean_date(date_string):
    try:
        date = date_string.split('>')[6]
        date = date.split('<')[0].strip()
        #print('\n', date)
        set_departure_and_arrival(date)
    except:
        print('Not able to get date')

def set_departure_and_arrival(date_string):
    departure = date_string.split('-')[0].strip()
    arrival = date_string.split('-')[1].strip()
    year = arrival.split(' ')[2]
    
    if 'Dec' in departure and 'Jan' in arrival:
        """
        Takes in consideration tours that start on one year and end on another year
        """
        year = str(int(year) - 1)
    
    departure = departure + ' ' + year
    
    departure = format_date(departure)
    arrival = format_date(arrival)
    
    data_aqua.DEPARTURE_DATES.append(departure) # Stores dates in lists for JSON file
    data_aqua.ARRIVAL_DATES.append(arrival)
    
    
    #print('Departure: ', departure)
    #print('Arrival: ', arrival)
    
def format_date(string_date):
    date = str(datetime.strptime(string_date, '%d %b %Y').date())
    return date

def get_price(driver, tour_indicator):
    price = driver.find_element(By.XPATH, data_aqua.PRICE_PATH_GENERAL.format(tour_indicator)).get_attribute('innerHTML').strip()
    data_aqua.PRICES.append(price)
    #print('price: ', price)

def get_availability(tour_info):
    if 'Sold out!' in tour_info:
        data_aqua.AVAILABILITIES.append(0)
        #print('Availability: 0')
    elif 'Last suite!' in tour_info:
        data_aqua.AVAILABILITIES.append(2)
        #print('Availability: 2')
    elif 'Last 2 suites!' in tour_info:
        data_aqua.AVAILABILITIES.append(4)
        #print('Availability: 4')
    elif 'Selling fast!' in tour_info:
        data_aqua.AVAILABILITIES.append(4)
        #print('Availability: 4')
    elif 'Few suites left!' in tour_info:
        data_aqua.AVAILABILITIES.append(6)
        #print('Availability: 6')
    else:
        data_aqua.AVAILABILITIES.append(8)
        #print('Availability: 8')
    
def create_json():
    
    COMPLETE_JSON['84'] = {}
    
    COMPLETE_JSON['84']['705'] = {
        'boat' : 84,
        'cabin' : 705,
        'departures' : []
        }
    
    if len(data_aqua.DEPARTURE_DATES) == len(data_aqua.ARRIVAL_DATES) == len(data_aqua.PRICES) == len(data_aqua.AVAILABILITIES):
        
        for i in range(len(data_aqua.DEPARTURE_DATES)):
            dict_departures_temp = {}
            
            dict_departures_temp['departure_date'] = data_aqua.DEPARTURE_DATES[i]
            dict_departures_temp['arrival_date'] = data_aqua.ARRIVAL_DATES[i]
            dict_departures_temp['days'] = get_days(data_aqua.DEPARTURE_DATES[i], data_aqua.ARRIVAL_DATES[i])
            dict_departures_temp['available'] = data_aqua.AVAILABILITIES[i]
            dict_departures_temp['hold'] = 0
            dict_departures_temp['adult_price'] = process_price(data_aqua.PRICES[i])
            dict_departures_temp['promotion_name'] = 'season price'
            
            if dict_departures_temp['available'] != 0:
                COMPLETE_JSON['84']['705']['departures'].append(dict_departures_temp)
            
    else:
        print('\n*** ERROR creating JSON file')
        
      
def get_days(dep, arr):
    departure = datetime.strptime(dep, '%Y-%m-%d')
    arrival = datetime.strptime(arr, '%Y-%m-%d')
    diff = arrival - departure
    return diff.days + 1
      
def process_price(price):
    price_formatted = price.split('$')[1]
    price_formatted = price_formatted.split(',')
    price_formatted = price_formatted[0] + price_formatted[1]
    return int(price_formatted)
      
        
      
        
      
        
        
        
        
        
        
        
        








