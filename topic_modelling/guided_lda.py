import numpy as np

import guidedlda

from nltk.corpus import reuters


from sklearn.feature_extraction.text import CountVectorizer

X = guidedlda.datasets.load_data(guidedlda.datasets.NYT)
vocab = guidedlda.datasets.load_vocab(guidedlda.datasets.NYT)
word2id = dict((v, idx) for idx, v in enumerate(vocab))

print(X.shape)

print(X[0])

# vectorizer
vectorizer_fit_data = []
 
for fileid in reuters.fileids():
    document = ' '.join(reuters.words(fileid))
    vectorizer_fit_data.append(document)

vectorizer = CountVectorizer(min_df=5, max_df=0.9, 
                             stop_words='english', lowercase=True, 
                             token_pattern=r'[a-zA-Z\-][a-zA-Z\-]{2,}')

vectorized_v_Fit_data = vectorizer.fit_transform(vectorizer_fit_data)

# # without seeding
# model = guidedlda.GuidedLDA(n_topics=5,n_iter=100, random_state=7, refresh=20)
# model.fit(X)

# topic_word = model.topic_word_
# n_top_words = 8

# for i, topic_dist in enumerate(topic_word):
#     topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
#     print('Topic %d: %s' %(i, ' '.join(topic_words)))

# with seeding
seed_topic_list = [['game', 'team', 'win', 'player', 'season', 'second', 'victory'],
                   ['percent', 'company', 'market', 'price', 'sell', 'business', 'stock', 'share'],
                   ['music', 'write', 'art', 'book', 'world', 'film'],
                   ['political', 'government', 'leader', 'official', 'state', 'country', 'american', 'case', 'law', 'police', 'charge', 'officer', 'kill', 'arrest', 'lawyer']]

model = guidedlda.GuidedLDA(n_topics=5, n_iter=100, random_state=7, refresh=20)

seed_topics = {}
for t_id, st in enumerate(seed_topic_list):
    for word in st:
        seed_topics[word2id[word]] = t_id

model.fit(X, seed_topics=seed_topics, seed_confidence=0.15)

n_top_words = 10
topic_word = model.topic_word_
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))

print("="*20)

# testing
text = "I enjoy music. I like to play the piano. I also like reading about artists."
text_vectorized = vectorizer.transform([text])
print(text,"\n")
print(text_vectorized)
# doc_topic = model.transform(X)
doc_topic = model.fit_transform(text_vectorized)
print(doc_topic)
# for i in range(9):
#     # print("top topic: {} Document: {}".format(doc_topic[i].argmax(), ', '.join(np.array(vocab)[list(reversed(X[i,:].argsort()))[0:5]])))


# x = model.fit_transform(vectorizer.transform([text]))[0]
# print(x)