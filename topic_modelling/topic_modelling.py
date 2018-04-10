import numpy as np

from sklearn.externals import joblib
 
class TopicModelling:
    def __init__(self, n_topics=10, vectorizer_file='vectorize_on_brown.pkl', lda_file='lda_model.pkl'):
        self.n_topics = n_topics
        self.vectorizer = joblib.load('vectorize_on_brown.pkl')
        self.lda_model = joblib.load('lda_model.pkl')
        self.topic_list = []
        self.n_topics = n_topics

    # log topic lists to a list of topics
    def log_topics(self, model, vectorizer, top_n=10):
        for idx, topic in enumerate(model.components_):
            topics = [(vectorizer.get_feature_names()[i], topic[i])
                            for i in topic.argsort()[:-top_n - 1:-1]]
            self.topic_list.append(topics)
            # print("Topic %d:" % (idx))
            # print(topics)

    # test the topic model on a new string of text
    def test_lda(self, text):
        self.log_topics(self.lda_model, self.vectorizer)
        text_vectorized = self.vectorizer.transform([text])
        x = self.lda_model.transform(text_vectorized)[0]
        top_topic = np.argmax(np.array(x))
        return top_topic, self.topic_list[top_topic]


# print("LDA Model:")
# log_topics(lda_model, vectorizer)
# print("=" * 20)

# # TESTING
# sports_text = "I haven't played baseball in a long while. I used to play baseball for my sunday league with a small team, but I got injured."
# biz_text = "I want to start a business. I need to find low cost materials for my company to make a profit."
# gov_text = "The state government may have a new leading political party this election. The people need a new leader."

# texts = [sports_text, biz_text, gov_text]

# text = "Chemical warfare in Syria do I need to see more."
# out = TopicModelling().test_lda(text)
# print(out)