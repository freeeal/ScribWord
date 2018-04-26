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
    try:
        top_topic = TopicModelling().test_lda(text)
        print("{}: {}".format(top_topic[0],top_topic[1]), "\n")
    except Exception as ex:
        print (ex)


#start process
if __name__ == '__main__':
    main()
