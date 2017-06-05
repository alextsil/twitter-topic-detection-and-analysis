import pandas

from DB import db
from Preprocessing import preprocess

count = 0
appendCount = 0
db = db()

allTweets = db.getAll()

hashtagDatetimes = []
for tweet in allTweets:
    # Hashtags list
    terms_hash = [term for term in preprocess(tweet['text'].lower())
                  if term.startswith('#')]
    if '#parisagreement' in terms_hash:
        hashtagDatetimes.append(tweet['created_at'])

    count += 1
    print("\rLive number of processed tweets: " + str(count), end="")

print("\n")
print("length of occurence array : " + str(len(hashtagDatetimes)))

# a list of "1" to count the hashtags
ones = [1] * len(hashtagDatetimes)
# the index of the series
idx = pandas.DatetimeIndex(hashtagDatetimes)
# the actual series (at series of 1s for the moment)
tweetSeries = pandas.Series(ones, index=idx)

# Resampling / bucketing
tweetsResampled = tweetSeries.resample('5T').sum().fillna(0)

print("\n")
print("done")
