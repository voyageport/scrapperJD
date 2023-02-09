import json

DRIVER_PATH_WINDOWS = r"C:\SeleniumDrivers" # For use in Lightsail
DRIVER_PATH_PERSONAL = '/Users/juandiegovaca/Downloads' # For personal use

URL = 'https://www.galagentsdisponibilidad.com/servicio/_dispo/search/{}/{}/{}'
NUMBER_OF_BOATS = 5

BOATS_NAMES_DICT = {
    '1' : 'Galaxy',
    '2' : 'EcoGalaxy',
    '3' : 'Alya',
    '4' : 'Bonita',
    '5' : 'Galaxy Diver'
    }

CABINS_ID_WEB = {
    'Galaxy' : {
        '1' : 'Lower Deck',
        '2' : 'Lower Deck',
        '3' : 'Main Deck',
        '4' : 'Main Deck',
        '5' : 'Main Deck',
        '6' : 'Upper Deck',
        '7' : 'Upper Deck',
        '8' : 'Upper Deck',
        '9' : 'Upper Deck',
        'All boat' : 626
        },
    'EcoGalaxy' : {
        '2' : 'Main Deck',
        '3' : 'Main Deck',
        '4' : 'Main Deck',
        '5' : 'Main Deck',
        '6' : 'Upper Deck',
        '7' : 'Upper Deck',
        '8' : 'Upper Deck',
        '9' : 'Upper Deck',
        'All boat' : 627
        },
    'Alya' : {
        '1' : 'Main Deck',
        '2' : 'Main Deck',
        '3' : 'Main Deck',
        '4' : 'Main Deck',
        '5' : 'Main Deck',
        '6' : 'Upper Deck',
        '7' : 'Upper Deck',
        '8' : 'Upper Deck',
        '9' : 'Upper Deck',
        'All boat' : 628
        },
    'Bonita' : {
        '1' : 'Lower Deck',
        '2' : 'Lower Deck',
        # Page does not show any cabin #3
        '4' : 'Lower Deck', 
        '5' : 'Main Deck',
        '6' : 'Main Deck',
        '7' : 'Upper Deck',
        '8' : 'Upper Deck',
        '9' : 'Upper Deck',
        '10' : 'Upper Deck',
        'All boat' : 629
        },
    'Galaxy Diver' : {
        '1' : 'Lower Deck',
        '2' : 'Lower Deck',
        '3' : 'Lower Deck',
        '4' : 'Lower Deck',
        '5' : 'Main Deck',
        '6' : 'Upper Deck',
        '7' : 'Upper Deck',
        '8' : 'Upper Deck',
        '9' : 'Upper Deck',
        'All boat' : 630
        },
    'Galaxy Daily' : {
        # New ship
        # Seems like there's only a Main Deck
        }
    }

def return_boats_data():
    #with open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\boats_ids.json', 'r') as f: # Path para Lightsail
    with open("/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/boats_ids.json") as boats_fp: # Path para uso personal
        return json.load(boats_fp)
    
BOATS_INTERNAL_IDS = return_boats_data()

COMPLETE_JSON = {}

























'''
URL = 'https://www.galagents.com/'

DRIVER_PATH_WINDOWS = r"C:\SeleniumDrivers" # For use in Lightsail
DRIVER_PATH_PERSONAL = '/Users/juandiegovaca/Downloads' # For personal use

CHAT_BOT_CLOSE_PATH = '/html/body/div/div/div/div/div[1]/i'
CHAT_BOT_CLOSE_PATH = '/html/body/div/div/div/div/div[1]/i'

# SEARCH FILTERS
CRUISE_SELECTOR_PATH = '/html/body/section[4]/div[1]/div/div/div/div[1]/form/div/div[1]/div/div/div/div'
SELECT_ALL_CRUISES_PATH = '/html/body/section[4]/div[1]/div/div/div/div[1]/form/div/div[1]/div/ul/li[3]/span/input'
START_DATE_PATH = '/html/body/section[4]/div[1]/div/div/div/div[1]/form/div/div[2]/div/input'
END_DATE_PATH = '/html/body/section[4]/div[1]/div/div/div/div[1]/form/div/div[3]/div/input'
PASSENGERS_PATH = '/html/body/section[4]/div[1]/div/div/div/div[1]/form/div/div[4]/div/input'
NUMBER_OF_PASSENGERS  = '2'

# DATA 
TOTAL_CRUISES = 4 # Galaxy, EcoGalaxy, Alya, Bonita
CRUISE_NAME_PATH = '/html/body/section[4]/div[2]/div/h3[{}]'
DATES_PATH_GENERAL = '/html/body/section[4]/div[2]/div/div[{}]/table/tbody/tr[{}]/td[1]' #.format(#barco*2 , #fila+1)













COMPLETE_JSON = {}






# BOATS AND CRUISES FILES:


'''




















 

