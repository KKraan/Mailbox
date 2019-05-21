from mimp import readdata

import re
from nltk.corpus import stopwords as sw
from nltk.tokenize import word_tokenize
from collections import Counter
import csv
import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from gensim.models import KeyedVectors
from sklearn.cluster import KMeans
import numpy as np
import pickle

nr_clusters = 50
clusterfile = './result/result.csv'
sentsfile = './result/sents.pickle'
cloudfig = './img/wc.png'
model = './model/word2vec_mail.model'
srcxlsx = './src/Mailgegevens.xlsx'
xtra_stopwords = './src/added_stopwords.txt'


def find_vec_size(model):
    for item in model.vocab:
        return len(model[item])


def get_data(source):
    df = readdata(sourcefile=source)
    # dataframe met alleen de verzonden mails
    df = df[df.status == 1]
    df = df.groupby(['conversationID'])['tekst'].first()
    return df.tolist()
    #Test Martijn om tweede tekst terug te krijgen ipv de eerste
    #Maakt een lijst van de group by op converstationID en koppelt de 2e tekst aan het conversationId  .nth(0) = .first()
    #dfxlstext = dfxls.groupby(['conversationID'])['tekst'].nth(1)


def input_stopwords(stopfile):
    f = open(stopfile, "r")
    addition = f.read().split('\n')
    f.close()
    result = sw.words('dutch')
    result.extend(sw.words('english'))
    result.extend(addition[:len(addition) - 1])
    pattern = re.compile(r'\b(' + r'|'.join(result) + r')\b\s*')
    return pattern


def cleantext(text):
    text = str(text).lower()                                            # Alle tekst in kleine letters
    text = text.translate(str.maketrans('', '', string.punctuation))    # Vervang meeste leestekens
    text = text.replace('•', '').replace('’', '')                       # Vervang rest van leestekens
    text = re.sub('\d+', '', text)                                      # Vervang alle getallen
    text = text.split('Disclaimer', 1)[0]                               # Vervang alles na het woord disclaimer
    text = re.sub(r'\w*http\w*', '', text)                              # Vervang alle woorden die http bevatten
    text = re.sub(r'\w*brainnet\w*', '', text)                          # Vervang alle woorden die brainnet bevatten
    text = stoppattern.sub('', text)                                    # Vervang alles uit de stopwoorden lijst
    return(text)


def process_text(tekst):
    allwords = []
    allsents = []
    for text in tekst:
        if (text != None):
            allsents.append(cleantext(text))
            allwords.extend(word_tokenize(cleantext(text)))
    return Counter(allwords),allsents


def create_vecgram(input,model,size):
    first = True
    for key, value in input:
        if first is True:
            if key in model.vocab:
                x = np.array([model[key]])
            else:
                x = np.array(np.zeros(size))
            first = False
        else:
            if key in model.vocab:
                x = np.append(x, [model[key]], axis=0)
            else:
                x = np.append(x, [np.zeros(size)], axis=0)
    return x


def k_cluster(input):
    kmeans = KMeans(n_clusters=nr_clusters)
    return kmeans.fit(input)


def add_to_list(list,addition):
    result = []
    for i in range(len(list)):
        result.append([list[i][0], list[i][1], addition.labels_[i]])
    return result


def save_result(filename,list):
    with open(filename, "w", newline='', errors='ignore') as file:
        writer = csv.writer(file)
        writer.writerows(list)


#Woordkleur wordcloud in KZA kleuren
def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    h = int(float(random_state.randint(240, 320)))
    s = int(100.0 )
    l = int(50.0)

    return "hsl({}, {}%, {}%)".format(h, s, l)


#genereer een wordcloud
def generate_wordcloud(text,figure):
    wc = WordCloud(background_color="white", max_words=30)
    # generate word cloud
    wc.generate_from_frequencies(text)
    plt.imshow(wc.recolor(color_func=random_color_func, random_state=3), interpolation="bilinear")

    plt.axis("off")
    plt.savefig(figure, format="png")
    plt.show()


print('start model')
w2v_model = KeyedVectors.load(model)
vec_size = find_vec_size(w2v_model)
print('load data')
tekst = get_data(source=srcxlsx)
stoppattern = input_stopwords(xtra_stopwords)
print('clean text')
wordcount,sents = process_text(tekst)
with open(sentsfile, 'wb') as f:
    pickle.dump(sents, f)
print('create matrix')
inputlist = wordcount.most_common()
vecgram = create_vecgram(inputlist,w2v_model,vec_size)
print('create clustering')
cluster = k_cluster(vecgram)
newinfo = add_to_list(inputlist,cluster)
print(wordcount.most_common(50))
print('save results')
save_result(clusterfile,newinfo)

print('create cloud')
generate_wordcloud(wordcount,cloudfig)

