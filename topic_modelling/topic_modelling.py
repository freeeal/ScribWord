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
        topic_labels = ['Spirituality','Life','Politics','America','Work','Religion','Art','Business','Ambiguous','Sports']
        topic_dict = {topic_labels[i]: self.topic_list[i] for i in range(len(topic_labels))}
        return topic_dict

    # test the topic model on a new string of text
    def test_lda(self, text):
        topic_dict = self.log_topics(self.lda_model, self.vectorizer)
        # print(topic_dict)
        text_vectorized = self.vectorizer.transform([text])
        topic_likelihoods = self.lda_model.transform(text_vectorized)[0]
        # print("LDA result: ", topic_likelihoods)
        topics_sorted = np.argsort(np.array(topic_likelihoods))[::-1]
        # print(topics_sorted.tolist())
        top_topics = [list(topic_dict.keys())[topic] for topic in topics_sorted.tolist() if topic_likelihoods[topic] >= 0.1]
        if len(top_topics) > 1 and 'Ambiguous' in top_topics:
            top_topics.remove('Ambiguous')
        # print(top_topics)
        # top_topic = np.argmax(np.array(topic_likelihoods))
        output_topics = [(topic, topic_dict[topic]) for topic in top_topics]
        # print(output,"\n")
        return output_topics, list(topic_dict.keys()), topic_likelihoods.tolist()


# print("LDA Model:")
# log_topics(lda_model, vectorizer)
# print("=" * 20)

# # TESTING
# sports_text = "I haven't played baseball in a long while. I used to play baseball for my sunday league with a small team, but I got injured."
# biz_text = "I want to start a business. I need to find low cost materials for my company to make a profit."
# gov_text = "The state government may have a new leading political party this election. The people need a new leader."

# texts = [sports_text, biz_text, gov_text]
