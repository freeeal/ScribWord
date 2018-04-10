import numpy as np

import guidedlda

# from nltk.corpus import reuters

from sklearn.externals import joblib

X = guidedlda.datasets.load_data(guidedlda.datasets.NYT)
vocab = guidedlda.datasets.load_vocab(guidedlda.datasets.NYT)
word2id = dict((v, idx) for idx, v in enumerate(vocab))

# # generate model without seeding
# model = guidedlda.GuidedLDA(n_topics=5,n_iter=100, random_state=7, refresh=20)
# model.fit(X)

# topic_word = model.topic_word_
# n_top_words = 8

# for i, topic_dist in enumerate(topic_word):
#     topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
#     print('Topic %d: %s' %(i, ' '.join(topic_words)))

# generate model with seeding
seed_topic_list = [['game', 'team', 'win', 'player', 'season', 'second', 'victory'],
                   ['percent', 'company', 'market', 'price', 'sell', 'business', 'stock', 'share'],
                   ['music', 'write', 'art', 'book', 'world', 'film'],
                   ['political', 'government', 'leader', 'official', 'state', 'country', 'american', 'case', 'law', 'police', 'charge', 'officer', 'kill', 'arrest', 'lawyer']]

model = guidedlda.GuidedLDA(n_topics=5, n_iter=100, random_state=7, refresh=20)

seed_topics = {}
for t_id, st in enumerate(seed_topic_list):
    for word in st:
        seed_topics[word2id[word]] = t_id

model.fit(X, seed_topics=seed_topics, seed_confidence=0.85)

# save model
joblib.dump(model, 'guidedlda_model.pkl')

#load model
guidedlda_model = joblib.load('guidedlda_model.pkl')

#get top 10 words of each topic
n_top_words = 5
topic_words_list = []
topic_word = guidedlda_model.topic_word_
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
    topic_words_list.append([' '.join(topic_words)])
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))

print("="*20)

# testing
text = "I enjoy music. I like to play the piano. I also like reading about artists."
v_model = joblib.load('vectorizer.pkl')
# text_vectorized = vectorizer.transform([text])
text_vectorized = v_model.transform([text])
print(text,"\n")
# print(text_vectorized)
# doc_topic = model.transform(X)
doc_topic = guidedlda_model.fit_transform(text_vectorized)
top_topic_ind = np.argmax(np.array(doc_topic[0]))
print('Topic {} keywords: {}'.format(top_topic_ind, topic_words_list[top_topic_ind][0]))
