import DB
import GeoPrediction as gp
import QueryAPis

qa = QueryAPis.QueryApi()

db = DB.db()

# Get geottaged tweets
geotagged = db.getGeotagged()

# Get a dict with username and location
a = gp.dictGeoGenerator(geotagged)

#gp.plotFrequentCities(a)

# Get for 15 most populated cities 15 unique users
#d = gp.getUniqueUsersPerLoc(a)

#gp.printGeotaggedCities(a)

# Get 200 latest tweets of each user
#for key in d:
#	qa.getUserTimeLine(str(key))

db.removeUnusedFields()

db.deleteMany('absolutgrace')
db.deleteMany('veganbongwater')
db.deleteMany('alexisvmoran')
db.deleteMany('JASON_PAYBACK')

# Get all tweets
allTweets = db.getAllLatest()

# Get all locations
users = db.getAllLoc()

# Get predictions
pred = gp.getPredictions(allTweets, users)

# Get accuracy
gp.getAccuracy(pred, a)