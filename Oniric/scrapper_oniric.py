from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from data_oniric import COMPLETE_JSON

import time
import data_oniric

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
        
def set_search_filters(driver):
    click_on_element_by_path(driver, data_oniric.DATE_SELECTOR_PATH) # Displays the date selector panel
    click_on_element_by_path(driver, data_oniric.START_DAY_PATH) # Clicks on the first day displayed
    for i in range(12):
        """
        Goes to a year in the future
        """
        click_on_element_by_class_name(driver, data_oniric.NEXT_MONTH_CLASS_NAME) # Clicks on the next month arrow
    click_on_element_by_path(driver, data_oniric.END_DAY_PATH) # Clicks on the last day displayed
    click_on_element_by_class_name(driver, data_oniric.REFRESH_BUTTON_CLASS_NAME) # Clicks on the refresh button to get results
    
def scroll_down(driver):
    """
    Scrolls to the end of infinite scroll
    """
    previous_height = driver.execute_script('return document.body.scrollHeight;')

    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(60)
        new_height = driver.execute_script('return document.body.scrollHeight;')
        
        if new_height == previous_height:
            break
        
        previous_height = new_height
        
def get_all_info_columns(driver):
    data_oniric.COLUMNS_INFO = driver.find_elements(By.CLASS_NAME, data_oniric.INFO_COLUMNS_CLASS_NAME)
    
def process_info():
    for i in range(len(data_oniric.COLUMNS_INFO)): # For iteration through all columns
    #for i in range(1):
        info = data_oniric.COLUMNS_INFO[i].get_attribute('innerHTML')
        """
        """
        boat_name = get_boat_name(info, i)
        get_dates(info, i, boat_name)
        get_availabilitie_and_hold(info, i, boat_name)
        get_prices(info, i, boat_name)
        
        
        
    
def get_boat_name(info, i):
    try:
        boat_name = info.split('span data-v-932536be')
        boat_name = boat_name[1]
        boat_name = boat_name.split('<')
        boat_name = boat_name[0]
        boat_name = boat_name.split('>')
        boat_name = boat_name[1]
        
        #if boat_name not in data_oniric.ALL_BOAT_NAMES:
        #    data_oniric.ALL_BOAT_NAMES.append(boat_name)
        return str(boat_name).strip()
    except:
        print('Not able to get boat name from column #', i+1)
    
    
def get_dates(info, i, boat_name):
    try:
        dates = info.split('departure col-sm-3')
        
        departure_date = dates[1]
        departure_date = departure_date.split('<')
        departure_date = departure_date[0]
        departure_date = departure_date.split('>')
        departure_date = departure_date[1]
        departure_date = departure_date.split('(')
        departure_date = departure_date[0].strip()
        departure_date = format_string_to_date(departure_date)
        data_oniric.DEPARTURE_DATES.append(departure_date)
        
        add_info_to_boat_list(boat_name, 'departure_date', departure_date)
        
        
        arrival_date = dates[2]
        arrival_date = arrival_date.split('<')
        arrival_date = arrival_date[0]
        arrival_date = arrival_date.split('>')
        arrival_date = arrival_date[1]
        arrival_date = arrival_date.split('(')
        arrival_date = arrival_date[0].strip()
        arrival_date = format_string_to_date(arrival_date)
        data_oniric.ARRIVAL_DATES.append(arrival_date)
        
        add_info_to_boat_list(boat_name, 'arrival_date', arrival_date)

        #print('Departure date: ', departure_date)
        #print('Arrival date: ', arrival_date, end = '\n')
    
    except:
        print('Not able to get departure or arrival date from column #', i+1)
    

def format_string_to_date(date):
    formatted_date = datetime.strptime(date, '%d %b %Y').date()
    return formatted_date

def get_availabilitie_and_hold(info, i, boat_name):
    try:
        data = info.split('null')
        availability = data[2]
        availability = availability.split('<')
        availability = availability[0]
        availability = availability.split('>')
        availability = availability[1].strip()
        data_oniric.AVAILABILITIES.append(availability)
        
        add_info_to_boat_list(boat_name, 'availability', availability)
        
        hold = data[3]
        hold = hold.split('<')
        hold = hold[0]
        hold = hold.split('>')
        hold = hold[1].strip()
        data_oniric.HOLD.append(hold)
        
        add_info_to_boat_list(boat_name, 'hold', hold)

        
        #print('availability: ', availability)
        #print('hold: ', hold, end = '\n\n')
    except:
        add_info_to_boat_list(boat_name, 'availability', 0)
        add_info_to_boat_list(boat_name, 'hold', 0)
        print('Not able to get availability from column #', i+1)


def get_prices(info, i, boat_name):
    try:
        price = info.split('rate col-sm-2')
        price = price[1]
        price = price.split('<')
        price = price[1]
        price = price.split('>')
        price = price[1].strip()
        data_oniric.PRICES.append(price)
        
        add_info_to_boat_list(boat_name, 'price', price)
        
        #print('price: ', price)
        
    except:
        add_info_to_boat_list(boat_name, 'price', 0)
        print('Not able to get price from column #', i+1)


def add_info_to_boat_list(boat_name, type_info, info):
    """
    Distributes information to its respective boat and list
    """    
    if boat_name == 'Solaris':
        if type_info == 'departure_date':
            data_oniric.DEPARTURE_DATES_SOLARIS.append(info)
        elif type_info == 'arrival_date':
            data_oniric.ARRIVAL_DATES_SOLARIS.append(info)
        elif type_info == 'availability':
            data_oniric.AVAILABILITIES_SOLARIS.append(info)
        elif type_info == 'hold':
            data_oniric.HOLD_SOLARIS.append(info)
        elif type_info == 'price':
            data_oniric.PRICES_SOLARIS.append(info)

    elif boat_name == 'Treasure':
        if type_info == 'departure_date':
            data_oniric.DEPARTURE_DATES_TREASURE.append(info)
        elif type_info == 'arrival_date':
            data_oniric.ARRIVAL_DATES_TREASURE.append(info)
        elif type_info == 'availability':
            data_oniric.AVAILABILITIES_TREASURE.append(info)
        elif type_info == 'hold':
            data_oniric.HOLD_TREASURE.append(info)
        elif type_info == 'price':
            data_oniric.PRICES_TREASURE.append(info)

    elif boat_name == 'Archipel I':
        if type_info == 'departure_date':
            data_oniric.DEPARTURE_DATES_ARCHIPEL.append(info)
        elif type_info == 'arrival_date':
            data_oniric.ARRIVAL_DATES_ARCHIPEL.append(info)
        elif type_info == 'availability':
            data_oniric.AVAILABILITIES_ARCHIPEL.append(info)
        elif type_info == 'hold':
            data_oniric.HOLD_ARCHIPEL.append(info)
        elif type_info == 'price':
            data_oniric.PRICES_ARCHIPEL.append(info)

    elif boat_name == 'Aqua':
        if type_info == 'departure_date':
            data_oniric.DEPARTURE_DATES_AQUA.append(info)
        elif type_info == 'arrival_date':
            data_oniric.ARRIVAL_DATES_AQUA.append(info)
        elif type_info == 'availability':
            data_oniric.AVAILABILITIES_AQUA.append(info)
        elif type_info == 'hold':
            data_oniric.HOLD_AQUA.append(info)
        elif type_info == 'price':
            data_oniric.PRICES_AQUA.append(info)

    else:
        print('Name of boat not recognized')
    
    

def create_json_file():
    flag = check_data() # Gets true if all data is correct
    #print('\n\n***FLAG: ', flag)
    if flag == False:
        """
        Terminates the program if data structures do not have the same size
        """
        print('*** ERROR ***: data structures are not the same sizes')
        quit()
    else:
        """
        creates JSON file
        """
        for i in range(len(data_oniric.ALL_BOAT_NAMES)):
            boat_id_temp = get_boat_id(data_oniric.ALL_BOAT_NAMES[i])
            cabin_id_temp = data_oniric.CABINS_INTERNAL[data_oniric.ALL_BOAT_NAMES[i]]
            COMPLETE_JSON[boat_id_temp] = {}
            COMPLETE_JSON[boat_id_temp][cabin_id_temp] = {
                'boat' : boat_id_temp,
                'cabin' : cabin_id_temp,
                'departures' : get_departures_dict(i)
                } # *** Cambiar por el número de ALL CABINS
            
            #departures_list = 
            #COMPLETE_JSON[boat_id_temp]['All cabins']['departures'] = departures_list
            
            
            
        
        
    
def check_data():
    """
    Checks if all the arrays of each boat have the same size
    """
    if len(data_oniric.DEPARTURE_DATES_AQUA) == len(data_oniric.ARRIVAL_DATES_AQUA) == len(data_oniric.AVAILABILITIES_AQUA) == len(data_oniric.HOLD_AQUA) == len(data_oniric.PRICES_AQUA):
        temp_aqua = True
    else:
        temp_aqua = False
    if len(data_oniric.DEPARTURE_DATES_ARCHIPEL) == len(data_oniric.ARRIVAL_DATES_ARCHIPEL) == len(data_oniric.AVAILABILITIES_ARCHIPEL) == len(data_oniric.HOLD_ARCHIPEL) == len(data_oniric.PRICES_ARCHIPEL):
        temp_archipel = True
    else:
        temp_archipel = False
    if len(data_oniric.DEPARTURE_DATES_SOLARIS) == len(data_oniric.ARRIVAL_DATES_SOLARIS) == len(data_oniric.AVAILABILITIES_SOLARIS) == len(data_oniric.HOLD_SOLARIS) == len(data_oniric.PRICES_SOLARIS):
        temp_solaris = True
    else:
        temp_solaris = False
    if len(data_oniric.DEPARTURE_DATES_TREASURE) == len(data_oniric.ARRIVAL_DATES_TREASURE) == len(data_oniric.AVAILABILITIES_TREASURE) == len(data_oniric.HOLD_TREASURE) == len(data_oniric.PRICES_TREASURE):
        temp_treasure = True
    else:
        temp_treasure = False
    
    if temp_aqua == True and temp_archipel == True and temp_solaris == True and temp_treasure == True:
        return True
    else:
        return False
    
    
def get_boat_id(boat_name):
    return data_oniric.BOATS[boat_name]

def get_departures_dict(i):
    list_temp = []
    
    if i+1 == 1:
        """
        ARCHIPEL I
        """

        for j in range(len(data_oniric.DEPARTURE_DATES_ARCHIPEL)):
            dict_temp = {}
            dict_temp['departure_date'] = str(data_oniric.DEPARTURE_DATES_ARCHIPEL[j])
            dict_temp['arrival_date'] = str(data_oniric.ARRIVAL_DATES_ARCHIPEL[j])
            dict_temp['days'] = get_dates_difference(data_oniric.DEPARTURE_DATES_ARCHIPEL[j], data_oniric.ARRIVAL_DATES_ARCHIPEL[j])
            dict_temp['available'] = int(data_oniric.AVAILABILITIES_ARCHIPEL[j])
            dict_temp['hold'] = int(data_oniric.HOLD_ARCHIPEL[j])
            dict_temp['adult_price'] = clean_price(data_oniric.PRICES_ARCHIPEL[j])
            dict_temp['promotion_name'] = 'season price'
            
            if dict_temp['available'] != 0:
                """
                Only adds the date to the list if there is room available
                """
                list_temp.append(dict_temp)
            
        return list_temp
    
    elif i+1 == 2:
        """
        AQUA
        """
        for j in range(len(data_oniric.DEPARTURE_DATES_AQUA)):
            dict_temp = {}
            dict_temp['departure_date'] = str(data_oniric.DEPARTURE_DATES_AQUA[j])
            dict_temp['arrival_date'] = str(data_oniric.ARRIVAL_DATES_AQUA[j])
            dict_temp['days'] = get_dates_difference(data_oniric.DEPARTURE_DATES_AQUA[j], data_oniric.ARRIVAL_DATES_AQUA[j])
            dict_temp['available'] = int(data_oniric.AVAILABILITIES_AQUA[j])
            dict_temp['hold'] = int(data_oniric.HOLD_AQUA[j])
            dict_temp['adult_price'] = clean_price(data_oniric.PRICES_AQUA[j])
            dict_temp['promotion_name'] = 'season price'
            
            if dict_temp['available'] != 0:
                """
                Only adds the date to the list if there is room available
                """
                list_temp.append(dict_temp)
        
        return list_temp
    
    elif i+1 == 3:
        """
        SOLARIS
        """
        
        for j in range(len(data_oniric.DEPARTURE_DATES_SOLARIS)):
            dict_temp = {}
            dict_temp['departure_date'] = str(data_oniric.DEPARTURE_DATES_SOLARIS[j])
            dict_temp['arrival_date'] = str(data_oniric.ARRIVAL_DATES_SOLARIS[j])
            dict_temp['days'] = get_dates_difference(data_oniric.DEPARTURE_DATES_SOLARIS[j], data_oniric.ARRIVAL_DATES_SOLARIS[j])
            dict_temp['available'] = int(data_oniric.AVAILABILITIES_SOLARIS[j])
            dict_temp['hold'] = int(data_oniric.HOLD_SOLARIS[j])
            dict_temp['adult_price'] = clean_price(data_oniric.PRICES_SOLARIS[j])
            dict_temp['promotion_name'] = 'season price'
            
            if dict_temp['available'] != 0:
                """
                Only adds the date to the list if there is room available
                """
                list_temp.append(dict_temp)
        
        return list_temp
    
    elif i+1 == 4:
        """
        TREASURE
        """
        
        for j in range(len(data_oniric.DEPARTURE_DATES_TREASURE)):
            dict_temp = {}
            dict_temp['departure_date'] = str(data_oniric.DEPARTURE_DATES_TREASURE[j])
            dict_temp['arrival_date'] = str(data_oniric.ARRIVAL_DATES_TREASURE[j])
            dict_temp['days'] = get_dates_difference(data_oniric.DEPARTURE_DATES_TREASURE[j], data_oniric.ARRIVAL_DATES_TREASURE[j])
            dict_temp['available'] = int(data_oniric.AVAILABILITIES_TREASURE[j])
            dict_temp['hold'] = int(data_oniric.HOLD_TREASURE[j])
            dict_temp['adult_price'] = clean_price(data_oniric.PRICES_TREASURE[j])
            dict_temp['promotion_name'] = 'season price'
            
            
            if dict_temp['available'] != 0:
                """
                Only adds the date to the list if there is room available
                """
                list_temp.append(dict_temp)
        
        return list_temp
        
    
def get_dates_difference(departure_date, arrival_date):
    
    
    #converted_date1 = datetime.strptime(departure_date, '%Y-%m-%d')
    #converted_date2 = datetime.strptime(arrival_date, '%Y-%m-%d')
    dates_difference = arrival_date - departure_date
    dates_difference = str(dates_difference)
    dates_difference = dates_difference.split(' ')

    #print('\nDeparture: {}\tArrival: {}\tDays: {}'.format(departure_date, arrival_date, int(dates_difference[0]) + 1))
    return int(dates_difference[0]) + 1        
        
    
    
"""
'departure_date' : data_gadventures.DEPARTURE_DATE_TEMP,
'arrival_date' : data_gadventures.ARRIVAL_DATE_TEMP,
'days' : dates_difference(data_gadventures.DEPARTURE_DATE_TEMP, data_gadventures.ARRIVAL_DATE_TEMP),
'available' : availability_final,
'hold' : 0,
'adult_price' : int(price_final[1:]) # Eliminates the dollar sign
"""
        
def clean_price(price_old):
    try: 
        price = price_old.split('$')
        price = price[1]
        if ',' in price:
            price = price.split(',')
            temp = int(price[0]) * 1000
            price = price[1].split('.')
            price = int(price[0])
            final = temp + price
        else:
            final = int(price.split('.')[0])
        
        return final
        
    except:
        print('Failed getting price')
        return None
        quit()
        
        
        
        
        
        
        
        
        
        
        

