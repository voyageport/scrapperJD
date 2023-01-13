import json
import requests
from requests.auth import HTTPBasicAuth
import sys
    

sys.path.insert(1, r'C:\Users\Administrator\Documents\Projects\scrapper_JD') # Path para Lightsail
#sys.path.insert(1, '/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final') # Path para test personal

import API_CREDENTIALS


'''
# Load the JSON file into a Python dictionary
with open('/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/GoldenGalapagos/all_info.json', 'r') as f:
    data = json.load(f)
'''

    


def update_price_and_availability(boat_id=None, cabin_type_id=None):
    
    file_json = open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\GoldenGalapagos\Requests\request_boat_{}_cabin_type_{}.json'.format(boat_id, cabin_type_id), 'r') # Path para Lightsail
    #file_json = open('/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/GoldenGalapagos/Requests/request_boat_{}_cabin_type_{}.json'.format(boat_id, cabin_type_id), 'r') # Para uso persona;
    data = file_json.read()
    
    #print(type(data))
    
    data = json.loads(data) 
    
    

    '''
    Code to manually transform the 'departures' list to string
    '''
    #list_string = json.dumps(data['departures'])
    #data['departures'] = list_string

    url = '{}{}'.format(API_CREDENTIALS.API_URL, API_CREDENTIALS.UPDATE_PRICE_AND_AVAILABILITY_PATH)

    response = requests.post(url, json=data,
                             auth=HTTPBasicAuth(API_CREDENTIALS.API_USER, API_CREDENTIALS.API_PASS),
                             headers= API_CREDENTIALS.HEADERS)


    print(f"\tRequest made for: boat_id: {boat_id} and cabin_type: {cabin_type_id}")
    print(f"\tStatus code of response: {response.status_code}\n")



def send_information(final_json):
    
    
    #print(final_json)
    
    
    for boat_id in final_json:
        for cabin_type_id in final_json[boat_id]:

            info_in_json = final_json[boat_id][cabin_type_id]
            list_string = json.dumps(info_in_json['departures'])
            
            info_in_json['departures'] = list_string
            
            #print(info_in_json)
    
    
            f = open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\GoldenGalapagos\Requests\request_boat_{}_cabin_type_{}.json'.format(boat_id, cabin_type_id), 'w') # Path to use in Lightsail 
            #f = open('/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/GoldenGalapagos/Requests/request_boat_{}_cabin_type_{}.json'.format(boat_id, cabin_type_id), 'w')
            f.write(json.dumps(info_in_json))
            f.close()
    
            update_price_and_availability(boat_id, cabin_type_id)

        




#send_information(process_data(data))
#update_price_and_availability(31,240)


           
 






'''

def process_data(data):
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
                
    
    return aux_dict
'''










