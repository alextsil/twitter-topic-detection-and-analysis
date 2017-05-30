import tweepy
import time
import json
import pymongo

# API connection
auth = tweepy.OAuthHandler('consumer_key', 'consumer_secret')
auth.set_access_token('access_token', 'access_token_secret')
api = tweepy.API(auth)
api.retry_count = 5
api.retry_delay = 5
api.timeout = 5
api.wait_on_rate_limit = True
api.wait_on_rate_limit_notify = True

class MyStreamListener(tweepy.StreamListener):

    def __init__(self, time_limit = ):
        self.start_time = time.time()
        self.limit = time_limit
        # database connection for deletion of all records before the new stream starts(optional)
        client = pymongo.MongoClient('mongodb://localhost/twitterdb')
        db = client.twitterdb
        db.tweets.delete_many({})
        super(MyStreamListener, self).__init__()

    def on_data(self, data):
        try:
            # checks if the time interval passed
            if (time.time() - self.start_time) < self.limit:
                client = pymongo.MongoClient('mongodb://localhost/twitterdb')
                db = client.twitterdb
                datajson = json.loads(data)
                # data insertion to the database
                db.twitter_search.insert(datajson)
                return True
            else:
                # if the time interval passed the stream stops and disconnect
                return False
        except Exception as e:
            print(e)

myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener(time_limit = ))
# put what you want as a filter
myStream.filter(track=['Barcelona','Alaves'])