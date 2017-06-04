from nltk import Counter, bigrams

from DB import db
from Preprocessing import preprocess, stop

count = 0
db = db()

allTweets = db.getAll()

count_all_hashtags = Counter()
count_all_bigrams = Counter()
for tweet in allTweets:
    tweetText = tweet['text'].lower()
    # Bigrams list
    terms_stop = [term for term in preprocess(tweetText) if term not in stop]
    terms_bigram = bigrams(terms_stop)
    # Hashtags list
    terms_hash = [term for term in preprocess(tweetText)
                  if term.startswith('#')]

    # Update the counter(s)
    count_all_hashtags.update(terms_hash)
    count_all_bigrams.update(terms_bigram)

    count += 1
    print("\rLoop run " + str(count) + " times", end="")

# Print results
print(count_all_bigrams.most_common(75))
print(count_all_hashtags.most_common(75))
