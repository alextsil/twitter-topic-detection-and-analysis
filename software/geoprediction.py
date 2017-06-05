from geopy.geocoders import Nominatim
import DB

db=DB.db()

geotagged = db.getGeotagged()

def dictGeoGenerator():
    geo = {}
    for doc in geotagged:
        if doc['coordinates'] is not None:
            geolocator = Nominatim()
            k = str(doc["_id"])
            q = str(doc["coordinates"]["coordinates"][0])
            r = str(doc["coordinates"]["coordinates"][1])
            location = geolocator.reverse(q + ", " + r, timeout = 25)
            loc = location.address
            geo[k] = str(loc)
        else:
            k = str(doc["_id"])
            q = str(doc["place"]["full_name"])
            geo[k] = q
    return geo

def printGeotaggedCities(geo):
    for key, value in geo.items():
        print(key + " : " + value)
        
a = dictGeoGenerator()
printGeotaggedCities(a)