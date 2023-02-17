import json

URL = 'https://nemofleet.com/availability/'

DRIVER_PATH_WINDOWS = r"C:\SeleniumDrivers" # For use in Lightsail

DRIVER_PATH_PERSONAL = '/Users/juandiegovaca/Downloads' # For personal use

MONTH_SELECTOR_PATH = '/html/body/div[1]/div[3]/div[1]/div/div/div[1]/div[1]/div[1]/div[2]/select'
SPECIFIC_MONTH_GENERAL_PATH = '/html/body/div[1]/div[3]/div[1]/div/div/div[1]/div[1]/div[1]/div[2]/select/option[{}]'  # Starts in 2

DATES_PATH = '/html/body/div[1]/div[3]/div[1]/div/div/div[1]/div[1]/div[3]/div[1]/table/tbody/tr[{}]/td[1]'
AVAILABILITY_CLASS_NAME = 'badge badge-default'.replace(' ', '.') 
BOAT_NAME_PATH = '/html/body/div[1]/div[3]/div[1]/div/div/div[1]/div[1]/div[3]/div[1]/table/tbody/tr[{}]/td[2]/span[2]/a'


ALL_BOAT_NAMES = []
BOAT_NAME_FROM_CODE = {
    'N1' : 'Nemo I',
    'N2' : 'Nemo II',
    'N3' : 'Nemo III',
    }

ALL_DATES = []
START_DATES = []
END_DATES = []
DAYS = []
AVAILABILITIES = []




def return_boats_data():
    #with open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\boats_ids.json', 'r') as boats_fp: # Path para Lightsail
    with open("/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/boats_ids.json") as boats_fp: # Path para uso personal
        return json.load(boats_fp)

def return_cabin_ids():
    #with open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\GAdventures\cabin_id_gadventure_internal.json', 'r') as f: # Path para Lightsail
    with open("/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/Nemo/cabins_internal_nemo.json") as cabins_fp: # Path para uso personal
        return json.load(cabins_fp)





BOATS = return_boats_data()
CABINS = return_cabin_ids()

COMPLETE_JSON = {}