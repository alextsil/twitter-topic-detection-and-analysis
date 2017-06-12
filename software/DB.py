import datetime

import pymongo
from bson import ObjectId

uri = "mongodb://localhost:27017/twitter?authMechanism=SCRAM-SHA-1"
client = pymongo.MongoClient(uri)
db = client['twitter']
tweets = db.tweets  # group
latestTweets = db.latestTweets
userLoc = db.userLoc

class db:
    def getByDatetimeRange(self, datetimeCenter):
        # pernw 2 lepta pisw kai 2 mprosta apo to peak
        delta = 2
        start = datetimeCenter - datetime.timedelta(minutes=delta)
        end = datetimeCenter + datetime.timedelta(minutes=delta)
        # Querying db at {datetimeCenter} with {delta} minute deltas
        return tweets.find({'timestamp': {'$gte': start, '$lt': end}})

    def getAll(self):
        return latestTweets.find()

    def getOneSpecific(self, objId):
        return tweets.find_one({"_id": objId})

    def printAll(self):
        results = tweets.find()
        for doc in results:
            print(doc)

    def insertOneDummy(self, username, loc):
        post_data = {
            'screen_name': username,
            'Location': loc
        }
        userLoc.insert_one(post_data)
        print("Inserted, user: " + username + " ,location: " + loc)

    def insertOne(self, tweetRawJson):
        tweets.insert_one(tweetRawJson)

    def insertOneLatest(self, tweetRawJson):
        latestTweets.insert_one(tweetRawJson)
        
    def deleteAll(self):
        print("Attempting to delete all tweets from db")
        result = tweets.delete_many({})  # no filter - deletes all documents
        print("Deleted " + str(result.deleted_count) + " document(s)")

    def removeUnusedFields(self):
        res = latestTweets.update_many(
            {},
            {"$unset": {"user.contributors_enabled": 1, "user.listed_count": 1, "user.profile_image_url": 1,
                        "user.profile_background_image_url_https": 1, "user.profile_background_color": 1,
                        "user.profile_link_color": 1, "user.default_profile_image": 1, "user.follow_request_sent": 1,
                        "user.profile_background_tile": 1, "user.profile_sidebar_border_color": 1,
                        "user.profile_text_color": 1, "user.profile_background_image_url": 1,
                        "user.profile_use_background_image": 1, "user.notifications": 1,
                        "user.profile_sidebar_fill_color": 1, "user.profile_image_url_https": 1,
                        "extended_entities.media.sizes": 1, "extended_entities.media.indices": 1,
                        "retweeted_status.user.contributors_enabled": 1, "retweeted_status.user.listed_count": 1,
                        "retweeted_status.user.profile_image_url": 1,
                        "retweeted_status.user.profile_background_image_url_https": 1,
                        "retweeted_status.user.profile_background_color": 1,
                        "retweeted_status.user.profile_link_color": 1, "retweeted_status.user.default_profile_image": 1,
                        "retweeted_status.user.follow_request_sent": 1,
                        "retweeted_status.user.profile_background_tile": 1,
                        "retweeted_status.user.profile_sidebar_border_color": 1,
                        "retweeted_status.user.profile_text_color": 1,
                        "retweeted_status.user.profile_background_image_url": 1,
                        "retweeted_status.user.profile_use_background_image": 1,
                        "retweeted_status.user.notifications": 1,
                        "retweeted_status.user.profile_sidebar_fill_color": 1,
                        "retweeted_status.user.profile_image_url_https": 1,
                        "retweeted_status.extended_entities.media.sizes": 1,
                        "retweeted_status.extended_entities.media.indices": 1,
                        "retweeted_status.entities.media.sizes": 1, "retweeted_status.entities.media.sizes:": 1
                        }
             },
        )
        print("Update_many results ->")
        print("matched count: " + str(res.matched_count))
        print("modified count: " + str(res.modified_count))
        
    def deleteMany(self, tweet):
        latestTweets.delete_many({'user.screen_name' : tweet})
        print("End")
    
    def getGeotagged(self):
        return tweets.find({'$and':[{'user.protected': False}, {'$or':[{'place' : {'$not' : {'$type' : 10}}}, {"coordinates" : {'$not' : {'$type': 10}}}]}, {'lang':'en'}]})
	