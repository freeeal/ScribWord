## compute_input.py

import sys, json, os
from sklearn.externals import joblib
from topic_modelling import TopicModelling

# set working directory for compute_input.py script
os.chdir(os.path.dirname(os.path.realpath(__file__)))

NUM_TOPICS = 10
VECTORIZER_FILE = 'vectorize_on_brown.pkl'
LDA_FILE = 'lda_model.pkl'

#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def main():
    # print('blah')
    text = read_in()    # read in the transcribed speech
    # text = "Suppose you follow the NBA I'm actually a big basketball fan myself but I'm not a fan of any team in the league right now really why is that I didn't grow up playing basketball do you follow the NBA but I used to follow the NBA before I came to the US and surely I used to follow the lord when I was in school but right now"
    try:
        model_out = TopicModelling().test_lda(text)
        # print(model_out)
        datastring = ""
        for topic in model_out[0]:
            datastring += "Topic: {}; Keywords: {}; \n".format(topic[0], dict(topic[1]))
        datastring += "All topics: {}\nAll likelihoods: {}".format(model_out[1], model_out[2])
        print(datastring)
    except Exception as ex:
        print (ex)


#start process
if __name__ == '__main__':
    main()
