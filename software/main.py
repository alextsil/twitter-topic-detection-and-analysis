import pandas
import vincent
from nltk import Counter, bigrams

from DB import db
from Preprocessing import preprocess, stop

count = 0
db = db()

allTweets = db.getAll()

count_all_hashtags = Counter()
count_all_terms = Counter()
dates_hashtag = []
for tweet in allTweets:
    tweetText = tweet['text'].lower()
    # Bigrams list
    termsWithoutStopwords = [term for term in preprocess(tweetText) if term not in stop]
    # termsBigrams = bigrams(termsWithoutStopwords)

    # Hashtags list
    terms_hash = [term for term in preprocess(tweetText)
                  if term.startswith('#')]
    if '#marchfortruth' in terms_hash:
        dates_hashtag.append(tweet['created_at'])

    # Update the counter(s)
    count_all_terms.update(termsWithoutStopwords)
    count_all_hashtags.update(terms_hash)

    count += 1
    print("\rLive number of processed tweets: " + str(count), end="")

# a list of "1" to count the hashtags
ones = [1]*len(dates_hashtag)
# the index of the series
idx = pandas.DatetimeIndex(dates_hashtag)
# the actual series (at series of 1s for the moment)
ITAvWAL = pandas.Series(ones, index=idx)

# Resampling / bucketing
per_1_minute = ITAvWAL.resample('120Min', how='sum').fillna(0)

# all the data together
match_data = dict(marchfortruth=per_1_minute)
# we need a DataFrame, to accommodate multiple series
all_matches = pandas.DataFrame(data=match_data,
                               index=per_1_minute.index)
# Resampling as above
all_matches = all_matches.resample('120Min', how='sum').fillna(0)

# and now the plotting
time_chart = vincent.Line(all_matches[['marchfortruth']])
time_chart.axis_titles(x='Time', y='Hits')
time_chart.legend(title='Hashtags')
time_chart.to_json('time_chart.json')

# Print results
print(count_all_terms.most_common(75))
print(count_all_hashtags.most_common(75))
