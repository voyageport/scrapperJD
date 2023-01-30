from requests.auth import HTTPBasicAuth
from datetime import date

import requests
import json
import data_gogalapagos
import data_process
import time

import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
#sys.path.insert(1, r'C:\Users\Administrator\Documents\Projects\scrapper_JD') # Path to use in Lightsail
sys.path.insert(1, '/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/') # Path para uso personal

import send_information

"""
To do:
    1. Asegurarse que en COMPLETE_JSON se estén almacenando cada fecha como diccionario y no como lista
    2. Revisar precios
    3. Incluir promociones

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
    
def get_info_from_api(from_date, until_date):
    
    complete_url = data_gogalapagos.BASE_URL + data_gogalapagos.AVAILABILITIES_TAG
    
    params = {
        "from" : from_date,
        "until" : until_date, # Sets the search a year in the future
        "paxs" : 1
        }

    #print('** from sent: {}\t\tuntil sent: {}'.format(from_date, until_date))
    

    response = requests.get(complete_url, headers = data_gogalapagos.HEADERS, params = params)
    data = response.json()
 
    return data

 
def determine_day(i):
    return data_process.add_months(date.today(), 1 * i), data_process.add_months(data_process.add_months(date.today(), 1 * i), 1)
    


print('Logging in to GoGalapagos API...', end = '\t\t')
login_to_api() # API Authentication
print('Access successful')
time.sleep(1)

months = 12
print('\nGetting info {} months in advance...'.format(months))


for i in range(months): # Iteration is equal to the number of months that are desired
    from_date, until_date = determine_day(i)
    #print('from: {}\t\tuntil: {}'.format(from_date, until_date))

    
    json_example = get_info_from_api(from_date, until_date) # Gets all info for time lapse
    for i in range(len(json_example)):
        data_gogalapagos.COMPLETE_JSON_LIST.append(json_example[i])


#print('*** FINAL *** ', data_gogalapagos.COMPLETE_JSON_LIST[0])




print('Processing data...')
json_object = json.dumps(data_gogalapagos.COMPLETE_JSON_LIST) # Creates object in order to save it as file

# Saves returned info to file 
with open("all_data.json", "w") as outfile:
    outfile.write(json_object)
    
outfile.close()

# Gets the JSON file in the format for GDS
final_json = data_process.process_info()

print('Info ready to be sent to GDS...')
time.sleep(1)
#print(final_json)


# Sends info to the API
print('Sending info to API...')
send_information.send_information(final_json, 'GoGalapagos')

print('\n\n*** Process finished succesfully!')





    

















