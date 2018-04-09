from nltk.corpus import brown

from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer

import pyLDAvis.sklearn

import numpy as np
 
NUM_TOPICS = 10
data = []
 
for fileid in brown.fileids():
    document = ' '.join(brown.words(fileid))
    data.append(document)
 
NO_DOCUMENTS = len(data)

vectorizer = CountVectorizer(min_df=5, max_df=0.9, 
                             stop_words='english', lowercase=True, 
                             token_pattern=r'[a-zA-Z\-][a-zA-Z\-]{2,}')
data_vectorized = vectorizer.fit_transform(data)

# LDA model
lda_model = LatentDirichletAllocation(n_components=NUM_TOPICS, max_iter=20, learning_method='online')
lda_z = lda_model.fit_transform(data_vectorized)

# store/print topics
topic_list = []
def print_topics(model, vectorizer, top_n=10):
    for idx, topic in enumerate(model.components_):
        topics = [(vectorizer.get_feature_names()[i], topic[i])
                        for i in topic.argsort()[:-top_n - 1:-1]]
        topic_list.append(topics)
        print("Topic %d:" % (idx))
        print(topics)

print("LDA Model:")
print_topics(lda_model, vectorizer)
print("=" * 20)

text = "I haven't played baseball in a long while. I used to play baseball for my sunday league with a small team, but I got injured."
print(text,"\n")
text_vectorized = vectorizer.transform([text])
print(text_vectorized)
print(text_vectorized.shape)
x = lda_model.transform(vectorizer.transform([text]))[0]
top_topic = np.argmax(np.array(x))
print("Top topic (#{}):".format(top_topic), topic_list[top_topic],"\n")
print(x, x.sum())

print(brown.categories())

# # visualize LDA results
# data_visualization = pyLDAvis.sklearn.prepare(lda_model, data_vectorized, vectorizer, mds='tsne')
# pyLDAvis.show(data_visualization)