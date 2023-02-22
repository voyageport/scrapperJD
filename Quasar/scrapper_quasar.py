from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from data_quasar import COMPLETE_JSON


import time
import data_quasar
import string
import re
import requests
import json

def get_dates(driver):
    for i in range(2):
        if i == 0:
            path = data_quasar.START_DATE_PATH_GENERAL
        else:
            path = data_quasar.END_DATE_PATH_GENERAL
        
        try:
            j = 0
            prev = ''
            while True:
                date = driver.find_element(By.XPATH, path.format(17+j)).get_attribute('innerHTML')
                for month in data_quasar.MONTHS:
                    if month in date and date != prev:
                        if i == 0:
                            date = format_dates(date)
                            data_quasar.START_DATES.append(date)
                        else:
                            date = format_dates(date)
                            data_quasar.END_DATES.append(date)
                        prev = date
                        
                j += 1
        except:
            print('', end = '')
            
        #print('len start: ', len(data_quasar.START_DATES))
        #print('len end: ', len(data_quasar.END_DATES))
        
    if len(data_quasar.START_DATES) != len(data_quasar.END_DATES):
        print('\n***ERROR: not able to get all dates')
        quit()
    else:
        pass
        #print_dates()

def print_dates():
    for i in range(len(data_quasar.START_DATES)):
        print('{}\t\t{}'.format(data_quasar.START_DATES[i], data_quasar.END_DATES[i]))

def format_dates(date):
    date_formatted = datetime.strptime(date, '%d-%b-%y')
    date_formatted = datetime.strftime(date_formatted, '%Y-%m-%d')
    return date_formatted

def get_availabilities(driver , path):
    try:
        i = 18
        #prev = ''
        while True:
            availability = driver.find_element(By.XPATH, path.format(i)).get_attribute('innerHTML')
            try:
                availability = int(availability)
                data_quasar.AVAILABILITIES.append(availability)
            except:
                print('', end = '')
                
            
            i += 1
    except:
        print('', end = '')

    if len(data_quasar.AVAILABILITIES) != len(data_quasar.START_DATES):
        print('\n***ERROR: not able to get all availabilities')

    """
    Prints len() and all availabilities

    for i in range(len(data_quasar.AVAILABILITIES)):
        print('{}. {}'.format(i+1, data_quasar.AVAILABILITIES[i]))
    print('\nlen availabilities: ', len(data_quasar.AVAILABILITIES))
    """


def get_prices(driver, path, boat):
    if boat == 'Grace':
        try:
            i = 18
            while True:
                price_GKS = driver.find_element(By.XPATH, path.format(i, 2)).get_attribute('innerHTML')
                if '-' == price_GKS or '$' in price_GKS:
                    #print(price_GKS, end = '\t')
                    data_quasar.PRICES_GKS.append(price_GKS)
                price_A1 = driver.find_element(By.XPATH, path.format(i, 3)).get_attribute('innerHTML')
                if '-' == price_A1 or '$' in price_A1:
                    data_quasar.PRICES_A1.append(price_A1)
                    #print(price_A1, end = '\t')
                price_A2 = driver.find_element(By.XPATH, path.format(i, 4)).get_attribute('innerHTML')
                if '-' == price_A2 or '$' in price_A2:
                    data_quasar.PRICES_A2.append(price_A2)
                    #print(price_A2, end = '\n')
                price_A3 = driver.find_element(By.XPATH, path.format(i, 5)).get_attribute('innerHTML')
                if '-' == price_A3 or '$' in price_A3:
                    data_quasar.PRICES_A3.append(price_A3)
                    #print(price_A3, end = '\t')
                price_A4 = driver.find_element(By.XPATH, path.format(i, 6)).get_attribute('innerHTML')
                if '-' == price_A4 or '$' in price_A4:
                    data_quasar.PRICES_A4.append(price_A4)
                    #print(price_A4, end = '\t')
                price_C1 = driver.find_element(By.XPATH, path.format(i, 7)).get_attribute('innerHTML')
                if '-' == price_C1 or '$' in price_C1:
                    data_quasar.PRICES_C1.append(price_C1)
                    #print(price_C1, end = '\t')
                price_C2 = driver.find_element(By.XPATH, path.format(i, 8)).get_attribute('innerHTML')
                if '-' == price_C2 or '$' in price_C2:
                    data_quasar.PRICES_C2.append(price_C2)
                    #print(price_C2, end = '\t')
                price_C3 = driver.find_element(By.XPATH, path.format(i, 9)).get_attribute('innerHTML')
                if '-' == price_C3 or '$' in price_C3:
                    data_quasar.PRICES_C3.append(price_C3)
                    #print(price_C3, end = '\t')
                price_C5 = driver.find_element(By.XPATH, path.format(i, 10)).get_attribute('innerHTML')
                if '-' == price_C5 or '$' in price_C5:
                    data_quasar.PRICES_C5.append(price_C5)
                    #print(price_C5, end = '\n\n')
                
                i += 1
        except:
            print('', end = '')
        
        """
        print('len GKS: ', len(data_quasar.PRICES_GKS))
        print('len A1: ', len(data_quasar.PRICES_A1))
        print('len A2: ', len(data_quasar.PRICES_A2))
        print('len A3: ', len(data_quasar.PRICES_A3))
        print('len A4: ', len(data_quasar.PRICES_A4))
        print('len C1: ', len(data_quasar.PRICES_C1))
        print('len C2: ', len(data_quasar.PRICES_C2))
        print('len C3: ', len(data_quasar.PRICES_C3))
        print('len C5: ', len(data_quasar.PRICES_C5))
        """
    
    elif boat == 'Evolution':
        try:
            i = 18
            while True:
                price_A1 = driver.find_element(By.XPATH, data_quasar.PRICES_GENERAL_PATH_EVOLUTION.format(i, 2)).get_attribute('innerHTML')
                if '-' == price_A1 or '$' in price_A1:
                    #print(price_A1, end='\t')
                    data_quasar.PRICES_A1.append(price_A1)
                
                price_A2 = driver.find_element(By.XPATH, data_quasar.PRICES_GENERAL_PATH_EVOLUTION.format(i, 3)).get_attribute('innerHTML')
                if '-' == price_A2 or '$' in price_A2:
                    #print(price_A2, end='\t')
                    data_quasar.PRICES_A2.append(price_A2)
                
                price_A3 = driver.find_element(By.XPATH, data_quasar.PRICES_GENERAL_PATH_EVOLUTION.format(i, 4)).get_attribute('innerHTML')
                if '-' == price_A3 or '$' in price_A3:
                    #print(price_A3, end='\t')
                    data_quasar.PRICES_A3.append(price_A3)
                
                price_C1 = driver.find_element(By.XPATH, data_quasar.PRICES_GENERAL_PATH_EVOLUTION.format(i, 5)).get_attribute('innerHTML')
                if '-' == price_C1 or '$' in price_C1:
                    #print(price_C1, end='\t')
                    data_quasar.PRICES_C1.append(price_C1)
                
                price_C2 = driver.find_element(By.XPATH, data_quasar.PRICES_GENERAL_PATH_EVOLUTION.format(i, 6)).get_attribute('innerHTML')
                if '-' == price_C2 or '$' in price_C2:
                    #print(price_C2, end='\t')
                    data_quasar.PRICES_C2.append(price_C2)
                
                price_C3 = driver.find_element(By.XPATH, data_quasar.PRICES_GENERAL_PATH_EVOLUTION.format(i, 7)).get_attribute('innerHTML')
                if '-' == price_C3 or '$' in price_C3:
                    #print(price_C3, end='\t')
                    data_quasar.PRICES_C3.append(price_C3)
                
                price_C4 = driver.find_element(By.XPATH, data_quasar.PRICES_GENERAL_PATH_EVOLUTION.format(i, 8)).get_attribute('innerHTML')
                if '-' == price_C4 or '$' in price_C4:
                    #print(price_C4, end='\t')
                    data_quasar.PRICES_C4.append(price_C4)
                
                price_C5 = driver.find_element(By.XPATH, data_quasar.PRICES_GENERAL_PATH_EVOLUTION.format(i, 9)).get_attribute('innerHTML')
                if '-' == price_C5 or '$' in price_C5:
                    #print(price_C5, end='\t')
                    data_quasar.PRICES_C5.append(price_C5)
                
                price_C6 = driver.find_element(By.XPATH, data_quasar.PRICES_GENERAL_PATH_EVOLUTION.format(i, 10)).get_attribute('innerHTML')
                if '-' == price_C6 or '$' in price_C6:
                    #print(price_C6, end='\t')
                    data_quasar.PRICES_C6.append(price_C6)
                
                price_C7 = driver.find_element(By.XPATH, data_quasar.PRICES_GENERAL_PATH_EVOLUTION.format(i, 11)).get_attribute('innerHTML')
                if '-' == price_C7 or '$' in price_C7:
                    #print(price_C7, end='\t')
                    data_quasar.PRICES_C7.append(price_C7)
                
                price_C8 = driver.find_element(By.XPATH, data_quasar.PRICES_GENERAL_PATH_EVOLUTION.format(i, 12)).get_attribute('innerHTML')
                if '-' == price_C8 or '$' in price_C8:
                    #print(price_C8, end='\t')
                    data_quasar.PRICES_C8.append(price_C8)
                
                price_C9 = driver.find_element(By.XPATH, data_quasar.PRICES_GENERAL_PATH_EVOLUTION.format(i, 13)).get_attribute('innerHTML')
                if '-' == price_C9 or '$' in price_C9:
                    #print(price_C9, end='\t')
                    data_quasar.PRICES_C9.append(price_C9)
                
                price_D1 = driver.find_element(By.XPATH, data_quasar.PRICES_GENERAL_PATH_EVOLUTION.format(i, 14)).get_attribute('innerHTML')
                if '-' == price_D1 or '$' in price_D1:
                    #print(price_D1, end='\t')
                    data_quasar.PRICES_D1.append(price_D1)
                
                price_D2 = driver.find_element(By.XPATH, data_quasar.PRICES_GENERAL_PATH_EVOLUTION.format(i, 15)).get_attribute('innerHTML')
                if '-' == price_D2 or '$' in price_D2:
                    #print(price_D2, end='\t')
                    data_quasar.PRICES_D2.append(price_D2)
                
                price_D3 = driver.find_element(By.XPATH, data_quasar.PRICES_GENERAL_PATH_EVOLUTION.format(i, 16)).get_attribute('innerHTML')
                if '-' == price_D3 or '$' in price_D3:
                    #print(price_D3, end='\t')
                    data_quasar.PRICES_D3.append(price_D3)
                
                price_D4 = driver.find_element(By.XPATH, data_quasar.PRICES_GENERAL_PATH_EVOLUTION.format(i, 17)).get_attribute('innerHTML')
                if '-' == price_D4 or '$' in price_D4:
                    #print(price_D4, end='\n')
                    data_quasar.PRICES_D4.append(price_D4)

                i+=1
        except:
            print('', end = '')
            

def get_hold(driver, path):
    try:
        i = 18
        #prev = ''
        while True:
            holds = driver.find_element(By.XPATH, path.format(i)).get_attribute('innerHTML')
            try:
                holds = int(holds)
                data_quasar.HOLDS.append(holds)
                #print('Inside try: ', holds)
            except:
                print('', end = '')
                
            
            i += 1
    except:
        print('', end = '')
    
    """
    print(len(data_quasar.HOLDS))
    
    for i in range(len(data_quasar.HOLDS)):
        print('{}. {}'.format(i+1, data_quasar.HOLDS[i]))
    """

def get_charter_promo(driver, path):
    try:
        i = 18
        while True:
            charter_price = driver.find_element(By.XPATH, path.format(i)).get_attribute('innerHTML')
            if '$' in charter_price or '-' in charter_price:
                #print(charter_price)
                data_quasar.CHARTER_PRICES.append(charter_price)
            i += 1
    except:
        pass
    
    #print('\n\n', len(data_quasar.CHARTER_PRICES))

def create_json(boat):
    if boat == 'Grace':
        if len(data_quasar.START_DATES) == len(data_quasar.END_DATES) == len(data_quasar.AVAILABILITIES) == len(data_quasar.HOLDS):
            COMPLETE_JSON['67'] = {}
            COMPLETE_JSON['67']['690'] = {
                'boat' : 67,
                'cabin' : 690,
                'departures' : []
                }
            
            
            for i in range(len(data_quasar.START_DATES)):
                dict_departures_temp = {}
                dict_departures_temp['departure_date'] = data_quasar.START_DATES[i]
                dict_departures_temp['arrival_date'] = data_quasar.END_DATES[i]
                dict_departures_temp['days'] = get_days(data_quasar.START_DATES[i], data_quasar.END_DATES[i])
                dict_departures_temp['available'] = data_quasar.AVAILABILITIES[i]
                dict_departures_temp['hold'] = data_quasar.HOLDS[i]
                
                if dict_departures_temp['available'] != 0:
                    COMPLETE_JSON['67']['690']['departures'].append(dict_departures_temp)
            
        else:
            print('ERROR creating JSON file')
    
    elif boat == 'Evolution': 
        if len(data_quasar.START_DATES) == len(data_quasar.END_DATES) == len(data_quasar.AVAILABILITIES) == len(data_quasar.HOLDS):
            COMPLETE_JSON['69'] = {}
            COMPLETE_JSON['69']['699'] = {
                'boat' : 69,
                'cabin' : 699,
                'departures' : []
                }
            
            
            for i in range(len(data_quasar.START_DATES)):
                dict_departures_temp = {}
                dict_departures_temp['departure_date'] = data_quasar.START_DATES[i]
                dict_departures_temp['arrival_date'] = data_quasar.END_DATES[i]
                dict_departures_temp['days'] = get_days(data_quasar.START_DATES[i], data_quasar.END_DATES[i])
                dict_departures_temp['available'] = data_quasar.AVAILABILITIES[i]
                dict_departures_temp['hold'] = data_quasar.HOLDS[i]
                
                if dict_departures_temp['available'] != 0:
                    COMPLETE_JSON['69']['699']['departures'].append(dict_departures_temp)
            
        else:
            print('ERROR creating JSON file')
        
    


def get_days(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    difference = str(end_date - start_date)
    difference = int(difference.split(' ')[0]) + 1
    
    return int(difference)


def empty_lists():
    data_quasar.START_DATES = []
    data_quasar.END_DATES = []
    data_quasar.AVAILABILITIES = []
    data_quasar.HOLDS = []






    
    
