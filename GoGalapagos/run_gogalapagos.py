from requests.auth import HTTPBasicAuth
from datetime import date

import requests
import json
import data_gogalapagos
import data_process

import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, r'C:\Users\Administrator\Documents\Projects\scrapper_JD') # Path to use in Lightsail
#sys.path.insert(1, '/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/') # Path para uso personal

import send_information

"""
To do:
    1. Revisar precios
    2. Incluir promociones

Notas:
    * Se hace request para 1 año en el futuro y se recibe solo hasta marzo 2023


Preguntas:
    1) ¿Qué hacer si hay promos por cabina Y promos para toda la fecha?
    2) ¿Cómo manejar las 'extensions'?
"""




url = 'https://goware.net/api/v2'
tag = '/login'


USER = 'VOYAGEPO-698cc7'
PASS = 'Vo4ya1o1'

headers = {
    

    }

auth_params = {
    "username" : USER,
    "password" : PASS
    
    }


def login_to_api():
    
    complete_url = url + '/login'
    params = {
        "username" : USER,
        "password" : PASS
        
        }
    
    response = requests.post(complete_url, json = params)
    response = response.json()
    
    """
    Stores the token
    """
    #token = response['access_token']
    data_gogalapagos.API_TOKEN = response['access_token']
    
    
    #headers['Authorization'] = 'Bearer ' + token
    data_gogalapagos.HEADERS['Authorization'] = 'Bearer ' + data_gogalapagos.API_TOKEN
    
def get_info_from_api():
    
    complete_url = data_gogalapagos.BASE_URL + data_gogalapagos.AVAILABILITIES_TAG
    
    params = {
        "from" : date.today(),
        "until" : data_process.add_years(date.today(), 2), # Sets the search a year in the future # add_days(date.today(), 60)
        "paxs" : 1
        }

    print('** from sent: {}\t\tuntil sent: {}'.format(date.today(), data_process.add_years(date.today(), 1)))
    
    response = requests.get(complete_url, headers = data_gogalapagos.HEADERS, params = params)
    data = response.json()
    
    #print(data[len(data)-1])
    
    return data 
 



print('Logging in to API')
login_to_api() # API Authentication
print('Access successful')

print('Getting info a year in advance')
json_example = get_info_from_api() # Gets all info for time lapse

print('Processing data')
json_object = json.dumps(json_example) # Creates object in order to save it as file

# Saves returned info to file 
with open("all_data.json", "w") as outfile:
    outfile.write(json_object)
    
outfile.close()

# Gets the JSON file in the format for GDS
final_json = data_process.process_info()

print(final_json)

# Sends info to the API
print('Sending info to API')
send_information.send_information(final_json, 'GoGalapagos')






    

















