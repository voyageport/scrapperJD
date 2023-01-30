import json
import datetime

URL = 'https://www.gadventures.com/travel-styles/cruising/galapagos/'

DRIVER_PATH_WINDOWS = r"C:\SeleniumDrivers" # For use in Lightsail
DRIVER_PATH_PERSONAL = '/Users/juandiegovaca/Downloads' # For personal use


MONTHS = ['January 2023', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY' 'AUGUST', 'SEPTEMBER', 'OCTOBRE', 'NOVEMBER', 'DECEMBER']

MONTHS_SHORT = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

CLOSE_COOKIES_CLASS_NAME = 'onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon'.replace(' ', '.')

VIEW_ALL_TOURS_BUTTON_CLASS_NAME = 'heroBtn'

TOURS_CONTAINER_CLASS_NAME = 'ais-Hits'

INDIVIDUAL_TOURS_CLASS_NAME = 'ais-Hits-item'

TOURS_NAMES_CLASS_NAME = 'name'

TOUR_TITLES = []

TOUR_TITLES_CRUISE_ONLY = []


PROMO_INFO_CLASS_NAME = 'promo-alert'
PROMOS_PERCENTAGES = []
PROMOS_START_DATES = []
PROMOS_END_DATES = []



def return_boats_data():
    #with open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\boats_ids.json', 'r') as f: # Path para Lightsail
    with open("/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/boats_ids.json") as boats_fp: # Path para uso personal
        return json.load(boats_fp)
    
def return_cabin_ids():
    #with open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\GAdventures\cabin_id_gadventure_internal.json', 'r') as f: # Path para Lightsail
    with open("/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/GAdventures/cabin_id_gadventure_internal.json") as cabins_fp: # Path para uso personal
        return json.load(cabins_fp)

BOATS = return_boats_data()

CABIN_IDS_INTERNAL = return_cabin_ids()


CRUISES_TO_ADD = []

DATES_INFO = []

LINKS_TO_VISIT = []

XPATH_INDEXES = [4, 7, 8] # Indexes used in XPATH of first date of itinerary


# **************************************
# **************************************
# ******** DATA FOR DICTIONARIES *******
# **************************************
# **************************************


COMPLETE_JSON = {} # External dictionary for json (has the cruise number in the GDS), the key is going to be the cruise

# Dictionaries for each cabin type
DICT_Main_Deck_Balcony_Double_Twin = {
        "Main Deck Balcony Double/Twin" : {}
    }


DICT_Main_Deck_Double = {
        "Main Deck Double" : {}
    }



DICT_Upper_Deck_Balcony_Single = {
    
        "Upper Deck Balcony Single" : {}
    }



DICT_Upper_Deck_Balcony_Double_Twin = {
    
        "Upper Deck Balcony Double/Twin"
    }


DICT_DEPARTURES_TEMP = {}

DEPARTURE_DATE_TEMP = None
ARRIVAL_DATE_TEMP = None













