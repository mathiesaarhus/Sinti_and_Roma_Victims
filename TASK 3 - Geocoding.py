# Geocoding

import geopy
import pandas as pd
from geopy.exc import GeocoderTimedOut
import time


data = pd.read_csv("person_information.csv")
locator = geopy.Nominatim(user_agent="john.doe@gmail.com")

location_birth = data['place_of_birth'] 
location_death = data['place_of_death']
latitudes_birth = []
longitudes_birth = []
latitudes_death = []
longitudes_death = []

for i in range(len(location_birth)):
    print("Geocoding ...", location_birth[i])
    location = None
    try:
        location = locator.geocode(location_birth[i],timeout=10000)
        if location == None:
            latitudes_birth.append(0)
            longitudes_birth.append(0)
        else:
            latitudes_birth.append(location.latitude)
            longitudes_birth.append(location.longitude)
    except GeocoderTimedOut:
        print("Not able to geocode ...", location_birth[i])
        latitudes_birth.append(0)
        longitudes_birth.append(0)
    time.sleep(1)

for i in range(len(location_death)):
    print("Geocoding ...", location_death[i])
    location = None
    try:
        location = locator.geocode(location_death[i],timeout=10000)
        if location == None:
            latitudes_death.append(0)
            longitudes_death.append(0)
        else:
            latitudes_death.append(location.latitude)
            longitudes_death.append(location.longitude)
    except GeocoderTimedOut:
        print("Not able to geocode ...", location_death[i])
        latitudes_death.append(0)
        longitudes_death.append(0)
    time.sleep(1)
    

data['latitudes birth'] = latitudes_birth
data['longitudes birth'] = longitudes_birth
data['latitudes death'] = latitudes_death
data['longitudes death'] = longitudes_death

data.to_csv('person_information_geocoded.csv', index=False, encoding='utf-8')