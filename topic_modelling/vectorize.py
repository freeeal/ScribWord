from nltk.corpus import brown

from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer

data = []

# add reuters words to list of reuters data
for fileid in brown.fileids():
    document = ' '.join(brown.words(fileid))
    data.append(document)

# create vectorizer
vectorizer = CountVectorizer(min_df=5, max_df=0.9, 
                             stop_words='english', lowercase=True, 
                             token_pattern=r'[a-zA-Z\-][a-zA-Z\-]{2,}')

vectorized_reuters_data = vectorizer.fit_transform(data)    # fit vectorizer to reuters corpus
joblib.dump(vectorizer, 'vectorize_on_brown.pkl')   # save vectorizer model for later use