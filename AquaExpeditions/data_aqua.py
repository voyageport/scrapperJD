URL = 'https://book.aquaexpeditions.com/'

DRIVER_PATH_WINDOWS = r"C:\SeleniumDrivers" # For use in Lightsail
DRIVER_PATH_PERSONAL = '/Users/juandiegovaca/Downloads' # For personal use

# SEARCH FILTERS
DESTINATION_SELECTOR_PATH = '/html/body/div[1]/div/section/main/div[2]/div/div[1]/div/form/div[1]/div/div/div/span/span/i'
GALAPAGOS_PATH = '/html/body/div[2]/div[1]/div[1]/ul/li[3]'



MONTH_SELECTOR_PATH = '/html/body/div[1]/div/section/main/div[2]/div/div[1]/div/form/div[2]/div/div/div[2]/span'
MONTH_SELECTOR_PATH = '/html/body/div[1]/div/section/main/div[2]/div/div[1]/div/form/div[2]/div/div'



MONTHS_PATH = '/html/body/div[{}]/div[1]/div[1]/ul/div[2]/div[2]/div[{}]/div/div[{}]/li' #.format(3(2023)/5(2024-25), año, mes)
#YEAR_GENERAL = '/html/body/div[3]/div[1]/div[1]/ul/div[2]/div[1]/div/div/div/div[{}]' # 3 : 2024 ; 4 : 2025
YEAR_GENERAL = '/html/body/div[5]/div[1]/div[1]/ul/div[2]/div[1]/div/div/div/div[{}]' # 3 : 2024 ; 4 : 2025
YEAR_2024_PATH = '/html/body/div[3]/div[1]/div[1]/ul/div[2]/div[1]/div/div/div/div[3]' # Uninteracted

SUITE_SELECTOR_PATH = '/html/body/div[1]/div/section/main/div[2]/div/div[1]/div/form/div[3]/div/div/div/span/span/i'
SUITE_SPECIFIC_PATH = '/html/body/div[4]/div[1]/div[1]/ul/li[1]'



DATES_PATH_GENERAL = '/html/body/div[1]/div/section/main/div[5]/div[{}]/div/div/div[2]/div[1]/div[2]/div/div[{}]' # Tour empieza en 1 & Fecha en 2

PRICE_PATH_GENERAL = '/html/body/div[1]/div/section/main/div[5]/div[{}]/div/div/div[2]/div[2]/label/span' # Empieza en 1

DEPARTURE_DATES = []
ARRIVAL_DATES = []
PRICES = []
AVAILABILITIES = []

COMPLETE_JSON = {}