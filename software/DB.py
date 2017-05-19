import pymongo

client = pymongo.MongoClient("mongodb://")
db = client['twitter']  # whole db
tweets = db.tweets  # group


class db:
    def getAll(self):
        return tweets.find()

    def printAll(self):
        results = tweets.find()
        for doc in results:
            print(doc)

    def insertOneDummy(self):
        post_data = {
            'title': 'Python and MongoDB',
            'content': 'PyMongo is fun, you guys',
            'author': 'Scott'
        }
        tweets.insert_one(post_data)

    def insertOne(self, tweetRawJson):
        tweets.insert_one(tweetRawJson)

    def deleteAll(self):
        result = tweets.delete_many({})  # no filter - deletes all documents
        print("Deleted " + str(result.deleted_count) + " document(s)")
