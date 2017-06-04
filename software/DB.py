import pymongo
from bson import ObjectId

uri = "mongodb://ergasia:mongoergasia@localhost:27017/twitter?authMechanism=SCRAM-SHA-1"
client = pymongo.MongoClient(uri)
db = client['twitter']
tweets = db.tweets  # group


class db:
    def getAll(self):
        return tweets.find()

    def getOneSpecific(self):
        return tweets.find_oneop({"_id": ObjectId("592daabea3576d2fb580facf")})

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
        print("Attempting to delete all tweets from db")
        result = tweets.delete_many({})  # no filter - deletes all documents
        print("Deleted " + str(result.deleted_count) + " document(s)")

    def removeUnusedFields(self):
        res = tweets.update_many(
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