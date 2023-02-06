import json

DRIVER_PATH_WINDOWS = r"C:\SeleniumDrivers" # For use in Lightsail
DRIVER_PATH_PERSONAL = '/Users/juandiegovaca/Downloads' # For personal use

URL = 'https://www.intrepidtravel.com/en'

CLOSE_COOKIES_CLASS_NAME = 'onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon'.replace(' ', '.')

SEARCH_BOX_PATH = '/html/body/div[1]/header/div/div[2]/div[2]/div/div/div/div/div[1]/div/div/input'

CHECK_BOX_ADVENTURE_CRUISING_PATH = '/html/body/div[1]/div/div/div[4]/div[2]/div[5]/div[2]/div[2]/div'

DISMISS_US_LOCATION_PATH = '/html/body/div[1]/footer/div/div[4]/div/div/button[2]'

NUMBER_OF_TRIPS_PATH = '/html/body/div[1]/div/div/div[3]/div/span/strong'

#INDIVIDUAL_TRIP_CARD_CLASS_NAME = 'l-grid__cell l-grid__cell--flex l-grid__cell--12-col l-grid__cell--6-col-desktop l-grid__cell--4-col-tablet'.replace(' ', '.')

INDIVIDUAL_TRIP_CARD_CLASS_NAME = 'card__content card__content--link'.replace(' ', '.')

LINKS_TO_VISIT = []

NEXT_PAGE_PATH = '/html/body/div[1]/div/div/div[5]/div[3]/div[4]/button'
                  
CLOSE_COOKIES_2_PATH = '/html/body/div[4]/div[3]/div/div[2]/button'

CLOSE_COOKIES_2_CLASS_NAME = 'onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon'.replace(' ', '.')

DATE_SELECTOR_CLASS_NAME = 'btn btn-month-selector date ng-binding'.replace(' ', '.')

TOTAL_DAYS_CLASS_NAME = 'product-info__content'

TOUR_TITLE_CLASS_NAME = 'banner__heading'

START_CITY_PATH = '/html/body/div[1]/div/section/div[4]/div[1]/dl/dd[1]'

FINISH_CITY_PATH = '/html/body/div[1]/div/section/div[4]/div[1]/dl/dd[2]'

VIEW_MORE_DEPARTURES_CLASS_NAME = 'btn btn-lg btn-block btn-passive'.replace(' ', '.')

VIEW_MORE_DEPARTURES_PATH = '/html/body/div[1]/div/section/div[12]/div/div/div[2]/div/div/div/div[3]/button'

#INDIVIDUAL_DATES_INFO_CLASS_NAME = 'info-date collapsed'.replace(' ', '.')
INDIVIDUAL_DATES_INFO_CLASS_NAME = 'info-date'
INDIVIDUAL_DATES_INFO_CSS = "[id^='panel-id'"

INDIVIDUAL_DATES_PATH = '/html/body/div[1]/div/section/div[12]/div/div/div[2]/div/div/div/div[2]/div[{}]/div[1]'


TOTAL_NUMBER_OF_DAYS = 0

DEPARTURES_DATES_LIST = []

ARRIVAL_DATES_LIST = []

POP_UP_INTRUSIVE_PATH = '/html/body/div[2]/div/div/div[2]/div[1]/button'

CABIN_TYPES_PATH_GENERAL = '/html/body/div[1]/div/section/div[12]/div/div/div[2]/div/div/div/div[2]/div[{}]/div[2]/div[{}]/div/div/div/div[1]/h4'

PRICES_PATH_GENERAL = '/html/body/div[1]/div/section/div[12]/div/div/div[2]/div/div/div/div[2]/div[{}]/div[2]/div[{}]/div/div/div/div[2]'

AVAILABILITIES_PATH_GENERAL = '/html/body/div[1]/div/section/div[12]/div/div/div[2]/div/div/div/div[2]/div[{}]/div[2]/div[{}]/div/div/div/div[3]'

COMPLETE_JASON = {}

def return_boats_data():
    #with open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\boats_ids.json', 'r') as boats_fp: # Path para Lightsail
    with open("/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/boats_ids.json") as boats_fp:
        return json.load(boats_fp)
    
BOATS_DATA = return_boats_data()

def return_cabin_ids():
    #with open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\Intrepid\internal_cabins_intrepid.json', 'r') as cabins_fp: # Path para Lightsail
    with open("/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/Intrepid/internal_cabins_intrepid.json") as cabins_fp: # Path para uso personal
        return json.load(cabins_fp)

CABINS_IDS_INTERNAL = return_cabin_ids()








