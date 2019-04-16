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

allwords = []
pattern = re.compile(r'\b(' + r'|'.join(stopwords) + r')\b\s*')
for text in tekst:
    if(text != None):
        text = str(text).lower()                                            #Alle tekst in kleine letters
        text = pattern.sub('', text)
        text = text.translate(str.maketrans('', '', string.punctuation))    #Vervang meeste leestekens
        text = text.replace('•','').replace('’','')                         #Vervang rest van leestekens
        text = re.sub('\d+','',text)                                        #Vervang alle getallen
        text = text.split('Disclaimer', 1)[0]                               #Vervang alles na het woord disclaimer
        allwords.extend(word_tokenize(text.lower()))
wordcount = Counter(allwords)

dfwordcount = pd.DataFrame(wordcount.most_common(),columns=['Word','Aantal'])
dfwordcount["Aantal"] = pd.to_numeric(dfwordcount["Aantal"])
#dfwordcount = dfwordcount[(dfwordcount.Aantal < (dfxls.count() * 0.9)) & (dfwordcount.Aantal > (dfxls.count() * 0.1))]


dfwordcount.to_csv("results.csv",index=False, header=False)

dfxls.to_csv("text.csv",index=False, header=True)

#genereer een wordcloud
def generate_wordcloud(text):
    wc = WordCloud(background_color="white", max_words=50)
    # generate word cloud
    wc.generate_from_frequencies(text)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()

generate_wordcloud(wordcount)

