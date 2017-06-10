from geopy.geocoders import Nominatim


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
            geo[k] = q
    return geo

def printGeotaggedCities(geo):
    for key, value in geo.items():
        print(key + " : " + value)
