from DB import db
from QueryAPis import QueryApi

db = db()

# db.printAll()
db.deleteAll()

queryApi = QueryApi()
queryApi.getStream()
