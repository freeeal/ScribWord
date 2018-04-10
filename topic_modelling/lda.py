# from nltk.corpus import brown

from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD
# from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS

import pyLDAvis.sklearn

import numpy as np

from sklearn.externals import joblib
 
NUM_TOPICS = 10
VECTORIZER_FILE = 'vectorize_on_brown.pkl'
LDA_FILE = 'lda_model.pkl'
# stop_words = ENGLISH_STOP_WORDS.union(["said","like","new","did"])
# data = []
 
# for fileid in brown.fileids():
#     document = ' '.join(brown.words(fileid))
#     data.append(document)
 
# NO_DOCUMENTS = len(data)

# vectorizer = CountVectorizer(min_df=5, max_df=0.9, 
#                              stop_words='english', lowercase=True, 
#                              token_pattern=r'[a-zA-Z\-][a-zA-Z\-]{2,}')
# data_vectorized = vectorizer.fit_transform(data)
# joblib.dump(vectorizer, 'vectorize_on_brown.pkl')   # save vectorizer model for later use

# load saved vectorizer
# vectorizer = joblib.load('vectorize_on_brown.pkl')
# data_vectorized = vectorizer.fit_transform(data)

# # LDA model
# lda_model = LatentDirichletAllocation(n_components=NUM_TOPICS, max_iter=10, learning_method='online')
# lda_z = lda_model.fit_transform(data_vectorized)

# # save model
# joblib.dump(lda_model, 'lda_model.pkl')

# load saved model
# lda_model = joblib.load('lda_model.pkl')

def load_models(vectorize_file, lda_file):
    return (joblib.load('vectorize_on_brown.pkl'), joblib.load('lda_model.pkl'))

vectorizer, lda_model = load_models(VECTORIZER_FILE,LDA_FILE)

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

sports_text = "I haven't played baseball in a long while. I used to play baseball for my sunday league with a small team, but I got injured."
biz_text = "I want to start a business. I need to find low cost materials for my company to make a profit."
gov_text = "The state government may have a new leading political party this election. The people need a new leader."
# music_text = "I enjoy music. I like to play jazz piano. I also like reading about artists."

# texts = [sports_text, biz_text, gov_text, music_text]
texts = [sports_text, biz_text, gov_text]

def test_lda(text):
    print(text)
    text_vectorized = vectorizer.transform([text])
    # print(text_vectorized)
    # print(text_vectorized.shape)
    x = lda_model.transform(text_vectorized)[0]
    top_topic = np.argmax(np.array(x))
    print("Top topic (#{}):".format(top_topic), topic_list[top_topic])
    print(x, x.sum(), "\n")
    print("=" * 20)
    return

for text in texts:
    test_lda(text)
# print(brown.categories())

# # visualize LDA results
# data_visualization = pyLDAvis.sklearn.prepare(lda_model, data_vectorized, vectorizer, mds='tsne')
# pyLDAvis.show(data_visualization)