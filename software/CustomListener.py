import tweepy
from tweepy.streaming import StreamListener
from DB import db
from DataAccess import api

db = db()

count = 0
class MyStreamListener(StreamListener):
    def on_status(self, status):
        global count
        db.insertOne(status._json)
        count += 1
        print("\rInserted " + str(count) + " tweets in the db -> ", end="")

    def on_error(self, status_code):
        if status_code == 420:
            return print("420 error (rate limit)")

    def start (self):
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(track=['trump']) # to filter na bgei eksw kai na mpenei param
