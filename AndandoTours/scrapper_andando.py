from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from datetime import timedelta

import time
import data_andando
from data_andando import COMPLETE_JSON

def click_on_element_by_path(driver, path):
    time.sleep(5)
    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '{}'.format(path))))\
        .perform()
    
def click_on_element_by_class_name(driver, class_name):
    time.sleep(5)
    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.CLASS_NAME,
                                           '{}'.format(class_name))))\
        .click()
        
def prepare_frame_info(driver):
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))
    
def get_all_rows_info(driver):
    rows = driver.find_elements(By.CLASS_NAME, 'container')
    for i in range(len(rows) - 1):
        get_dates(rows[i])

def get_dates(rows):
    row = rows.get_attribute('innerHTML')
    row = row.split('>')

    """
    DATES
    """
    dates = row[10]
    dates = dates.split('<')[0]
    dates = dates.strip()
    process_dates(dates)
    
    """
    DAYS
    """
    days = row[14].strip()
    days = int(days.split(' ')[0])
    data_andando.DAYS.append(days)
    
    """
    AVAILABILITY
    """
    availability = row[30].strip()
    availability = availability.split('<')
    availability = int(availability[0])
    data_andando.AVAILABILITIES.append(availability)
    
    """
    PRICE
    """
    price = row[41].strip()
    price = price.split('<')[0]
    process_price(price)
    

def process_dates(date):
    date_formatted = datetime.strptime(date, '%a, %d %b %Y').date()
    data_andando.DATES.append(str(date_formatted))
    

def process_price(price):
    try:
        price_formatted = price.split('$')[1]
        price_formatted = price_formatted.split(',')
        price_formatted = price_formatted[0] + price_formatted[1]
        price_formatted = price_formatted.split('.')[0]
        data_andando.PRICES.append(price_formatted)
    except:
        data_andando.PRICES.append(None)
        
def get_arrival_dates():
    if len(data_andando.DATES) == len(data_andando.DAYS):
        for i in range(len(data_andando.DATES)):
            date = data_andando.DATES[i]
            date = datetime.strptime(date, '%Y-%m-%d').date()
            days_to_add = int(data_andando.DAYS[i]) - 1
            temp = str(date + timedelta(days=days_to_add))
            #print('{}\t\t{}'.format(date, temp))
            data_andando.ARRIVAL_DATES.append(temp)
            
            #print('{}\t\t{}'.format(i+1, len(data_andando.ARRIVAL_DATES)))
            

def create_json(i):
    if i == 0:
        if '12' not in COMPLETE_JSON.keys():
            COMPLETE_JSON['12'] = {
                '703' : {
                    'boat' : 12,
                    'cabin' : 703,
                    'departures' : []
                    }
                }
            
        if len(data_andando.DATES) == len(data_andando.DAYS) == len(data_andando.AVAILABILITIES) == len(data_andando.PRICES):
            for k in range(len(data_andando.DATES)):
                dict_departures_temp = {
                    'departure_date' : None,
                    'arrival_date' : None,
                    'days' : None,
                    'available' : None,
                    'hold' : 0
                    }
                
                dict_departures_temp['departure_date'] = data_andando.DATES[k]
                dict_departures_temp['arrival_date'] = data_andando.ARRIVAL_DATES[k]
                dict_departures_temp['days'] = data_andando.DAYS[k]
                dict_departures_temp['available'] = data_andando.AVAILABILITIES[k]
                
                if data_andando.PRICES[k] != None:
                    dict_departures_temp['adult_price'] = data_andando.PRICES[k]
                    dict_departures_temp['promotion_name'] = 'season price'
        
                COMPLETE_JSON['12']['703']['departures'].append(dict_departures_temp)
                
    else:
        if '13' not in COMPLETE_JSON.keys():
            COMPLETE_JSON['13'] = {
                '704' : {
                    'boat' : 13,
                    'cabin' : '704',
                    'departures' : []
                    }
                }
            
        if len(data_andando.DATES) == len(data_andando.DAYS) == len(data_andando.AVAILABILITIES) == len(data_andando.PRICES):
            for k in range(len(data_andando.DATES)):
                dict_departures_temp = {
                    'departure_date' : None,
                    'arrival_date' : None,
                    'days' : None,
                    'available' : None,
                    'hold' : 0
                    }
                
                dict_departures_temp['departure_date'] = data_andando.DATES[k]
                dict_departures_temp['arrival_date'] = data_andando.ARRIVAL_DATES[k]
                dict_departures_temp['days'] = data_andando.DAYS[k]
                dict_departures_temp['available'] = data_andando.AVAILABILITIES[k]
                
                if data_andando.PRICES[k] != None:
                    dict_departures_temp['adult_price'] = data_andando.PRICES[k]
                    dict_departures_temp['promotion_name'] = 'season price'
        
                COMPLETE_JSON['13']['704']['departures'].append(dict_departures_temp)
                
        

    
def empty_lists():
    data_andando.DATES = []
    data_andando.DAYS = []
    data_andando.AVAILABILITIES = []
    data_andando.PRICES = []
    data_andando.ARRIVAL_DATES = []





























