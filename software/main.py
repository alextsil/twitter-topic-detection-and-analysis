#import pandas
import DB
import GeoPrediction as gp
import QueryAPis
#from Preprocessing import stop, preprocess, regex_str
#import re
#from nltk.tokenize import TweetTokenizer


qa = QueryAPis.QueryApi()

db = DB.db()

#db.removeUnusedFields()

# Get geottaged tweets
geotagged = db.getGeotagged()

# Get a dict with username and location
a = gp.dictGeoGenerator(geotagged)

# Get for 20 most populated cities 30 unique users
d = gp.getUniqueUsersPerLoc(a)

#gp.printGeotaggedCities(a)

# Get 200 latest tweets of each user
for key in d:
	qa.getUserTimeLine(str(key))

# Get all tweets
#allTweets = db.getAll()

# List of lists with terms
#terms = []

# Keep hashtag's regex
#regex_str.pop(2)
#regex_str.pop(4)
#regex_str.pop(4)
#regex_str.pop(4)

# Make a combined regex of all regex-es
#reg = "(" + ")|(".join(regex_str) + ")"

#print(reg)

# Tokenization/(removing stopwords, urls, html, 
#for tweet in allTweets:
#	t = [term for term in preprocess(tweet['text']) if ((term not in stop)and(not(re.match(reg, str(term)))))]
#	t.append(tweet['user']['screen_name'])
#	terms.append(t)

#print(terms)