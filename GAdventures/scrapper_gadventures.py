from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from data_gadventures import COMPLETE_JSON


import time
import data_gadventures
import string
import re
import data_gadventures
import requests
import json

def get_data_part_1(driver, tour_buttons):
    for i in range(len(data_gadventures.TOUR_TITLES)):
        if 'Cruise Only' in data_gadventures.TOUR_TITLES[i]:
            #print(data_gadventures.TOUR_TITLES[i])
            # Stores the link of the specific tour to visit later 
            tour_link = tour_buttons[i].get_attribute('href')
            data_gadventures.LINKS_TO_VISIT.append(tour_link)

            # Gets the cruise name from the page
            page_content = requests.get(tour_link)
            pattern = re.compile('(?sm)var trip = (.*?)}$')
            element = pattern.search(page_content.text)[0]
            trip_id = re.findall(r'"([0-9]+)"', element)[0]
            trip_name = re.findall(r'"(.*?)"', element)[2]
            
            trip_title = get_tour_name(str(trip_name)) # Cleans the TOUR TITLE
            data_gadventures.TOUR_TITLES_CRUISE_ONLY.append(trip_title)
            cruise_name = delete_cruise_only_tag(str(trip_name)) # Cleans the CRUISE TITLE
            
            data_gadventures.CRUISES_TO_ADD.append(cruise_name)
            
            #print('***Trip title: ', trip_title, end='\n\n') # Prints the tour title
            #print('cruise name: ', cruise_name) # Prints the cruise name
            
            # Se almacena el ID del barco del tour específico
            #trip_boat_id = data_gadventures.BOATS[cruise_name]
            #print('cruise ID: ', trip_boat_id)
          
    get_data_part_2(driver)
    
def get_data_part_2(driver):
    for i in range(len(data_gadventures.LINKS_TO_VISIT)):
        
        print('     Getting information from: ', data_gadventures.TOUR_TITLES_CRUISE_ONLY.pop(0)) # Prints the current tour that its being scrapped 
                

        # Get the boat ID of the curent cruise
        trip_boat_id = data_gadventures.BOATS[data_gadventures.CRUISES_TO_ADD.pop(0)]
        
        time.sleep(5)
        if trip_boat_id not in COMPLETE_JSON.keys():
            COMPLETE_JSON[trip_boat_id] = {}
        
        driver.get(data_gadventures.LINKS_TO_VISIT[i]) # Specific tour is opened in another window
        time.sleep(10)

        # Gets all the info of promotions
        promos = driver.find_elements(By.CLASS_NAME, data_gadventures.PROMO_INFO_CLASS_NAME)
        

        for i in range(len(promos)//2): # Each promo appears twice
            texto = promos[i].get_attribute('innerHTML')
            promo, start_date, end_date = get_promos_and_dates(texto)
            
            data_gadventures.PROMOS_PERCENTAGES.append(promo)
            data_gadventures.PROMOS_START_DATES.append(start_date)
            data_gadventures.PROMOS_END_DATES.append(end_date)

        """
        Método para sacar fechas y disponibilidades por XPATH
        """
        
        date_request = driver.find_elements(By.CLASS_NAME, 'clearfix.request-item.with-room')
        date_booking = driver.find_elements(By.CLASS_NAME, 'clearfix.booking-item.with-room')
        date_not_available = driver.find_elements(By.CLASS_NAME, 'clearfix.not-available.with-room')
        total_data = len(date_request) + len(date_booking) + len(date_not_available)

        
        months_counter = 1
        column_counter = 1
        
        flag = False
        index_in_use = -1
        while flag == False and index_in_use < 3:
            #print('Índice a probar: ', data_gadventures.XPATH_INDEXES[index_in_use])
            index_in_use += 1
            flag = check_exists_by_xpath(driver, '/html/body/div[4]/div/div[2]/div[4]/section[{}]/div[1]/div[2]/div/div[2]/div[1]/ul/div[1]/li'.format(data_gadventures.XPATH_INDEXES[index_in_use]))


        for i in range(total_data): # To iterate throguh all data
        #for i in range(40): # To test few dates 
        #for i in range(total_data-83): # To test promotions

            try:
                """
                MANIPULATES XPATHS TO OBTAIN DATES INFO 
                """
                month_and_year = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div[4]/section[{}]/div[1]/div[2]/div/div[2]/div[{}]/div/strong'.format(data_gadventures.XPATH_INDEXES[index_in_use], months_counter))
                year_to_use = get_year(month_and_year)
                
                date = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div[4]/section[{}]/div[1]/div[2]/div/div[2]/div[{}]/ul/div[{}]/li'.format(data_gadventures.XPATH_INDEXES[index_in_use], months_counter, column_counter))
                clean_tour_info(date.get_attribute('innerHTML'), year_to_use, trip_boat_id) 
                column_counter += 1

    
            except:
                #print('Entró')
                #print('Falló: /html/body/div[4]/div/div[2]/div[4]/section[7]/div[1]/div[2]/div/div[2]/div[{}]/ul/div[{}]/li'.format(months_counter, column_counter), end = '\n\n')
                column_counter = 1
                months_counter += 1
                
    print('Scrapping process finished succesfully')

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
        
def remove_special_char(text: str):

    pattern = r'[' + string.punctuation + ']'
    return re.sub(pattern, '', text.strip())

def convert_promos_dates(date_string):
    date_formatted = datetime.strptime(date_string, '%b %d, %Y').date()
    return date_formatted
    
def get_promos_and_dates(texto):
    promo = texto
    date = texto
    
    promo = promo.split('>')
    promo = promo[2]
    promo = promo.split('-')
    promo = promo[0]
    promo = promo.split('Save')
    promo = promo[1]
    promo = promo.strip()
    #print('Promo: ', promo)
    
    date = date.split('>')
    date = date[3]
    date = date.split('<')
    date = date[0] # Stores dates of start annd expiration of promotion
    
    year = date.split(', ') 
    year = int(year[1].strip()) # Stores only the year, to add it to the date in which promotion starts
    
    start_date = date.split(' - ')
    start_date = start_date[0]
    end_date = date.split(' - ')
    end_date = end_date[1]
    
    month_1 = start_date.split(' ')
    month_1 = month_1[0]    
    month_2 = end_date.split(' ')
    month_2 = month_2[0]
    
    if ('Dec' in month_1 and 'Jan' in month_2) or ('Dec' in month_1 and 'Dec' not in month_2):
        """
        Fixes the year in case a promo goes from the 
        end of a year to the start of another year
        """
        year -= 1
    
    start_date = start_date + ', ' + str(year) # Adds the corresponding year to the start_date
    
    # Dates become formatted for further validation of promotions
    start_date = convert_promos_dates(start_date)
    end_date = convert_promos_dates(end_date)
    
    return promo, start_date, end_date

def get_boat_id_in_text(boat_name_text: str):
    '''
    Check if its necessary
    '''
    boat_name_text = remove_special_char(boat_name_text).strip().replace(" ", "").lower()
    boat_data_name = remove_special_char(data_gadventures.BOATS["name"]).strip().replace(" ", "").lower()
    if boat_data_name in boat_name_text:
        return data_gadventures.BOATS['id']
    return -1

def get_boat_id_in_text_jd(boat_name_text: str):
    '''
    Check if its necessary
    '''
    
    temp_boat_name = boat_name_text.split(' ')
    boat_name_unprocessed = ''
    final_boat_name = ''
    
    for i in range(len(temp_boat_name)):
        if temp_boat_name[i] == 'the':
            boat_name_unprocessed = temp_boat_name[i+1:]
            break
        
    for word2 in boat_name_unprocessed:
        if word2 != 'Voyager':
            final_boat_name = final_boat_name + word2 + ' '
            
    final_boat_name = final_boat_name.strip()    
    #print('Final boat name: ', final_boat_name)
    return data_gadventures.BOATS['{}'.format(final_boat_name)]


def replace_characters_on_string(string, old_character, new_character):
    for i in range(len(string)):
        if string[i] == old_character:
            string = string.replace(string[i], new_character)
            
def delete_amp_in_title(title_string):
    title = title_string.split('amp;')
    if len(title) > 1:
        title_final = ''
        for i in range(len(title)):
            title_final = title_final + title[i]
        return title_final
    else:
        return title[0]
    
def store_trip_names(driver):
    tours_container = driver.find_element(By.CLASS_NAME, data_gadventures.TOURS_CONTAINER_CLASS_NAME)
    tours_list = driver.find_elements(By.CLASS_NAME, data_gadventures.INDIVIDUAL_TOURS_CLASS_NAME)
    tours_names = driver.find_elements(By.CLASS_NAME, data_gadventures.TOURS_NAMES_CLASS_NAME)

    for title_HTML in tours_names:
        title = title_HTML.get_attribute('innerHTML')
        title = delete_amp_in_title(str(title))
        data_gadventures.TOUR_TITLES.append(title)
        
def get_tour_name(trip_name):
    trip_title = trip_name.split(' – ')
    #print(trip_title)
    trip_title = trip_title[1]
    trip_title = trip_title.split(' aboard')
    trip_title = trip_title[0]
    
    return trip_title

def delete_cruise_only_tag(trip_name):
    trip_name = trip_name.split('the ')
    trip_name = trip_name[1]
    trip_name = trip_name.split(' (Cruise Only)')
    trip_name = trip_name[0]
    
    if 'Voyager' in trip_name:
        trip_name = trip_name.split(' Voyager')
        trip_name = trip_name[0]
    return trip_name

def clean_trip_month(trip_month):
    trip_month = trip_month.get_attribute('innerHTML')
    trip_month = trip_month.split('>')
    trip_month = trip_month[1]
    trip_month = trip_month.split('<')
    trip_month = trip_month[0]
    
    return trip_month

def store_trip_dates(dates):
    for month in data_gadventures.MONTHS_SHORT:
        i = 0
        iterador = len(dates)
        while i < iterador:
            date_to_compare = dates[i].get_attribute('innerHTML')
            date_half = date_to_compare.split('-')
            date_half = date_half[0]
            
            if month in date_half:
                data_gadventures.DATES_INFO.append(date_to_compare)
                print(date_to_compare)
                dates.pop(i)
                iterador -= 1
            i += 1
    
    #print('*** len: ', len(data_gadventures.DATES_INFO))
    
def clean_html(info):
    info = info.split('>')
    info = info[1]
    info = info.split('<')
    info = info[0]
    info = info.strip()
    return info

def clean_tour_info(all_info, year_to_use, trip_boat_id):
    
    dict_departures_temp = {}

    if 'class="date"' in all_info:
        all_info = all_info.split('"date">')
        all_info = all_info[1]

        all_info = all_info.split("</div>")
        month = all_info[0].split(' ')
                
        
        if '&nbsp;\n' in month:
            print('', end='')
            #print('Departure date: ', data_gadventures.DEPARTURE_DATE_TEMP)
            #print('Arrival date: ', data_gadventures.ARRIVAL_DATE_TEMP)
      
        else:
            month = month[2]
    
            if month in data_gadventures.MONTHS_SHORT:
                '''
                ***
                '''
                #print('\nDate: ', all_info[0])
                convert_dates(all_info[0], year_to_use)
                
                #print('Departure date: ', data_gadventures.DEPARTURE_DATE_TEMP)
                #print('Arrival date: ', data_gadventures.ARRIVAL_DATE_TEMP)
        availability_info = all_info[1]
        
        if int(clean_html(availability_info)[0]) == 7:
            availability_final = int(clean_html(availability_info)[0])+1
            #print('Availability: ', availability_final)

        else:
            availability_final = int(clean_html(availability_info)[0])
            #print('Availability: ', availability_final)
        price_info = all_info[2]
        price_final = clean_html(price_info)
        #print('Price: ', price_final)
        room_info = all_info[4]
        cabin_type = clean_html(room_info)

        cabin_type = cabin_type_id_internal(trip_boat_id, cabin_type) # Changes cabin ID to the one used by the GDS 

        dict_departures_temp = {
                'departure_date' : data_gadventures.DEPARTURE_DATE_TEMP,
                'arrival_date' : data_gadventures.ARRIVAL_DATE_TEMP,
                'days' : dates_difference(data_gadventures.DEPARTURE_DATE_TEMP, data_gadventures.ARRIVAL_DATE_TEMP),
                'available' : availability_final,
                'hold' : 0,
                'adult_price' : int(price_final[1:]) # Eliminates the dollar sign
            }

        promo = add_promos(dict_departures_temp['departure_date'])
        
        if promo != None:
            dict_departures_temp['promotion_type'] = 'promotion'
            dict_departures_temp['promotion_name'] = str(promo) + ' Off'
        else:
            dict_departures_temp['promotion_name'] = 'season price'
            

        #print('***** PROMOO: ', promo, end = '\n\n')
        #print('***** ', dict_departures_temp, end = '\n\n')
        
        if cabin_type not in COMPLETE_JSON[trip_boat_id].keys():
            COMPLETE_JSON[trip_boat_id][cabin_type] = {
                    'boat' : trip_boat_id,
                    'cabin' : cabin_type,
                    'departures' : [dict_departures_temp]
                }
        else:
            COMPLETE_JSON[trip_boat_id][cabin_type]['departures'].append(dict_departures_temp)

        #print('***** ', dict_departures_temp, end = '\n\n')     
    elif 'class="date "' in all_info:
        all_info = all_info.split('"date ">')
        all_info = all_info[1]
        all_info = all_info.split("</div>")
        
        convert_dates(all_info[0], year_to_use)

def add_promos(departure_date):
    date_formatted = datetime.strptime(departure_date, '%Y-%m-%d').date()
    for i in range(len(data_gadventures.PROMOS_START_DATES)):
        
        if data_gadventures.PROMOS_START_DATES[i] <= date_formatted <= data_gadventures.PROMOS_END_DATES[i]:
            return data_gadventures.PROMOS_PERCENTAGES[i]
        
    return None
        
def cabin_type_id_internal(trip_boat_id, cabin_type):
    return data_gadventures.CABIN_IDS_INTERNAL[str(trip_boat_id)][cabin_type]
    
def json_creator(dict_departures_temp, availability_final, price_final, cabin_type, trip_boat_id):
    dict_departures_temp = {
            'departure_date' : data_gadventures.DEPARTURE_DATE_TEMP,
            'arrival_date' : data_gadventures.ARRIVAL_DATE_TEMP,
            'days' : 0,
            'available' : availability_final,
            'hold' : 0,
            'adult_price' : price_final
        }
    

    if cabin_type not in COMPLETE_JSON[trip_boat_id].keys():
        COMPLETE_JSON[trip_boat_id][cabin_type] = {
                'boat' : trip_boat_id,
                'cabin' : cabin_type,
                'departures' : [dict_departures_temp]
            }
    else:
        COMPLETE_JSON[trip_boat_id][cabin_type]['departures'].append(dict_departures_temp)
        
def dates_difference(date1, date2):
    converted_date1 = datetime.strptime(date1, '%Y-%m-%d')
    converted_date2 = datetime.strptime(date2, '%Y-%m-%d')
    dates_difference = converted_date2 - converted_date1
    dates_difference = str(dates_difference)
    dates_difference = dates_difference.split(' ')

    return int(dates_difference[0]) + 1

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

def get_year(month_and_year):
    month_and_year = month_and_year.get_attribute('innerHTML')
    month_and_year = month_and_year.split(' ')
    year = int(month_and_year[1])
    return year
    
def convert_dates(date, year_to_use):
    date2 = date.split(' - ')
    departure_date = date2[0]
    arrival_date = date2[1]
    
    departure_date += ' {}'.format(year_to_use)
    arrival_date += ' {}'.format(year_to_use)

    converted_date1 = datetime.strptime(departure_date, '%a, %d %b %Y')
    converted_date2 = datetime.strptime(arrival_date, '%a, %d %b %Y')
    converted_date1 = converted_date1.strftime('%Y-%m-%d')
    converted_date2 = converted_date2.strftime('%Y-%m-%d')
    
    data_gadventures.DEPARTURE_DATE_TEMP = converted_date1
    data_gadventures.ARRIVAL_DATE_TEMP = converted_date2
    
def json_to_file():
    json_temp = json.dumps(COMPLETE_JSON)
    
    with open("all_info.json", "w") as outfile:
        outfile.write(json_temp)
        
    outfile.close()
    
    

    
    
            
    
            
            
            
            
            
            