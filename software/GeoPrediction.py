from geopy.geocoders import Nominatim
from collections import Counter
from Preprocessing import stop, preprocess, regex_str
import re
import operator

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
                db.insertOneUserLoc(k, v)
    return list(d)

def getPredictions(allTweets, users):
    terms = []
    l = []
    for user in users:
        t = []
        t.append(str(user['screen_name']))
        t.append(str(user['location']))
        terms.append(t)
        if user['location'] not in l:
            l.append(user['location'])
    # Keep hashtag's regex
    regex_str.pop(2)
    regex_str.pop(3)
    regex_str.pop(3)
    regex_str.pop(3)
    regex_str.pop(3)
    regex_str.pop(3)
    # Make a combined regex of all regex-es
    reg = "(" + ")|(".join(regex_str) + ")"
    # Tokenization/(removing stopwords, urls, html, 
    for tweet in allTweets:
        for t in terms:
            if t[0] == str(tweet['user']['screen_name']):
                for term in preprocess(tweet['text']):
                    if ((term not in stop)and(not(re.match(reg, str(term))))):
                        t.append(term)
    pred = {}
    for term in terms:
        pr = {}
        for loc in l:
            pr[loc] = 0
            for t in term:
                if re.search(loc, t, re.IGNORECASE):
                    pr[loc] += 1
        loc = max(pr.items(), key = operator.itemgetter(1))[0]
        pred[str(term[0])] = str(loc)
    return pred

def getAccuracy(pred, a):
    count = 0
    for key, value in pred.items():
        if a[key] == value:
            count = count + 1
    print("Accuracy: " + str(count/len(pred)))
