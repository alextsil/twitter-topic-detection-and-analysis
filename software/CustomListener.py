import tweepy
from tweepy.streaming import StreamListener

from DataAccess import api


class MyStreamListener(StreamListener):
    def on_status(self, status):
        # TODO : na ta kane save sth vash
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return print("420 error (rate limit)")

    def start (self):
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(track=['java'])
