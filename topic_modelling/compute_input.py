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
    #get our data as an array from read_in()
    text = read_in()
    # text = "Hello my name is Paul"
    # print(text)
    # text = "I haven't played baseball in a long while. I used to play baseball for my sunday league with a small team, but I got injured."
    try:
        top_topic = TopicModelling().test_lda(text)
        print("Top topic (#{}):".format(top_topic[0]), top_topic[1], "\n")
    except Exception as ex:
        print (ex)
        # import traceback; traceback.print_exc()


#start process
if __name__ == '__main__':
    main()
