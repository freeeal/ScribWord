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
        x = self.lda_model.transform(text_vectorized)[0]
        top_topic = np.argmax(np.array(x))
        return list(topic_dict.items())[top_topic]


# print("LDA Model:")
# log_topics(lda_model, vectorizer)
# print("=" * 20)

# # TESTING
# sports_text = "I haven't played baseball in a long while. I used to play baseball for my sunday league with a small team, but I got injured."
# biz_text = "I want to start a business. I need to find low cost materials for my company to make a profit."
# gov_text = "The state government may have a new leading political party this election. The people need a new leader."

# texts = [sports_text, biz_text, gov_text]

# text = "Chemical warfare in Syria do I need to see more."
text = "The proposal that you are making is completely new, vis-à-vis the conversations our two teams have been having. But I have gathered this from the position that you have taken in terms of trade. I think we have the route to continue having balanced trade between both nations. And frankly, to tell you the truth Mr. President, I feel quite surprised about this new proposal that you are making because it is different from the discussion that both of our teams have been holding. ÍEnrique, if I can interrupt – this is not a new proposal. This is what I have been saying for a year and a half on the campaign trail. I have been telling this to every group of 50,000 people or 25,000 people – because no one got people in their rallies as big as I did. But I have been saying I wanted to tax people that treated us unfairly at the border, and Mexico is treating us unfairly. Now, this is different from what Luis and Jared have been talking about. But this was not a new proposal – this is the old proposal. This was the proposal I wanted. But they say they can come up with some other idea, and that is fine if they want to try it out. But I got elected on this proposal – this won me the election, along with military and healthcare. So this is not a new proposal this is been here for a year and half."
out = TopicModelling().test_lda(text)
print("\n",out)