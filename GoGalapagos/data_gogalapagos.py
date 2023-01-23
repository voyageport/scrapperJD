import json


BASE_URL = 'https://goware.net/api/v2'
LOGIN_TAG = '/login'
AVAILABILITIES_TAG = '/availabilities'

API_USERNAME = 'VOYAGEPO-698cc7'
API_PASSWORD ='Vo4ya1o1'
API_TOKEN = ''


HEADERS  = {
    }

def return_boats_data():
    with open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\boats_ids.json', 'r') as f: # Path para Lightsail
    #with open("/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/boats_ids.json") as boats_fp:
        return json.load(boats_fp)
    
BOATS_DATA = return_boats_data()


def return_cabin_ids():
    with open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\GoGalapagos\cabin_types_internal.json', 'r') as f: # Path para Lightsail
    #with open("/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/GoGalapagos/cabin_types_internal.json") as cabins_fp:
        return json.load(cabins_fp)
    
    
CABIN_IDS_INTERNAL = return_cabin_ids()

