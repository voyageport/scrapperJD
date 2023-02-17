from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from data_nemo import COMPLETE_JSON


import time
import data_nemo
import string
import re
import requests
import json



def click_on_element_by_path(driver, path):
    time.sleep(5)
    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '{}'.format(path))))\
        .click()
    
def click_on_element_by_class_name(driver, class_name):
    time.sleep(5)
    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.CLASS_NAME,
                                           '{}'.format(class_name))))\
        .click()

def get_dates(driver):    
    try:
        i = 1
        data_nemo.ALL_DATES = []
        while True:
            data_nemo.ALL_DATES.append(driver.find_element(By.XPATH, data_nemo.DATES_PATH.format(i)).get_attribute('innerHTML'))
            i += 1
    except:
        print('', end='')

    clean_dates()

def clean_dates():
    for i in range(len(data_nemo.ALL_DATES)):
        start_date = data_nemo.ALL_DATES[i]
        start_date = start_date.split('From:</strong> ')[1]
        start_date = start_date.split('<')[0]
        start_date = start_date.split(' ')[1]
        start_date = format_dates(start_date)
        
        end_date = data_nemo.ALL_DATES[i]
        end_date = end_date.split('To:</strong> ')[1]
        end_date = end_date.split('<')[0]
        end_date = end_date.split(' ')[1]
        end_date = format_dates(end_date)
        
        get_days(start_date, end_date)
        
        data_nemo.START_DATES.append(str(start_date))
        data_nemo.END_DATES.append(str(end_date))
        

def format_dates(date):
    return datetime.strptime(date, '%d-%b-%Y').date()

def get_days(start_date, end_date):
    difference = str(end_date - start_date)
    difference = int(difference.split(' ')[0]) + 1
    
    data_nemo.DAYS.append(difference)
    #print('Start: {}\tEnd: {}\tDays: {}'.format(start_date, end_date, difference))
    
def get_availabilities(driver):
    availabilities_temp = driver.find_elements(By.CLASS_NAME, data_nemo.AVAILABILITY_CLASS_NAME)

    #print('len availabilities: {}\n\n'.format(len(availabilities_temp)))
    
    for i in range(len(availabilities_temp)):
        data_nemo.AVAILABILITIES.append(availabilities_temp[i].get_attribute('innerHTML'))

def get_boat_name(driver):
    try:
        i = 1
        while True:
            boat_name = driver.find_element(By.XPATH, data_nemo.BOAT_NAME_PATH.format(i)).get_attribute('innerHTML')
            boat_name = clean_boat_names(boat_name)
            data_nemo.ALL_BOAT_NAMES.append(boat_name)
            i += 1
    except:
        print('', end='')

        
def clean_boat_names(boat_name):
    try: 

        temp = boat_name
        temp = temp.split('-')[0]
        temp = data_nemo.BOAT_NAME_FROM_CODE[temp]
    
    
        create_boat_in_json(temp)
        
        temp = data_nemo.BOATS[temp]
        
        return temp
    except:
        print('Failed in clean_boat_names')
        
def create_boat_in_json(boat):
    
    boat_id = data_nemo.BOATS[boat]
    
    if boat_id not in data_nemo.COMPLETE_JSON.keys():
        data_nemo.COMPLETE_JSON[boat_id] = {}
        
        cabin_id = data_nemo.CABINS[str(boat_id)]
        
        data_nemo.COMPLETE_JSON[boat_id][cabin_id] = {
            'boat' : boat_id,
            'cabin' : cabin_id,
            'departures' : []
            }
        
        # *** CONTINUAR CON LOS CABIN IDS


def create_json():
    if len(data_nemo.ALL_BOAT_NAMES) != len(data_nemo.START_DATES) != len(data_nemo.END_DATES) != data_nemo.AVAILABILITIES != data_nemo.DAYS:
        print('Error getting information')
        0/0
    else:
        #print('\t\tlen ALL_BOAT_NAMES:', len(data_nemo.ALL_BOAT_NAMES))
        #print('\t\tlen START_DATES:', len(data_nemo.START_DATES))
        #print('\t\tlen END_DATES:', len(data_nemo.END_DATES))
        #print('\t\tlen AVAILABILITIES:', len(data_nemo.AVAILABILITIES))
        for i in range(len(data_nemo.ALL_BOAT_NAMES)):
            boat_name = data_nemo.ALL_BOAT_NAMES[i]
            cabin_id = data_nemo.CABINS[str(boat_name)]
            dict_departures_temp = {
                'departure_date' : data_nemo.START_DATES[i],
                'arrival_date' : data_nemo.END_DATES[i],
                'days' : data_nemo.DAYS[i],
                'available' : int(data_nemo.AVAILABILITIES[i]),
                'hold' : 0
                }
            data_nemo.COMPLETE_JSON[boat_name][cabin_id]['departures'].append(dict_departures_temp)
            

def empty_lists():
    data_nemo.ALL_BOAT_NAMES = []
    data_nemo.START_DATES = []
    data_nemo.END_DATES = []
    data_nemo.AVAILABILITIES = []























