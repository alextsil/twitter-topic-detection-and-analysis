#import pandas
import DB
import GeoPrediction as gp
import QueryAPis

from Preprocessing import stop, preprocess, regex_str
import re
from collections import Counter
import operator
#from nltk.tokenize import TweetTokenizer


qa = QueryAPis.QueryApi()

db = DB.db()

# Get geottaged tweets
geotagged = db.getGeotagged()

# Get a dict with username and location
a = gp.dictGeoGenerator(geotagged)
	
# Get for 20 most populated cities 30 unique users
#d = gp.getUniqueUsersPerLoc(a)

#gp.printGeotaggedCities(a)

# Get 200 latest tweets of each user
#for key in d:
#	qa.getUserTimeLine(str(key))

#db.removeUnusedFields()

# Get all tweets
allTweets = db.getAllLatest()

# Get all locations
users = db.getAllLoc()

terms = []
l = []

for user in users:
	t = []
	t.append(str(user['screen_name']))
	t.append(str(user['Location']))
	terms.append(t)
	if user['Location'] not in l:
		l.append(user['Location'])

# Keep hashtag's regex
regex_str.pop(2)
regex_str.pop(3)
regex_str.pop(3)
regex_str.pop(3)
regex_str.pop(3)
regex_str.pop(3)

# Make a combined regex of all regex-es
reg = "(" + ")|(".join(regex_str) + ")"

#print(reg)

# Tokenization/(removing stopwords, urls, html, 
for tweet in allTweets:
	for t in terms:
		if t[0] == str(tweet['user']['screen_name']):
			for term in preprocess(tweet['text']):
				if ((term not in stop)and(not(re.match(reg, str(term))))):
					t.append(term)

pred = {}

#l = [loc.lower() for loc in l]

for term in terms:
	pr = {}
	for loc in l:
		pr[loc] = 0
		for t in term:
			if re.search(loc, t, re.IGNORECASE):
				pr[loc] += 1
	loc = max(pr.items(), key = operator.itemgetter(1))[0]
	pred[str(term[0])] = str(loc)

#print(terms)

#print(pred)

count = 0

for key, value in pred.items():
	if a[key] == value:
		count = count + 1

print("Accuracy: " + str(count/len(a)))

#********** Removes the users that didn't downloaded tweets **********#

#allUsers = db.getAllLoc()

#b = db.getDistinct()

#i = 0

#for key in allUsers:
#	c = str(key['screen_name'])
#	if c not in b:
#		i = i + 1
#		print(i)
#		db.deleteMany(str(key['screen_name']))