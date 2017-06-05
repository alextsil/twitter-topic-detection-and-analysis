import DB

geo = {}

geotagged = DB.findGeottaged()

for doc in geotagged:
    geo[doc['_id']] = doc['place'];