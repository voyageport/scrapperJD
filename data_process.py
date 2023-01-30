from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

import json
import data_gogalapagos



def process_info():
    data = open('all_data.json', 'r')
    data = data.read()
    data = json.loads(data)
    
    dict_ships = {}
    
    #print(data[0].keys()) # ['id', 'status', 'start_date', 'end_date', 'nights', 'duration_id', 'code', 'combination_itinerary', 'availability', 'cabin_max', 'commission', 'min_gross', 'min_net', 'promotions_cabin', 'ship', 'itinerary', 'promotion', 'languages', 'extensions', 'cabins']
    

    
    for i in range(len(data)):
    #for i in range(1): For only one boat 

        departure_temp = data[i]['start_date']
        departure_temp = datetime.strptime(departure_temp, '%Y-%m-%d').date()

        arrival_temp = data[i]['end_date']
        arrival_temp = datetime.strptime(arrival_temp, '%Y-%m-%d').date()

        
        date_difference  = get_days_difference(departure_temp, arrival_temp)

        if  data[i]['ship']['name'] == 'Coral I & Coral II':
            boat_name =  "Coral I / II"
        else:
            boat_name = data[i]['ship']['name']
    
        for j in range(len(data[i]['cabins'])):
        #for j in range(2): # For only 2 dates repetition in the same boat

            boat_id = data_gogalapagos.BOATS_DATA[boat_name]
            cabin_type_text = data[i]['cabins'][j]['nombre']
            cabin_id =   data_gogalapagos.CABIN_IDS_INTERNAL[str(boat_id)][cabin_type_text]
            
            promotion_name, new_price = get_promotion_percentage(data[i]['cabins'][j]) #Gets the promotion (if there's one)
            
            dict_departures_temp = {
                'departure_date' : None,
                'arrival_date' : None,
                'days' : 0,
                'available' : 0,
                'hold' : 0,
                'adult_price' : None 
                }
            
            if boat_id not in dict_ships.keys():
                """
                Ship ID is entered to the JSON file as a new key
                """
                dict_ships[boat_id] = {}

            if cabin_id not in dict_ships[boat_id].keys():
                dict_ships[boat_id][cabin_id] = {
                    'boat' : boat_id,
                    'cabin' : cabin_id,
                    'departures' : []
                    }
                
            dict_departures_temp['departure_date'] = str(departure_temp)
            dict_departures_temp['arrival_date'] = str(arrival_temp)
            dict_departures_temp['days'] = date_difference
            dict_departures_temp['available'] = int(data[i]['cabins'][j]['disponible'])
            
            if promotion_name == None:
                """
                If there's no promotion, then the normal price is added
                """
                dict_departures_temp['adult_price'] = int(data[i]['cabins'][j]['tarifa_base'])
                dict_departures_temp['promotion_name'] = 'season price' # Needed in order for price to update
            else:
                """
                If there is a promotion, then its name is added, and the new price is saved in the JSON file
                """
                dict_departures_temp['adult_price'] = int(new_price)
                dict_departures_temp['promotion_name'] = str(promotion_name)
                
            dict_ships[boat_id][cabin_id]['departures'].append(dict_departures_temp)

    #print(dict_ships)    
    return dict_ships
    
    
    
def get_promotion_percentage(data):
    # Keys: ['codigo', 'nombre', 'orden', 'tarifa_base', 'tipo_habitacion', 
    #       'tipo_tarifa_id', 'disponible', 'opciones', 'promocion', 'estado', 
    #       'comision_general', 'descuento', 'tarifa_comision', 'tarifa_descuento']
    
    if data['promocion'] != None:
        """
        Code only runs if there's a promotion
        """        
        return data['promocion']['name'], data['tarifa_descuento'] # Returns promotion name, and price with promotion applied
    
    else:
        """
        If there's no promotion, then None is returned
        """
        return None, None
    
    
   
def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year = d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))
    
    
def add_days(d, t):
    new_date = date.today() + relativedelta(days=t)
    return new_date

def add_months(d, m):
    new_date = d + relativedelta(months=m)
    return new_date

def subtract_months(d, m):
    new_date = d - relativedelta(months=m)
    return new_date



def get_days_difference(departure_date, arrival_date):
    date_difference  = str(arrival_date - departure_date)
    date_difference = date_difference.split(' ')
    date_difference = date_difference[0]
    return int(date_difference) + 1
    
      
      
      
      
      



