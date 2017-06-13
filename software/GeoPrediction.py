from geopy.geocoders import Nominatim
from collections import Counter

import DB

db = DB.db()

def dictGeoGenerator(geotagged):
    geo = {}
    for doc in geotagged:
        if doc['coordinates'] is not None:
            geolocator = Nominatim()
            k = str(doc["user"]["screen_name"])
            q = str(doc["coordinates"]["coordinates"][0])
            r = str(doc["coordinates"]["coordinates"][1])
            location = geolocator.reverse(q + ", " + r, timeout = 25)
            loc = str(location.address)
            if loc is not None:
                geo[k] = loc
        else:
            k = str(doc["user"]["screen_name"])
            q = str(doc["place"]["name"])
            if q is not None:
                geo[k] = q
    return geo

def printGeotaggedCities(geo):
    for key, value in geo.items():
        print(key + " : " + value)

def getUniqueUsersPerLoc(av):
    # Top-20 inferenced cities
    g = ['Manhattan', 'Washington', 'Los Angeles', 'Chicago', 'Toronto', 'Houston', 'Brooklyn', 'Boston', 'Philadelphia', 'Austin', 'San Francisco', 'Phoenix', 'Dallas', 'Denver', 'Portland', 'Paris', 'Seattle', 'San Antonio', 'Columbus', 'Pittsburgh']
    d = {}
    for r in g:
        i = 0
        for key, value in av.items():
            w = str(r)
            q = str(value)
            if ((i != 30)&(w == q)&(key not in d)):
                i = i + 1
                k = str(key)
                v = str(value)
                d[k] = v
                db.insertOneDummy(k, v)
    return list(d)