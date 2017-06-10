import DB
import GeoPrediction as gp
import QueryAPis

qa = QueryAPis.QueryApi()

db = DB.db()

geotagged = db.getGeotagged()

a = gp.dictGeoGenerator(geotagged)

b = list(a)

qa.getUserTimeLine(str(b[0]))
qa.getUserTimeLine(str(b[1]))

#gp.printGeotaggedCities(a)

#for key in b:
#	qa.getUserTimeLine(str(key))