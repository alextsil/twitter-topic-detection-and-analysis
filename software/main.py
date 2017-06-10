import DB
import GeoPrediction as gp
import QueryAPis

qa = QueryAPis.QueryApi()

db = DB.db()

geotagged = db.getGeotagged()

a = gp.dictGeoGenerator(geotagged)


#gp.printGeotaggedCities(a)


for key, value in a.items():
	qa.getUserTimeLine(key)