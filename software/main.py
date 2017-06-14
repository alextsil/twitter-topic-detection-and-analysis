import DB
import GeoPrediction as gp
import QueryAPis

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

# Get predictions
pred = gp.getPredictions(allTweets, users)

# Get accuracy
gp.getAccuracy(pred, a)