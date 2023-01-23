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

    
    url = '{}{}'.format(API_CREDENTIALS.API_URL, API_CREDENTIALS.UPDATE_PRICE_AND_AVAILABILITY_PATH)
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


def update_price_and_availability(boat_id=None, cabin_type_id=None, specific_path=''):
    print('En update price: ', specific_path)

    #file_json = open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\GoldenGalapagos\Requests\request_boat_{}_cabin_type_{}.json'.format(boat_id, cabin_type_id), 'r') # Código para Lightsail
    file_json = open('/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/{}/Requests/request_boat_{}_cabin_type_{}.json'.format(specific_path, boat_id, cabin_type_id), 'r') # Para uso personal
    data = file_json.read()
    
    #print(type(data))
    
    data = json.loads(data) 
    
    
    #print(data)
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


def send_information(final_json, specific_path):
    #print('En send information: ', specific_path)
    #print(final_json) 
    for boat_id in final_json:
        for cabin_type_id in final_json[boat_id]:

            info_in_json = final_json[boat_id][cabin_type_id]
            list_string = json.dumps(info_in_json['departures'])
            
            info_in_json['departures'] = list_string
            
            #print(info_in_json)
            
            #f = open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\GAdventures\Requests\request_boat_{}_cabin_type_{}.json'.format(boat_id, cabin_type_id), 'w') # Path to use in Lightsail 
            f = open('/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/{}/Requests/request_boat_{}_cabin_type_{}.json'.format(specific_path, boat_id, cabin_type_id), 'w')
            f.write(json.dumps(info_in_json))
            f.close()
    
            update_price_and_availability(boat_id, cabin_type_id, specific_path)
    

#update_price_and_availability(48, 176, 'GAdventures')



#update_price_and_availability(31, 240, 'GoldenGalapagos')
update_price_and_availability(52, 313, 'GoGalapagos')











