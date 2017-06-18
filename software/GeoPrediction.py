from geopy.geocoders import Nominatim
from collections import Counter
from Preprocessing import stop, preprocess, regex_str
import re
import operator
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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
    #g = ['Manhattan', 'Washington', 'Los Angeles', 'Chicago', 'Toronto', 'Houston', 'Brooklyn', 'Boston', 'Philadelphia', 'Austin', 'San Francisco', 'Phoenix', 'Dallas', 'Denver', 'Portland']
    d = {}
    for r in g:
        i = 0
        for key, value in av.items():
            w = str(r)
            q = str(value)
            if ((i != 25)&(w == q)&(key not in d)):
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
            term.pop(1)
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

def plotFrequentCities(geo):
    g = Counter(geo.values()).most_common(36)
    x_labels = [val[0] for val in g]
    y_labels = [val[1] for val in g]
    f = plt.figure(figsize = (16, 6))
    ax = pd.Series(y_labels).plot(kind = 'bar')
    ax.set_xticklabels(x_labels)
    rects = ax.patches
    for rect, label in zip(rects, y_labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2, height + 1, label, ha='center', va='bottom')
    plt.bar(range(len(g)), [val[1] for val in g], align='center')
    plt.xticks(range(len(g)), [val[0] for val in g])
    plt.xticks(rotation = 70)
    f.show()

    g = [('Manhattan', 74), ('Washington', 67), ('Los Angeles', 66), ('Chicago', 54), ('Toronto', 32), ('Houston', 30), ('Brooklyn', 27), ('Boston', 26), ('Philadelphia', 26), ('Austin', 20), ('San Francisco', 18), ('Phoenix', 17), ('Dallas', 16), ('Denver', 16), ('Portland', 15), ('Paris', 14), ('Seattle', 13), ('San Antonio', 13), ('Columbus', 13), ('Pittsburgh', 11)]
    x_labels = [val[0] for val in g]
    y_labels = [val[1] for val in g]
    h = plt.figure(figsize = (12, 6))
    ax = pd.Series(y_labels).plot(kind = 'bar')
    ax.set_xticklabels(x_labels)
    rects = ax.patches
    for rect, label in zip(rects, y_labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2, height + 1, label, ha='center', va='bottom')
    plt.bar(range(len(g)), [val[1] for val in g], align='center')
    plt.xticks(range(len(g)), [val[0] for val in g])
    plt.xticks(rotation = 70)
    h.show()