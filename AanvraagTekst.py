from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from mimp import readdata
import logging

import re
from nltk.corpus import stopwords as sw
from nltk.tokenize import word_tokenize
from collections import Counter
import csv
import string
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from gensim.models import KeyedVectors
from sklearn.cluster import KMeans
import numpy as np

nr_clusters = 50
resultfile = 'result.csv'

print('start model')
w2v_model = KeyedVectors.load('word2vec_mail.model')
print(w2v_model.most_similar('agile'))
dfxls = readdata(sourcefile='Mailgegevens.xlsx')

#dataframe met alleen de verzonden mails
dfxls = dfxls[dfxls.status == 1]

dfxls = dfxls.groupby(['conversationID'])['tekst'].first()
tekst = dfxls.tolist()

#Test Martijn om tweede tekst terug te krijgen ipv de eerste

#Maakt een lijst van de group by op converstationID en koppelt de 2e tekst aan het conversationId  .nth(0) = .first()
#dfxlstext = dfxls.groupby(['conversationID'])['tekst'].nth(1)

xtra_stopwords = 'added_stopwords.txt'

f = open(xtra_stopwords, "r")
addition = f.read().split('\n')
f.close()

stopwords = sw.words('dutch')
stopwords.extend(sw.words('english'))
stopwords.extend(addition[:len(addition)-1])

print('clean text')

allwords = []
pattern = re.compile(r'\b(' + r'|'.join(stopwords) + r')\b\s*')
for text in tekst:
    if(text != None):
        text = str(text).lower()                                            #Alle tekst in kleine letters
        text = text.translate(str.maketrans('', '', string.punctuation))    #Vervang meeste leestekens
        text = text.replace('•','').replace('’','')                         #Vervang rest van leestekens
        text = re.sub('\d+','',text)                                        #Vervang alle getallen
        text = text.split('Disclaimer', 1)[0]                               #Vervang alles na het woord disclaimer
        text = re.sub(r'\w*http\w*', '', text)                              #Vervang alle woorden die http bevatten
        text = re.sub(r'\w*brainnet\w*', '', text)                          #Vervang alle woorden die brainnet bevatten
        text = pattern.sub('', text)                                        #Vervang alles uit de stopwoorden lijst
        allwords.extend(word_tokenize(text.lower()))
wordcount = Counter(allwords)

print('create matrix')
inputlist = wordcount.most_common()
first = True
for key, value in inputlist:
    if first is True:
        x = np.array([w2v_model[key]])
        first = False
    else:
        if key in w2v_model.vocab:
            x = np.append(x, [w2v_model[key]], axis=0)
        else:
            x = np.append(x, [np.zeros(200)], axis=0)

print('create clustering')
kmeans = KMeans(n_clusters=nr_clusters)
kmeans.fit(x)

newinfo = []
for i in range(len(x)):
    newinfo.append([inputlist[i][0], inputlist[i][1], kmeans.labels_[i]])

print(wordcount.most_common(50))

print('save results')
with open(resultfile, "w", newline='',errors='ignore') as file:
    writer = csv.writer(file)
    writer.writerows(newinfo)

print('continue')
dfwordcount = pd.DataFrame(wordcount.most_common(),columns=['Word','Aantal'])
dfwordcount["Aantal"] = pd.to_numeric(dfwordcount["Aantal"])
#dfwordcount = dfwordcount[(dfwordcount.Aantal < (dfxls.count() * 0.9)) & (dfwordcount.Aantal > (dfxls.count() * 0.1))]


dfwordcount.to_csv("results.csv",index=False, header=False)

dfxls.to_csv("text.csv",index=False, header=True)

#Woordkleur wordcloud in KZA kleuren
def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    h = int(float(random_state.randint(240, 320)))
    s = int(100.0 )
    l = int(50.0)

    return "hsl({}, {}%, {}%)".format(h, s, l)


#genereer een wordcloud
def generate_wordcloud(text):
    wc = WordCloud(background_color="white", max_words=30)
    # generate word cloud
    wc.generate_from_frequencies(text)
    plt.imshow(wc.recolor(color_func=random_color_func, random_state=3), interpolation="bilinear")

    plt.axis("off")
    plt.show()

generate_wordcloud(wordcount)

