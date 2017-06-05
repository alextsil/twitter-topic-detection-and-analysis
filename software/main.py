import pandas

from DB import db
from Preprocessing import preprocess

count = 0
db = db()

allTweets = db.getAll()

hashtagDatetimes = []
for tweet in allTweets:
    # Hashtags list
    terms_hash = [term for term in preprocess(tweet['text'].lower())
                  if term.startswith('#')]
    if '#covfefe' in terms_hash:
        hashtagDatetimes.append(tweet['created_at'])
    # if count == 60000:
    #     break
    count += 1
    print("\rLive number of processed tweets: " + str(count), end="")

print("\n")
print("length of occurence array : " + str(len(hashtagDatetimes)))

# a list of "1" to count the hashtags
ones = [1] * len(hashtagDatetimes)
# the index of the series
idx = pandas.DatetimeIndex(hashtagDatetimes)
# the actual series (xronoi kai monades opou iparxei occurence)
tweetSeries = pandas.Series(ones, index=idx)

# Resampling / bucketing
tweetsResampled = tweetSeries.resample('5T').sum().fillna(0)
# Vriskei to peak ston xrono
dtCenter = tweetsResampled.sort_values(ascending=False).index[0]

idIndex = []
followersCount = []
for tweet in db.getByDatetimeRange(dtCenter):
    terms_hash = [term for term in preprocess(tweet['text'].lower())
                  if term.startswith('#')]
    if '#covfefe' in terms_hash:
        idIndex.append(tweet['_id'])
        followersCount.append(tweet.get('retweeted_status', {})
                              .get('user', {})
                              .get('followers_count', {}))
# Replace gaps with 0
for index, i in enumerate(followersCount):
    if not i:
        followersCount[index] = 0

idx2 = pandas.Index(idIndex)
finalSeries = pandas.Series(followersCount, index=idx2)
objIdMaxFollowers = finalSeries.sort_values(ascending=False,
                                            axis=0).index[0]

print(db.getOneSpecific(objIdMaxFollowers))

print("\n")
print("done")
