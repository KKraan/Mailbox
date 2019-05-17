# IMPORT LIBRARIES
from gensim.models import KeyedVectors

# load model
model = KeyedVectors.load("model/word2vec_mail.model", mmap='r')

# get similar terms
searchterm = 'agile'
model.wv.most_similar(searchterm)
