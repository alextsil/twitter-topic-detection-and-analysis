import DB
import GeoPrediction as gp
import QueryAPis

qa = QueryAPis.QueryApi()

db = DB.db()

geotagged = db.getGeotagged()

a = gp.dictGeoGenerator(geotagged)

b = list(a)

#gp.printGeotaggedCities(a)

for key in b:
	qa.getUserTimeLine(str(key))