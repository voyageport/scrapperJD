from selenium.webdriver.common.by import By
from datetime import datetime
from dateutil.relativedelta import relativedelta
from data_galagents import COMPLETE_JSON
from data_galagents import CABINS_ID_WEB


import time
import data_galagents
import json


def format_date_for_search(indicator):
    """
    Returns the dates for search
    indicator == 'start' returns today's date
    indicator != 'start' returns today's date + 1 month (change to 'years' if desired)
    """
    if indicator == 'start':
        date = datetime.today().date()

    else:
        date2 = datetime.today().date()
        date = date2 + relativedelta(years=2)

    date_formatted = datetime.strftime(date, '%Y-%m-%d')
    return str(date_formatted)
    

def format_date_for_json(date):
    date_formatted = datetime.strftime(date, '%d-%m-%Y')
    return date_formatted

def get_info(driver):
    start_date = format_date_for_search('start')
    end_date = format_date_for_search('end')
    print('Getting info...')
    for i in range(data_galagents.NUMBER_OF_BOATS):
        driver.get(data_galagents.URL.format(i+1, start_date, end_date))
        all_data = driver.find_element(By.XPATH, "/html/body").text
        
        all_data = json.loads(all_data)
        # Keys: ['success', 'data']
        
        if all_data['success'] == True:
            print('\tInfo recieved from {}'.format(data_galagents.BOATS_NAMES_DICT[str(i+1)]))
            process_json_info(all_data) # Method that processes all data 
        else:
            print('Error obtaining data from {}'.format(data_galagents.BOATS_NAMES_DICT[str(i+1)]))
        time.sleep(3)    


def process_json_info(all_data):
    # Keys for all_data: ['success', 'data']
    # Keys for all_data['data']: ['name', 'data']
    boat_name = all_data['data']['name']
    #print('Boat: ', boat_name)
    boat_to_json(boat_name)
    # Keys for all_data['data']['data']: 
    #print(all_data['data']['name'], end='\n\n')
    
    for i in range(len(all_data['data']['data'])): # Gets info for every itinerary/dates on the boat 
        # Keys for all_data['data']['data'][i]: ['name', 'date_start', 'date_end', 'price', 'obsrevation', 'promo_price', 'promo_date', 'promo_flag', 'free', 'hold', 'cabin']
    
        start_date = all_data['data']['data'][i]['date_start']
        end_date = all_data['data']['data'][i]['date_end']
        date_difference = get_dates_difference(start_date, end_date)
        price = all_data['data']['data'][i]['price']
        promotion_description = all_data['data']['data'][i]['obsrevation'] # It's misspelled in the GDS
        price_promotion = all_data['data']['data'][i]['promo_price']
        availability = all_data['data']['data'][i]['free']
        hold = all_data['data']['data'][i]['hold']
        cabins_available_list = all_data['data']['data'][i]['cabin'] # Gives the cabins that are available
        cabin_id = CABINS_ID_WEB[boat_name]['All boat']
        
        
        cabin_to_json(boat_name, cabin_id) # Inclusion of the cabin type to the JSON file
        
        #print('*** ID All: ', cabin_id)
        
        dict_departures_temp = {}
        
        dict_departures_temp['departure_date'] = start_date
        dict_departures_temp['arrival_date'] = end_date
        dict_departures_temp['days'] = date_difference
        dict_departures_temp['available'] = availability
        dict_departures_temp['hold'] = hold
        if price_promotion == None:
            dict_departures_temp['adult_price'] = price
        else:
            dict_departures_temp['adult_price'] = price_promotion
        dict_departures_temp['promotion_type'] = 'promotion'
        dict_departures_temp['promotion_name'] = 'season price'
        dict_departures_temp['promotion_description'] = promotion_description
        dict_departures_to_json(dict_departures_temp, boat_name, cabin_id)
        
        
        

        #print(all_data['data']['data'][i], end = '\n\n')
        """
        print('start_date: ', start_date)
        print('end_date: ', end_date)
        print('date_difference: ', date_difference)
        print('price: ', price)
        print('promotion_description: ', promotion_description)
        print('price_promotion: ', price_promotion)
        print('availability: ', availability)
        print('hold: ', hold)
        print('cabins_available_list: ', cabins_available_list, end='\n\n')

        print(COMPLETE_JSON)
        """
         
    
        
        #print(dict_departures_temp, end='\n\n')
        #dict_departures_to_json(dict_departures_temp, boat_name, cabin_id)
        
        
def boat_to_json(boat_name):
    boat_id = data_galagents.BOATS_INTERNAL_IDS[boat_name]
    if boat_id not in COMPLETE_JSON.keys():
        #print('Bote creado en JSON')
        COMPLETE_JSON[str(boat_id)] = {}
    
def cabin_to_json(boat_name, cabin_id):
    boat_id = data_galagents.BOATS_INTERNAL_IDS[boat_name]
    if str(cabin_id) not in COMPLETE_JSON[str(boat_id)].keys():
        #print('\n***ENTRÓ***\n')
        COMPLETE_JSON[str(boat_id)][str(cabin_id)] = {
                'boat' : boat_id,
                'cabin' : cabin_id,
                'departures' : []
            }
    
def dict_departures_to_json(dict_departures, boat_name, cabin_id):
    boat_id = data_galagents.BOATS_INTERNAL_IDS[boat_name]
    #print(' ** Entró: ', dict_departures)
    COMPLETE_JSON[str(boat_id)][str(cabin_id)]['departures'].append(dict_departures)
    
    

def get_dates_difference(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    difference = end - start
    return int(difference.days)+1




































'''
********************************************************************************
********************************************************************************
*********************** SCRAPING DE LA PÁGINA (25% DONE) ***********************
********************************************************************************
********************************************************************************


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
        
def send_info_to_element_by_path(driver, path, text, flag):
    """
    flag indicates if return key is sent
    """
    element = driver.find_element(By.XPATH, path)
    element.send_keys(text)
    time.sleep(1)
    if flag == True:
        element.send_keys(Keys.RETURN)
    
        
def close_chat_bot(driver):
    try:
        click_on_element_by_path(driver,data_galagents.CHAT_BOT_CLOSE_PATH)
    except:
        print('Not able to close chat bot')
        

def search_filters_manipulation(driver):
    """
    Sets the search filters to obtain info
    """
    time.sleep(3)
    # Selecting 'All Cruises'
    click_on_element_by_path(driver, data_galagents.CRUISE_SELECTOR_PATH) 
    click_on_element_by_path(driver, data_galagents.SELECT_ALL_CRUISES_PATH)
    
    # Selecting 'Start Date' & 'End Date'
    send_info_to_element_by_path(driver, data_galagents.START_DATE_PATH, format_date_for_search('start'), False)
    time.sleep(2)
    send_info_to_element_by_path(driver, data_galagents.END_DATE_PATH, format_date_for_search('end'), False)
    
    # Selecting Number of Passengers
    send_info_to_element_by_path(driver, data_galagents.PASSENGERS_PATH, data_galagents.NUMBER_OF_PASSENGERS, True)

    time.sleep(5) # Time to wait for search to be completed

def get_data(driver):
    
    for i in range(data_galagents.TOTAL_CRUISES):
        """
        Getting boat name and ID
        """
        boat_name = driver.find_element(By.XPATH, data_galagents.CRUISE_NAME_PATH.format(i+1)).get_attribute('innerHTML')
        boat_id = data_galagents.BOATS_INTERNAL_IDS[boat_name]
        print('\n{}\t\t{}'.format(boat_name, boat_id))
        """
        Getting the dates
        """
        flag = True
        j = 1
        while flag == True:
            try:
                date = driver.find_element(By.XPATH, data_galagents.DATES_PATH_GENERAL.format((i+1)*2, j+1)).get_attribute('innerHTML')
                print(date)
                j += 1
            except:
                flag = False
                print('\n')
    
'''