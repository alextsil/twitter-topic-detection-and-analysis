import string

from nltk import re, Counter
from nltk.corpus import stopwords

from DB import db


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    return tokens


count = 0
db = db()

# text = "RT @Scavino45: President Trump pays respects and  delivers #MemorialDay " \
#        "remarks at Arlington National Cemetery. https://t.co/D5rl948J6u"
#
regex_str = [
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]
tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
print("Token compilation completed")

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']
print("Stopword list construction completed")

allTweets = db.getAll()

count_all = Counter()
for tweet in allTweets:
    tweetText = tweet['text'].lower()
    # Create a list with all the terms
    terms_stop = [term for term in preprocess(tweetText) if term not in stop]
    # Update the counter
    count_all.update(terms_stop)
    count += 1
    print("\rLoop run " + str(count) + " times", end="")

# Print the first 30 most frequent words
print(count_all.most_common(30))
