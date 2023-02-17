import json
import datetime

URL = 'https://partners.oniriccruises.com/availability-view'

DRIVER_PATH_WINDOWS = r"C:\SeleniumDrivers" # For use in Lightsail
DRIVER_PATH_PERSONAL = '/Users/juandiegovaca/Downloads' # For personal use


ALL_DATA_PATH = '/html/body/div[1]/div/div/div/div/div[3]'

DATE_SELECTOR_PATH = '/html/body/div[1]/div/div/div/div/span/div/div[1]/div/div/div[1]/div/div/div/b'
NEXT_MONTH_CLASS_NAME = 'next available'.replace(' ', '.')
START_DAY_PATH = '/html/body/div[1]/div/div/div/div/span/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr[2]/td[1]' # Clicks on first day displayer
END_DAY_PATH = '/html/body/div[1]/div/div/div/div/span/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr[7]/td[7]' # Clicks on last day displayed
REFRESH_BUTTON_CLASS_NAME = 'glyph-icon simple-icon-refresh'.replace(' ', '.')

INFO_COLUMNS_CLASS_NAME = 'row row no-gutter header-title row-avai border-top-0'.replace(' ', '.')
#INFO_COLUMNS_CLASS_NAME = 'row row no-gutter header-title row-avai border-top-0'.replace(' ', '.')

BOAT_NAME_CLASS_NAME = 'yachtname-check align-items-center custom-control custom-checkbox'.replace(' ', '.')

COLUMNS_INFO = [] # Stores the HTML of all columns (all info)
ALL_BOAT_NAMES = ['Archipel I', 'Aqua', 'Solaris', 'Treasure'] # Stores all the boat names for JSON creation
CABINS_INTERNAL = {
    'Archipel I' : 654,
    'Aqua' : 655,
    'Solaris' : 653,
    'Treasure' : 652
    }

DEPARTURE_DATES = []
DEPARTURE_DATES_TREASURE = [] # Stores all the departure dates
DEPARTURE_DATES_SOLARIS = [] # Stores all the departure dates
DEPARTURE_DATES_ARCHIPEL = [] # Stores all the departure dates
DEPARTURE_DATES_AQUA = [] # Stores all the departure dates


ARRIVAL_DATES = [] # Stores all the arrival dates
ARRIVAL_DATES_TREASURE = [] # Stores all the arrival dates
ARRIVAL_DATES_SOLARIS = [] # Stores all the arrival dates
ARRIVAL_DATES_ARCHIPEL = [] # Stores all the arrival dates
ARRIVAL_DATES_AQUA = [] # Stores all the arrival dates


AVAILABILITIES = []
AVAILABILITIES_TREASURE = []
AVAILABILITIES_SOLARIS = []
AVAILABILITIES_ARCHIPEL = []
AVAILABILITIES_AQUA = []

HOLD = []
HOLD_TREASURE = []
HOLD_SOLARIS = []
HOLD_ARCHIPEL = []
HOLD_AQUA = []

PRICES = []
PRICES_TREASURE = []
PRICES_SOLARIS = []
PRICES_ARCHIPEL = []
PRICES_AQUA = []

def return_boats_data():
    #with open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\boats_ids.json', 'r') as boats_fp: # Path para Lightsail
    with open("/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/boats_ids.json") as boats_fp: # Path para uso personal
        return json.load(boats_fp)

BOATS  = return_boats_data()













COMPLETE_JSON = {}