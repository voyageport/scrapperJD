from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from datetime import timedelta
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import data_intrepid
import time
import string
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
        
def write_element_by_xpath(driver, path, text):
    time.sleep(5)
    
    element = driver.find_element(By.XPATH, path)
    element.clear()
    time.sleep(2)
    element.send_keys(text)
    time.sleep(3)
    element.send_keys(Keys.RETURN)
    
def get_all_tour_links(driver, total_trips_web, ):
    while len(data_intrepid.LINKS_TO_VISIT) < total_trips_web:
        
        trips = driver.find_elements(By.CLASS_NAME, data_intrepid.INDIVIDUAL_TRIP_CARD_CLASS_NAME)
                                     
        #print('Number of trips found (counter): ', len(trips))
        
        for i in range(len(trips)):
            data_intrepid.LINKS_TO_VISIT.append(trips[i].get_attribute('href'))
        
        i += 10 # Adds the 10 trips that are found on the first page
        
        if len(data_intrepid.LINKS_TO_VISIT) < total_trips_web:
            #print("Clicking on 'Next page'")
            click_on_element_by_path(driver, data_intrepid.NEXT_PAGE_PATH)
            time.sleep(3)

def get_data(driver):
    """
    Main method of the program
    """
        # To test an specific tour
        #driver.get('https://www.intrepidtravel.com/en/ecuador/galapagos-focus-grand-queen-bea-140586')
    
    # Iteration through all links
    for i in range(len(data_intrepid.LINKS_TO_VISIT)):
        driver.get(data_intrepid.LINKS_TO_VISIT[i]) # For automatization
        #click_on_element_by_path(driver, data_intrepid.CLOSE_COOKIES_2_PATH) # Closes the cookies pop-up
        try:
            time.sleep((5))
            click_on_element_by_class_name(driver, data_intrepid.CLOSE_COOKIES_2_CLASS_NAME) # Closes the cookies pop-up
        except:
            print('No cookies pop-up')
        
        tour_title, boat_name, boat_ID = get_tour_title_and_boat_id(driver) # Gets the tour title and the boat ID
        include_boat_in_json(boat_ID) # Checks if boat exists in keys of JSON file and includes it
        total_days = determine_days(driver) # Gets the number of days of duration (it subtracts the days in Quito)
        view_more_departures(driver) # Clicks on 'View more departures' until all dates are shown
        get_all_dates_and_cabins(driver, boat_ID, total_days) # Gets the information in all cabins (including prices)
        json_to_file() # Stores all the info in a file

    #print('Dict: ', data_intrepid.COMPLETE_JASON)
    #driver.close()

def get_tour_title_and_boat_id(driver):
    tour_title = driver.find_element(By.CLASS_NAME, data_intrepid.TOUR_TITLE_CLASS_NAME)
    tour_title = tour_title.get_attribute('innerHTML')
    boat_id = data_intrepid.BOATS_DATA[clean_boat_name(tour_title)]
    print('\n\nVisiting tour:', clean_tour_title(tour_title))
    print('Boat: ', clean_boat_name(tour_title), end='\t\t')
    #print('Boat ID: ', boat_id)
    
    # Returns: tour title, boat name, boat ID
    return clean_tour_title(tour_title), clean_boat_name(tour_title), boat_id
    
def clean_tour_title(tour_title):
    #title = tour_title.split(':')
    #title = title[1]
    #title = title.split('(')
    
    title = tour_title.split('(')
    title = title[0]
    if '&amp;' in title:
        title = title.replace('&amp;', '&')
    return title

def clean_boat_name(tour_title):
    title = tour_title.split('(')
    title = title[1]
    title = title.split(')')
    title = title[0]
    if title == 'Grand Queen Bea':
        title = 'Grand Queen Beatriz'
    print(title)
    return title

def include_boat_in_json(boat_ID):
    if boat_ID not in data_intrepid.COMPLETE_JASON.keys():
       data_intrepid.COMPLETE_JASON[boat_ID] = {}

def determine_days(driver):
    days_total = int(driver.find_element(By.CLASS_NAME, data_intrepid.TOTAL_DAYS_CLASS_NAME).get_attribute('innerHTML'))
    #print('Total days (with Quito): ', days_total)
    
    start_city = driver.find_element(By.XPATH, data_intrepid.START_CITY_PATH).get_attribute('innerHTML')
    finish_city = driver.find_element(By.XPATH, data_intrepid.FINISH_CITY_PATH).get_attribute('innerHTML')
    
    if 'Quito' in start_city and 'Quito' in  finish_city:
        days_total = days_total - 2
    elif 'Quito' in start_city or 'Quito' in  finish_city:
        days_total = days_total - 1
        
    #print('Total days: ', days_total)
    return days_total
    
def view_more_departures(driver):
    """
    Tries to click on 'View more departures' a lot of times in order to make sure
    that all tours are being displayed
    """
    close_intrusive_pop_up(driver) # Checks in case the intrusive pop-up appears before trying to click on "more departures"
    
    for i in range(10):
        try:
            click_on_element_by_path(driver, data_intrepid.VIEW_MORE_DEPARTURES_PATH)
            time.sleep(5)
        except:
            print('', end = '')
            flag = close_intrusive_pop_up(driver)
            if flag == False:
                break
            else:
                close_intrusive_pop_up(driver)
    get_number_of_days(driver)
    #driver.refresh()
    time.sleep(4)
    close_intrusive_pop_up(driver)
        
def get_number_of_days(driver):
    data_intrepid.TOTAL_NUMBER_OF_DAYS = driver.find_elements(By.CLASS_NAME, data_intrepid.INDIVIDUAL_DATES_INFO_CLASS_NAME)
    for i in range(len(data_intrepid.TOTAL_NUMBER_OF_DAYS)):
        #print(data_intrepid.TOTAL_NUMBER_OF_DAYS[i].get_attribute('innerHTML'))
        get_departure_and_arrival_date(data_intrepid.TOTAL_NUMBER_OF_DAYS[i].get_attribute('innerHTML'))
        
    #print('Total number of days: ', len(data_intrepid.TOTAL_NUMBER_OF_DAYS))
    #print('len departure: {}\t\t len arrival: {}'.format(len(data_intrepid.DEPARTURES_DATES_LIST), len(data_intrepid.ARRIVAL_DATES_LIST))) # Checks that lens are the same
    
def close_intrusive_pop_up(driver):
    flag = False
    try:
        click_on_element_by_path(driver, data_intrepid.POP_UP_INTRUSIVE_PATH)
        flag = True
        return flag
    except:
        print('', end='')
        return flag

def get_departure_and_arrival_date(complete_text):
    departure_date = complete_text.split('>')
    departure_date = departure_date[2]
    departure_date = departure_date.split('<')
    departure_date = departure_date[0]
    departure_date = departure_date.strip()
    
    arrival_date = complete_text.split('>')
    arrival_date = arrival_date[4]
    arrival_date = arrival_date.split('<')
    arrival_date = arrival_date[0]
    arrival_date = arrival_date.strip()
    
    data_intrepid.DEPARTURES_DATES_LIST.append(departure_date) # Stores all departure dates in list
    data_intrepid.ARRIVAL_DATES_LIST.append(arrival_date) # Stores all arrival dates in list 
    
    print('departure_date: {}\t\tarrival_date: {}'.format(departure_date, arrival_date))

def get_all_dates_and_cabins(driver, boat_ID, total_days):
    """
    Also gets PRICES information
    """
    for i in range(len(data_intrepid.TOTAL_NUMBER_OF_DAYS)): # Iterates through ALL dates
    #for i in range(9): # Iterates through some dates
        #print('Departure: {}\t\tArrival: {}'.format(data_intrepid.DEPARTURES_DATES_LIST.pop(0), data_intrepid.ARRIVAL_DATES_LIST.pop(0)))
        
        departure = format_dates(data_intrepid.DEPARTURES_DATES_LIST.pop(0), 'departure')
        arrival = format_dates(data_intrepid.ARRIVAL_DATES_LIST.pop(0), 'arrival')
        
        #print('Departure: ', departure, end='\t\t')
        #print('Arrival: ', arrival)

        if boat_ID == 35:
            number_of_cabins = 6
        elif boat_ID == 77:
            number_of_cabins = 4
            
        for j in range(number_of_cabins): # Iterates through cabins
        
            dict_departures_temp = {
                'departure_date' : departure,
                'arrival_date' : arrival,
                'days' : total_days,
                'available' : None,
                'hold' : 0,
                'adult_price' : None,
                'promotion_name' :'season price'
                }
            
            price = get_prices(driver, i+1, j+2)
            availability = get_availabilities(driver, i+1, j+2)

            if price == 'Fully booked':
                dict_departures_temp['adult_price'] = 0
            else:
                dict_departures_temp['adult_price'] = int(price)
              
            dict_departures_temp['available'] = availability

            cabin_type_name = driver.find_element(By.XPATH, data_intrepid.CABIN_TYPES_PATH_GENERAL.format(i+1, j+2)).get_attribute('innerHTML')
            cabin_ID = get_cabin_ID_for_API(boat_ID, cabin_type_name)    
        
            # Inserting cabin types to JSON file
            #print('\t\t', driver.find_element(By.XPATH, data_intrepid.CABIN_TYPES_PATH_GENERAL.format(i+1, j+2)).get_attribute('innerHTML'), end = '\t\t')
            #print('*** ', dict_departures_temp, end = '\n\n')
            if cabin_ID not in data_intrepid.COMPLETE_JASON[boat_ID]:
                data_intrepid.COMPLETE_JASON[boat_ID][cabin_ID] = {
                    'boat' : boat_ID,
                    'cabin' : cabin_ID,
                    'departures' : []
                    }
            data_intrepid.COMPLETE_JASON[boat_ID][cabin_ID]['departures'].append(dict_departures_temp)
               
def get_cabin_ID_for_API(boat_ID, cabin_name):
    return data_intrepid.CABINS_IDS_INTERNAL[str(boat_ID)][cabin_name]

def format_dates(date, date_indicator):
    date_modified = datetime.strptime(date, '%a %d %b %Y')
    """
    Dates displayed in the Intrepid website doesn't match the ones in the GDS.
    That's why it is needed to: 
        - Add a day to the departure date
        - Subtract  a day to the arrival date
    """
    if date_indicator == 'departure':
        date_modified = date_modified + timedelta(days=1)
    elif date_indicator == 'arrival':
        date_modified = date_modified - timedelta(days=1)
    #print('Modificado: ', date_modified)
    #print(type(date_modified))
    return str(date_modified.date())
    
def get_prices(driver, i, j):
    price = driver.find_element(By.XPATH, data_intrepid.PRICES_PATH_GENERAL.format(i, j)).get_attribute('innerHTML')
    if'Fully booked' in price:
        return 'Fully booked'
    else:
        if '"room.discount_price">' in price:
            price = price.split('"room.discount_price">')
            price = price[1]
            price = price.split('<')
            price = price[0]
            price = price[1:]
            if ',' in price:
                price = price.replace(',', '')
            return int(price)
        elif '"room.total_price">' in price:
            price = price.split('"room.total_price">')
            price = price[1]
            price = price.split('<')
            price = price[0]
            price = price[1:]
            if ',' in price:
                price = price.replace(',', '')
            return int(price)
        else:
            return 'Not able to get price'
        
def get_availabilities(driver, i, j):
    availability = driver.find_element(By.XPATH, data_intrepid.AVAILABILITIES_PATH_GENERAL.format(i, j)).get_attribute('innerHTML')
    #print(availability)
    if 'left' in availability:
        availability = availability.split('>')
        availability = availability[-3]
        availability = availability.split(' ')
        availability = availability[0]
        #print(availability)
        return int(availability)
    elif 'book-now' in availability:
        return 4
    else:
        #print(0)
        return 0

def json_to_file():
    json_temp = json.dumps(data_intrepid.COMPLETE_JASON)
    
    with open("all_info_intrepid.json", "w") as outfile:
        outfile.write(json_temp)
        
    outfile.close()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    