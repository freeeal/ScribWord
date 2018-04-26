import numpy as np
import keras
from keras.datasets import reuters
from keras.models import Model, Sequential
from keras.layers import Input, Dense, Dropout, Flatten, Activation, Embedding, Conv1D
from keras.preprocessing.text import Tokenizer, text_to_word_sequence

# getting training data from reuters dataset
(x_train, y_train), (x_test, y_test) = reuters.load_data(path="reuters.npz",
                                                         num_words=None,
                                                         skip_top=0,
                                                         maxlen=None,
                                                         test_split=0.2,
                                                         seed=113,
                                                         start_char=1,
                                                         oov_char=2,
                                                         index_from=3)

word_index = reuters.get_word_index(path="reuters_word_index.json")

# HELPER VARIABLES
VOCAB_SIZE = len(word_index)
NUM_CLASSES = np.max(y_train)+1
BATCH_SIZE = 8
EPOCHS = 4

# vectorize sequence data
print('Vectorizing sequence data...')
tokenizer = Tokenizer(num_words=VOCAB_SIZE)
# x_train = tokenizer.sequences_to_matrix(x_train, mode='binary')
# x_test = tokenizer.sequences_to_matrix(x_test, mode='binary')
print('x_train shape:', x_train.shape)
print('x_test shape:', x_test.shape)

# categorize classes for categorical cross entropy
print('Convert class vector to binary class matrix '
      '(for use with categorical_crossentropy)')
y_train = keras.utils.to_categorical(y_train, NUM_CLASSES)
y_test = keras.utils.to_categorical(y_test, NUM_CLASSES)
print('y_train shape:', y_train.shape)
print('y_test shape:', y_test.shape)

# build model
# inputs = Input(shape=(VOCAB_SIZE,))
# embedding = Embedding(input_dim=VOCAB_SIZE, output_dim=100, input_length=5)(inputs)
# flatten = Flatten()(embedding)
# pred = Dense(NUM_CLASSES, activation='softmax')(flatten)
# model = Model(inputs=inputs, outputs=pred)

print('Building model...')
model = Sequential()
model.add(Dense(512, input_shape=(1,)))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(NUM_CLASSES))
model.add(Activation('softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# eval
model.fit(x_train, y_train,
          batch_size=BATCH_SIZE,
          epochs=EPOCHS,
          verbose=1,
          validation_split=0.1)
score = model.evaluate(x_test, y_test,
                       batch_size=BATCH_SIZE, verbose=1)

print('Test score:', score[0])
print('Test accuracy:', score[1])

# save model
model.save('nn_model.h5')

# ..