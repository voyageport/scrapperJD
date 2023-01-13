from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from requests.auth import HTTPBasicAuth

import requests
import time
import data
import json


days = ['Monday,', 'Tuesday,', 'Wednesday,', 'Thursday,', 'Friday,', 'Saturday,', 'Sunday,'] # List that allows to recognize dates on HTML of site


def click_on_element_by_path(driver, path):
    time.sleep(5)
    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '{}'.format(path))))\
        .click()
    
def click_on_element_by_class_name(driver, class_name):
    time.sleep(5)
    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.CLASS_NAME,
                                           '{}'.format(class_name))))\
        .click()
        
def take_all_info(driver, path):
    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '{}'.format(path))))


def get_data(driver, limite_inferior_fechas , limite_superior_fechas, ship_number):
    """
    Most importanf method
    """

    data.COMPLETE_JSON[ship_name_by_number(ship_number)] = {} # States a new key on the dictionary
    
    dates = driver.find_elements(By.CLASS_NAME, 'card-header')
    limite_superior_fechas += limite_inferior_fechas

    for i in range(limite_inferior_fechas, limite_superior_fechas, 1):
        
        dates_total = []
        date = dates[i].get_attribute('innerHTML')
        date = date.split(' ')
        
        dict_fecha_completa = {}
        date_complete_title = get_date_label_title(date)
        
        for j in range(len(date)):
            if date[j] in days:
                dates_temp = date[j] + ' ' + date[j + 1]
                dates_total.append(dates_temp)
            elif date[j] == 'Available:':
                total_available = date[j+1]
                total_available  = total_available.split('</strong>')
                total_available = int(total_available[1])
                
        
        availability_acumulada = 0
        
        if total_available == 0:
            
            dict_departures = {} # Diccionario de información de 'departures'
            dict_departures['departure_date'] = convert_dates(dates_total[0])
            dict_departures['arrival_date'] = convert_dates(dates_total[1])
            dict_departures['days'] = dates_difference(dates_total[0], dates_total[1])
            
            dict_nombre_cabina = {}
            dict_nombre_cabina['boat'] = ship_name_by_number(ship_number)
            dict_nombre_cabina['cabin_type'] = data.NOMBRE_CABINAS[0]
            data.NOMBRE_CABINAS.pop(0)

            dict_nombre_cabina['cabin_number'] =  data.CABINAS_FINAL[0]
            data.CABINAS_FINAL.pop(0)
            
            dict_departures['available'] = data.AVAILABILITIES_FINAL[0]
            data.AVAILABILITIES_FINAL.pop(0)
            dict_nombre_cabina['departures'] = [dict_departures]
        else: 
            while availability_acumulada < total_available:
                """
                Continues adding cabins until total availability of date is matched
                """
                
                dict_departures = {} # Diccionario de información de 'departures'
                dict_departures['departure_date'] = convert_dates(dates_total[0])
                dict_departures['arrival_date'] = convert_dates(dates_total[1])
                dict_departures['days'] = dates_difference(dates_total[0], dates_total[1])
                
                dict_nombre_cabina = {}
                dict_nombre_cabina['boat'] = ship_name_by_number(ship_number)
                dict_nombre_cabina['cabin_type'] = data.NOMBRE_CABINAS[0]
                data.NOMBRE_CABINAS.pop(0)

                dict_nombre_cabina['cabin_number'] =  data.CABINAS_FINAL[0]
                data.CABINAS_FINAL.pop(0)

                dict_departures['available'] = data.AVAILABILITIES_FINAL[0]
                availability_acumulada += data.AVAILABILITIES_FINAL.pop(0)
                
                """
                ***** Aquí se pone el Hold?
                """
                
                dict_departures['hold'] = 0
                
                #GET INFO FROM API
                dict_nombre_cabina['API_BOAT_ID'], dict_nombre_cabina['API_CABIN_ID'] = get_cabin_id_from_api(dict_nombre_cabina)
                
                dict_nombre_cabina['departures'] = [dict_departures]
                dict_fecha_completa['{}'.format(dict_nombre_cabina['cabin_type'])] = dict_nombre_cabina
                
                
                
                
        #print(dict_fecha_completa)
        
            data.COMPLETE_JSON[ship_name_by_number(ship_number)][date_complete_title] = dict_fecha_completa
        
        #print(dict_with_complete_date)
        
        
   
def process_cabins_and_availabilities(cabinas, availabilities):
    while len(cabinas) > 0:
        texto = cabinas[0].get_attribute('innerHTML')
        cabinas.pop(0)
        texto = texto.split('<u>')
        texto = texto[1]
        texto2 = texto.strip()
        texto = texto2.split(' ')
        texto = texto[0]
        data.CABINAS_FINAL.append(int(texto))
        
        # Name of cabin is obtained 
        texto2 = texto2.split('</u>')
        texto2 = texto2[0]
        texto2 = texto2.split(' ')
        texto_string = ''
        for i in range(len(texto2)-1):
            texto_string = texto_string + ' ' + texto2[i+1]
            
        data.NOMBRE_CABINAS.append(texto_string.strip())
        
        
        availability = int(availabilities[0].get_attribute('innerHTML'))
        data.AVAILABILITIES_FINAL.append(availability)
        availabilities.pop(0)
        

def convert_dates(date):
    date += ' 2023'
    converted_date = datetime.strptime(date, '%A, %d-%B %Y')
    converted_date = converted_date.strftime('%Y-%m-%d')
    return converted_date

def dates_difference(date1, date2):
    converted_date1 = datetime.strptime(date1, '%A, %d-%B')
    converted_date2 = datetime.strptime(date2, '%A, %d-%B')
    dates_difference = converted_date2 - converted_date1
    dates_difference = str(dates_difference)
    dates_difference = dates_difference.split(' ')
    
    return int(dates_difference[0]) + 1

def ship_name_by_number(ship):
    if ship == 0:
        return 'endemic'
    elif ship == 1:
        return 'elite'
    elif ship == 2:
        return 'petrel'
    else:
        return 'oceanspray'
    
def get_date_label_title(date_to_process):
    """
    Getting title of date label of website for json file
    """
    title = ''
    contador = 0
    for i in range(len(date_to_process)):
        if date_to_process[i] in days and contador < 1:
            title = title + date_to_process[i] + ' ' + date_to_process[i + 1] + ' to '
            contador += 1
        elif date_to_process[i] in days and contador == 1:
            title = title + date_to_process[i] + ' ' + date_to_process[i + 1] + ' ' + date_to_process[i + 2] +' ' + date_to_process[i + 3] + ' ' + date_to_process[i + 4] + ' ' + date_to_process[i + 5] + ' ' + date_to_process[i + 6]
        elif date_to_process[i] == 'Available:':
            numero = date_to_process[i + 1]
            numero = numero.split('</strong>')
            title = title + ' Total Available: ' + numero[1]
    return title
        
        
def get_cabin_id_from_api(dict_nombre_cabina):

    boat_name = dict_nombre_cabina['boat']
    boat_api_number = get_ship_number_from_api(boat_name)
    cabin_number = dict_nombre_cabina['cabin_number']

    
    payload={'boat_id': '{}'.format(boat_api_number),
    'number': '{}'.format(cabin_number)}
    
    response = requests.request("POST", data.URL_API, auth=HTTPBasicAuth('user@voyageport.com', 'userVoy#1534'), headers = data.HEADERS, data=payload, files = data.FILES)
    print('*** Response: ', response.text)
    """
    cabin_id = response.text
    cabin_id = cabin_id.split('"id":')
    cabin_id = cabin_id[1].split(',')
    cabin_id = int(cabin_id[0])

    return boat_api_number, cabin_id
    """

        
      
def get_ship_number_from_api(ship_name):
    ship_name = ship_name.capitalize()    
    return data.BOATS_IDS_FOR_API[ship_name]


def string_to_json_file(string):
    string = str(string)
    
    for i in range(len(string)):
        if string[i] == "\'":
            string = string.replace(string[i], '\"')
    
    # String is converted to json format
    json_string = json.loads(string)
    #json_in_text.close() # prints 'type: dict', but it is json format

    json_object = json.dumps(json_string) # Creates object in order to save it as file
    
    

    '''
    Saves the data onto a new file
    '''
    # Save file .json
    with open("all_info.json", "w") as outfile:
        outfile.write(json_object)
        
    outfile.close()

    
    
def string_to_json_return(string):
    string = str(string)
    #print(type(string))

    
    for i in range(len(string)):
        if string[i] == "\'":
            string = string.replace(string[i], '\"')
    
    # String is converted to json format
    json_string = json.loads(string)
    
    #print(type(json_string))
    #json_object = json.dumps(json_string)
    
    
    return json_string


    
def change_json_format(data):

    aux_dict = {}
    

    for boat_name, all_boat_dates in data.items():
        

        for itinerary_date, cabins in all_boat_dates.items():
            aux_departure = {}
            for cabin_name, cabin_data in cabins.items():
                cabin_type_id = cabin_data['API_CABIN_ID']
                boat_id = cabin_data['API_BOAT_ID']


                if boat_id not in aux_dict.keys():
                    aux_dict[boat_id] = {}
                    


                if cabin_type_id not in aux_dict[boat_id].keys():
                    aux_dict[boat_id][cabin_type_id] = {
                        "boat": boat_id,
                        "cabin": cabin_type_id,
                        "departures": []
                    }


                if cabin_type_id not in aux_departure.keys():
                    aux_departure[cabin_type_id] = cabin_data['departures'][0]
                
                else:
                    aux_departure[cabin_type_id]['available'] += int(cabin_data['departures'][0]['available'])
                    


            for key_type, departure in aux_departure.items():
                aux_dict[boat_id][key_type]['departures'].append(departure)
            
            json_object = json.dumps(aux_dict)


    return json_object
            
    
    
    
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
