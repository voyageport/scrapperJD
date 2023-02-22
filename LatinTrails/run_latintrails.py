from datetime import date

import requests
import json
import time
import data_latin
from datetime import datetime
from data_latin import COMPLETE_JSON

import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
#sys.path.insert(1, r'C:\Users\Administrator\Documents\Projects\scrapper_JD') # Path to use in Lightsail
sys.path.insert(1, '/Users/juandiegovaca/Desktop/Voyageport/Screen Scraping/Version Control/Final/') # Path para uso personal
import send_information

"""
TO DO:
    1. Chequear si funciona para 2024
"""




TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkxhdGluIFRyYWlscyIsImlhdCI6MTUxNjIzOTAyMn0.alP1FcKBWM7d0uHZfYphM-j-G4HTc_pxh3bLPGSWbkk'

params= {
    'Authorization' : 'Bearer ' + TOKEN
    
    }




for j in range(2):
    
    if j == 0:
        today = datetime.today().date()
    elif j == 1:
        today = datetime(2024, 1, 1).date()
    else:
        print('Unnecessary repetitions')
    #print(today)
    
    response = requests.get(f'https://app.latintrails.com/availability?cruise=seaman-journey&start={today}&allYear=true', headers = params)
    response = response.text
    #print(response)
    
    
    
    
    #response = open('example.txt', 'r')
    #response = response.read()
    
    json_all = json.loads(response)

#print(json_all[0].keys()) # Keys: 'cabin_type', 'itinerary', 'cruise', 'days', 'nights', 'start', 'end', 'spaces', 'hold', 'rackRate', 'cabinNumber'


    for i in range(len(json_all)):
        """
        CABIN ID
        """
    
        cabin_name =  json_all[i]['cabin_type']
        cabin_id = data_latin.CABINS[cabin_name]
        
        if str(cabin_id) not in COMPLETE_JSON['3'].keys():
            COMPLETE_JSON['3'][str(cabin_id)] = {
                'boat' : '3',
                'cabin' : str(cabin_id),
                'departures' : []
                }
            #print(cabin_id)
        
        dict_departures_temp = {
            'departure_date' : 0,
            'arrival_date' : 0,
            'days' : 0,
            'available' : 0,
            'hold' : 0,
            'adult_price' : 0,
            'promotion_name' : 'season price'
            }
        
        
        """
        START & END DATES
        """
        start_date = json_all[i]['start'] 
        #print(start_date, end = '\t')
        end_date = json_all[i]['end'] 
        #print(end_date, end = '\n')
        
        dict_departures_temp['departure_date'] = start_date
        dict_departures_temp['arrival_date'] = end_date
        
        
        """
        AVAILABLE
        """
        available = json_all[i]['spaces'] 
        #print(available)
        dict_departures_temp['available'] = available
        
    
        """
        HOLD
        """
        hold = json_all[i]['hold'] 
        #print(hold)
        dict_departures_temp['hold'] = hold
        
    
        """
        PRICES
        """    
        price = json_all[i]['rackRate'] 
        #print(price)
        dict_departures_temp['adult_price'] = price
        
        #print(dict_departures_temp)
        if dict_departures_temp['available'] != 0:
            COMPLETE_JSON['3'][str(cabin_id)]['departures'].append(dict_departures_temp)
    


#print(COMPLETE_JSON)

send_information.send_information(COMPLETE_JSON, 'LatinTrails', False)














