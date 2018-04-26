import numpy as np
import keras
from keras.datasets import reuters
from keras.models import load_model
from keras.preprocessing.text import Tokenizer, text_to_word_sequence

word_index = reuters.get_word_index(path="reuters_word_index.json")
VOCAB_SIZE = len(word_index)
tokenizer = Tokenizer(num_words=VOCAB_SIZE)

def get_index_sequence(text):
    words = text_to_word_sequence(text)
    word_indices = []
    for word in words:
        if word in word_index.keys():
            word_indices.append(word_index[word])
        else:
            print("'%s' not in training corpus; ignoring." %(word))
    return word_indices

model = load_model('nn_model.h5') # load model

# test model on input sentence
while True:
    text = input('Input a sentence to be evaluated, or Enter to quit: ')

    if len(text) == 0:
        break

    # format your input
    word_indices = get_index_sequence(text)
    input_matrix = tokenizer.sequences_to_matrix([word_indices], mode='binary')

    # predict topic for input
    pred = model.predict(input_matrix)
    print("topic dist: %s; %f%% confidence" %(pred, pred[0][np.argmax(pred)] * 100))

    # ...