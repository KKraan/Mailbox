# -*- coding: utf-8 -*-
"""
Created on Sun May 20 15:07:07 2018

@author: Kraan
"""
import pandas as pd
import numpy as np
from gensim.utils import tokenize 
from nltk.corpus import stopwords
import time
import re
from collections import Counter

stopword = stopwords.words("dutch")

def definenumber(textpart):
    checklist=['Sent Items','Inhuurprotocollen','Niet aangeboden','Intakes','Contracten','Aangeboden']
    for i in range(len(checklist)):
        if checklist[i] in textpart:
            return i+1
    return 0

#read data
sourcefile='C:\\Users\\Kraan\\OneDrive - KZA B.V\\Data-gilde\\KZAplanning\\Mailgegevens.xlsx'
dfxls=pd.read_excel(sourcefile,encoding='utf-8',errors='ignore')

#create indicator for in or outgoing mail
dfxls['Inkomend']=(dfxls['afzendernaam']!='KZA Planning')
dfxls['status']=(definenumber(dfxls['Map']))

dfxls=dfxls[['Inkomend','status','afzendernaam','Ontvanger','Verzenddatum','Onderwerp','tekst']]

def readfiles(files):
    text=''
    for file in files:
        text+=open(file,'r',encoding='utf-8',errors='ignore').read()
    return(text)

def ReplaceTokens(tekst):
    """Remove urls and remove E-mailadressess with or without countrycode"""
    tekst = re.sub(r'http\S+', '', tekst) #webadres
    tekst = re.sub(r'[0-9\s]{10,15}|\(\+[0-9]{2}\)[0-9\s]{9,12}','',tekst) #telefoonnummer
    tekst = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+', '', re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+', '', tekst))
    tekst = re.sub(r'[-\'`~!@#$%^&*()_|+=?;:\'",.<>\{\}\[\]\\\/]', ' ', tekst)
    return re.sub(r'\s+', ' ', tekst)

def removewords(inputtext,stopword,min_v=2,max_v=999999):
    wordlist=inputtext.lower()
    wordlist=list(tokenize(wordlist,deacc=True))
    smallwords=Counter(wordlist)
    smallwords=list([k for k,v in smallwords.items() if (v < min_v or v > max_v)])
    
    stopword.extend(list(smallwords))
    stopword=set(tuple(stopword))
    
    combilist=[[i, j] for i, j in zip(wordlist, list(map(len, map(str, wordlist))))]

    return([word[0] for word in combilist if (word[1]>1 and word[0] not in stopword)])
    
nptext=dfxls.as_matrix(['tekst'])
tm=time.time()
file='C:\\Users\\Kraan\\OneDrive - KZA B.V\\Data-gilde\\KZAplanning\\mailtekst.txt'
f=open(file,'w',encoding='utf-8',errors='ignore')
for i in range(len(nptext)):
    temp=nptext[i,0]
    if type(temp)==float and temp != temp:
        templist=[]
    else:
        f.write(temp+'\n')
f.close()       
print(time.time()-tm)

mailtext=readfiles([file])
mailtext=mailtext.replace('\n',' ')
mailtext=ReplaceTokens(mailtext)
mailwords=removewords(inputtext=mailtext,min_v=10,max_v=25000,stopword=stopword)
print(len(mailwords))
print(len(list(set(mailwords))))



tm=time.time()    
wordlist=[]
fastwordlist=[]
for i in range(len(nptest)):
    temp=nptest[i,0]
    if type(temp)==float and temp != temp:
        templist=[]
    else:
        templist=list(tokenize(temp,deacc=True))
        templist=list(set(templist))
        templist=[word for word in templist if (word not in stopword and word not in fastwordlist)]
        wordlist.extend(templist)
        fastwordlist=set(wordlist)
print(time.time()-tm)

newtest=[]
for test in wordlist:
    newtest.append([test,0])

for i in range(len(nptext)):
    temp=nptext[i,0]
    if type(temp)==float and temp != temp:
        templist=[]
    else:
        for test in newtest:
            test[1]=temp.count(test[0])


import itertools
from collections import Counter

dfxls1 = dfxls.replace(np.nan, '', regex=True)

dftext=dfxls1['tekst']

dfxls1['stemmed_text_data'].replace('\n',' ',inplace=True)
dfxls1['stemmed_text_data'].replace('\r',' ',inplace=True)
dfxls1['tekst'].replace('[!"#%\'()*+,-./:;<=>?@\[\]^_`{|}~1234567890’”“′‘\\\]',' ',inplace=True,regex=True)
wordlist = filter(None, " ".join(list(set(list(itertools.chain(*dfxls1['tekst'].str.split(' ')))))).split(" "))
dfxls1['stemmed_text_data'] = [' '.join(filter(None,filter(lambda word: word not in stopword,line))) for line in dfxls1['tekst'].str.lower().str.split(' ')]



minimum_count = 5
maximum_count = 15000
str_frequencies = pd.DataFrame(list(Counter(filter(None,list(itertools.chain(*dfxls1['stemmed_text_data'].str.split(' '))))).items()),columns=['word','count'])
low_frequency_words = set(str_frequencies[str_frequencies['count'] < minimum_count]['word'])
high_frequency_words = set(str_frequencies[str_frequencies['count'] > maximum_count]['word'])
dfxls1['stemmed_text_data'] = [' '.join(filter(None,filter(lambda word: word not in low_frequency_words, line))) for line in dfxls1['stemmed_text_data'].str.split(' ')]
dfxls1['stemmed_text_data'] = [' '.join(filter(None,filter(lambda word: word not in high_frequency_words, line))) for line in dfxls1['stemmed_text_data'].str.split(' ')]
dfxls1['stemmed_text_data'] = [" ".join(stemmer.stemWords(re.sub('[!"#%\'()*+,-./:;<=>?@\[\]^_`{|}~1234567890’”“′‘\\\]',' ', next_text).split(' '))) for next_text in dfxls1['stemmed_text_data']]






