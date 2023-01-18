import json

from datetime import date
from dateutil.relativedelta import relativedelta


def add_years():
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    
    new_year = date.today().year + 1
    return new_year



DRIVER_PATH_WINDOWS = r"C:\SeleniumDrivers" # For use in Lightsail
DRIVER_PATH_PERSONAL = '/Users/juandiegovaca/Downloads' # For personal use

BARCOS = ['endemic', 'elite', 'petrel', 'oceanspray']

CABINAS_FINAL = []

NOMBRE_CABINAS = []

AVAILABILITIES_FINAL = []

PROMOS_FINAL = []

COMPLETE_JSON = {}

URL = 'https://www.goldengalapagoscruises.com/'

def month_determinator():
    """
    Automates that selected month is 6 months from today
    """
    new_date = date.today() + relativedelta(months=+6)
    return int(new_date.month)
    


# ****************************************
# ********* PATHS & CLASS NAME ***********
# ****************************************


ALL_DATA_PATH = '/html/body/div[1]/div/main/div/section/div/div/div[5]/div/div/div[2]/div[1]/div[3]'

TOTAL_SHIPS = 4

CRUISES_AND_DATES = [0]

END_DATE_PATH = '/html/body/div[1]/div/main/div/section/div/div/div[2]/div/div/div/div/div[7]/div/form/div/fieldset/div/div[2]/input'

YEAR_CLASS_NAME = 'ui-datepicker-year'
YEAR_SELECTION_PATH = '/html/body/div[9]/div/div/select[2]/option[{}]'.format(add_years() - 2012)


MONTH_CLASS_NAME = 'ui-datepicker-month'
MONTH_PATH ='/html/body/div[9]/div/div/select[1]'
MONTH_SELECTION_PATH = '/html/body/div[9]/div/div/select[1]/option[{}]'.format(month_determinator())


DAY_SELECTION_PATH = '/html/body/div[8]/table/tbody/tr[3]/td[5]/a' # Random day 
DAY_SELECTION_CLASS_NAME = 'ui-state-default'


GUESTS_PATH = '/html/body/div[1]/div/main/div/section/div/div/div[2]/div/div/div/div/div[7]/div/form/div/fieldset/div/div[4]/select'
GUESTS_2_PATH = '/html/body/div[1]/div/main/div/section/div/div/div[2]/div/div/div/div/div[7]/div/form/div/fieldset/div/div[4]/select/option[2]'

SEARCH_BUTTON_PATH = '/html/body/div[1]/div/main/div/section/div/div/div[2]/div/div/div/div/div[7]/div/form/div/fieldset/div/div[7]/button' 

AVAILABILITIES_CLASS_NAME = 'important-data'

CABINAS_CSS_SELECTOR = "[id^='cabin'"



# ****************************************
# ************** API INFO ****************
# ****************************************

URL_API = 'http://test.supplier.voyageport.com/product/cabins'


FILES= [

        ]

HEADERS = {
  'Token': '4d673d3d', #'4d544532' (Cristiano)
  'Authorization': 'Basic aW5mb0B2b3lhZ2Vwb3J0LmNvbTpNM3Q0JTRkbTFuIzIw',
  'Cookie': 'laravel_session=eyJpdiI6InVpV2x3T1lJTWszOTE0eElLSGUxZ2c9PSIsInZhbHVlIjoidHZDTFdKdE9zZXRobUF4T0ZtRWRHaE00SSsyeTFPMXUyNHFZTng1enNDOHljYlY1TG5LeHVaYVp3R2hsSDFUMSIsIm1hYyI6IjQ4MWU2N2VjNzA0ODdiNGJiNTlhOTk1M2VlNTZmYmY3MDYxMjVlYWQxNDVlODBiYmI2MTAwMTA2OWEyNjk4MjEifQ%3D%3D'
}

"""
Gets the boat ID for every page (such as Endemic, Elite, or Oceanspray)
"""
with open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\boats_ids.json', 'r') as f: # Path para Lightsail
#with open('/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/boats_ids.json', 'r') as f: # Path para uso personal
    data = json.load(f)
    

BOATS_IDS_FOR_API = data
#print(BOATS_IDS_FOR_API['oceanspray'])


TEMP_YEAR = 0

TEMP_PREV_YEAR = 2023


FLAG = True # Flag that keeps track if there is a ship on a year-change (departure in December and arrival in January)
FLAG_YEAR_TO_USE = 0






with open(r'C:\Users\Administrator\Documents\Projects\scrapper_JD\GoldenGalapagos\cabin_types_internal.json', 'r') as f: # Path para Lightsail
#with open('/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/GoldenGalapagos/cabin_types_internal.json', 'r') as f: # Path para uso personal
    data2 = json.load(f)

CABIN_IDS_INTERNAL = data2








