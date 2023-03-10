import json
import requests
from requests.auth import HTTPBasicAuth
import sys
    

#sys.path.insert(1, r'C:\Users\Administrator\Documents\Projects\scrapper_JD') # Path para Lightsail
sys.path.insert(1, '/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final') # Path para test personal

import API_CREDENTIALS


'''
# Load the JSON file into a Python dictionary
with open('/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/GoldenGalapagos/all_info.json', 'r') as f:
    data = json.load(f)
'''

    


def update_price_and_availability_golden(boat_id=None, cabin_type_id=None):
    
    #file_json = open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\GoldenGalapagos\Requests\request_boat_{}_cabin_type_{}.json'.format(boat_id, cabin_type_id), 'r') # Código para Lightsail
    file_json = open('/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/GoldenGalapagos/Requests/request_boat_{}_cabin_type_{}.json'.format(boat_id, cabin_type_id), 'r') # Para uso personal
    data = file_json.read()
    
    #print(type(data))
    
    data = json.loads(data) 
    
    '''
    Code to manually transform the 'departures' list to string
    '''
    #list_string = json.dumps(data['departures'])
    #data['departures'] = list_string

    
    url = '{}{}'.format(API_CREDENTIALS.API_URL_REAL, API_CREDENTIALS.UPDATE_PRICE_AND_AVAILABILITY_PATH)
    print('Enviando a : ', url)
    
    response = requests.post(url, json=data,
                             auth=HTTPBasicAuth(API_CREDENTIALS.API_USER, API_CREDENTIALS.API_PASS),
                             headers= API_CREDENTIALS.HEADERS)


    print(f"\tRequest made for: boat_id: {boat_id} and cabin_type: {cabin_type_id}")
    print(f"\tStatus code of response: {response.status_code}\n")



def send_information_golden(final_json):
    #print(final_json) 
    for boat_id in final_json:
        for cabin_type_id in final_json[boat_id]:

            info_in_json = final_json[boat_id][cabin_type_id]
            list_string = json.dumps(info_in_json['departures'])
            
            info_in_json['departures'] = list_string
            
            #print(info_in_json)
    
    
            #f = open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\GoldenGalapagos\Requests\request_boat_{}_cabin_type_{}.json'.format(boat_id, cabin_type_id), 'w') # Path to use in Lightsail 
            f = open('/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/GoldenGalapagos/Requests/request_boat_{}_cabin_type_{}.json'.format(boat_id, cabin_type_id), 'w')
            f.write(json.dumps(info_in_json))
            f.close()
    
            update_price_and_availability_golden(boat_id, cabin_type_id)

        

#send_information(process_data(data))
#update_price_and_availability(31,240)


def update_price_and_availability(boat_id=None, cabin_type_id=None, specific_path='', GDS_indicator=''):
    print('En update price: ', specific_path)

    #file_json = open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\GoldenGalapagos\Requests\request_boat_{}_cabin_type_{}.json'.format(boat_id, cabin_type_id), 'r') # Código para Lightsail
    file_json = open('/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/{}/Requests/request_boat_{}_cabin_type_{}.json'.format(specific_path, boat_id, cabin_type_id), 'r') # Para uso personal
    data = file_json.read()
    
    #print(type(data))
    
    data = json.loads(data) 
    
    
    #print(data) # Prints the data that is being sent to the GDS
    '''
    Code to manually transform the 'departures' list to string
    '''
    #list_string = json.dumps(data['departures'])
    #data['departures'] = list_string
    
    if GDS_indicator == True:
        print('True`')
        GDS_URL = API_CREDENTIALS.API_URL_REAL
    elif GDS_indicator == False:
        print('False')
        GDS_URL = API_CREDENTIALS.API_URL
    else:
        GDS_URL = None
        print('Not able to decide GDS URL')
    
    # Sends info to Demo GDS
    url = '{}{}'.format(GDS_URL, API_CREDENTIALS.UPDATE_PRICE_AND_AVAILABILITY_PATH) # Sends info to demo GDS
    
    print('\tEnviando a : ', url)
    
    response = requests.post(url, json=data,
                             auth=HTTPBasicAuth(API_CREDENTIALS.API_USER, API_CREDENTIALS.API_PASS),
                             headers= API_CREDENTIALS.HEADERS)


    print(f"\tRequest made for: boat_id: {boat_id} and cabin_type: {cabin_type_id}")
    print(f"\tStatus code of response: {response.status_code}\n")



def send_information(final_json, specific_path, GDS_indicator):
    #print('En send information: ', specific_path)
    #print(final_json) 
    # GDS indicator:
        # True: live server
        # False: Demo GDS
    for boat_id in final_json:
        for cabin_type_id in final_json[boat_id]:

            """
            Orders the departure dates
            """
            info_in_json = final_json[boat_id][cabin_type_id]
            departures_sorted = sorted(final_json[boat_id][cabin_type_id]['departures'], key=lambda d: d['departure_date'])
            
            #print(departures_sorted, end = '\n\n')  # Prints only the 'departures' list (sorted)
            
            # Converts the departures list onto string format
            info_in_json['departures'] = departures_sorted
            list_string = json.dumps(info_in_json['departures'])
            info_in_json['departures'] = list_string
            
            ##print(info_in_json, end = '\n\n*\n\n')
            
            #f = open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\GAdventures\Requests\request_boat_{}_cabin_type_{}.json'.format(boat_id, cabin_type_id), 'w') # Path to use in Lightsail 
            f = open('/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/{}/Requests/request_boat_{}_cabin_type_{}.json'.format(specific_path, boat_id, cabin_type_id), 'w')
            f.write(json.dumps(info_in_json))
            f.close()
            
            #print('Done')
    
            update_price_and_availability(boat_id, cabin_type_id, specific_path, GDS_indicator)
           
           
           
           

#update_price_and_availability(31, 240, 'GoldenGalapagos', True)
#update_price_and_availability(48, 177, 'GAdventures', True)
#update_price_and_availability(52, 313, 'GoGalapagos', True)
#update_price_and_availability(35, 71, 'Intrepid', False)
#update_price_and_availability(88, 425, 'Galagents', False)
#update_price_and_availability(19, 652, 'Oniric', False)

update_price_and_availability(37, 701, 'Nemo', True)















