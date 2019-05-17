from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from mimp import readdata
import logging


dfxls = readdata(sourcefile='Mailgegevens.xlsx')
dfxls = dfxls.groupby(['conversationID'])['tekst'].first()
tekst = dfxls.tolist()


def read_input(input_file):
    """This method reads the input file which is in gzip format"""
    logging.info("reading file {0}...this may take a while".format(input_file))

    for i, line in enumerate(input_file):
        if (i % 10000 == 0):
            logging.info("read {0} reviews".format(i))
        # do some pre-processing and return list of words for each review
        # text
        if not (type(line) == float and line != line):
            yield simple_preprocess(line)


documents = list(read_input(tekst))

model = Word2Vec(documents, size=200, window=10, min_count=5, workers=10)

model.wv.save('word2vec_mail.model')
