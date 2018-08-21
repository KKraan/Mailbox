# -*- coding: utf-8 -*-
"""
Created on Sun May 20 15:07:07 2018

@author: Kraan
"""
#IMPORT LIBRARIES
import pandas as pd
import numpy as np
from gensim.utils import tokenize
from nltk.corpus import stopwords
import time
import re
from collections import Counter
stopword = stopwords.words("dutch")

test=True
workingdir='C:\\Users\\Kraan\\OneDrive - KZA B.V\\Data-gilde\\KZAplanning\\'
textfilename=workingdir+'mailtekst.txt'
sourcefile=workingdir+'Mailgegevens.xlsx'

#DEFINE FUNCTIONS
def definenumber(textpart):
    """Based on "checklist" this function gives every item (in "textpart") a number coresponding with the position in the list.
    Input: a string
    Output: a number"""
    checklist=['Sent Items','Inhuurprotocollen','Niet aangeboden','Intakes','Contracten','Aangeboden']
    for i in range(len(checklist)):
        if checklist[i] in textpart:
            return i+1
    return 0

def readfiles(files):
    """function to get text out of a list of files.
    Input: a list of files
    Output: a string with the text"""
    text=''
    for file in files:
        text+=open(file,'r',encoding='utf-8',errors='ignore').read()
    return(text)

def ReplaceTokens(tekst):
    """Function which uses regex to remove urls, mailadress, telefoonnummer and special tokens.
    Input: string
    Output: string with less tokens"""
    tekst = re.sub(r'http\S+', '', tekst) #webadres
    tekst = re.sub(r'[0-9\s]{10,15}|\(\+[0-9]{2}\)[0-9\s]{9,12}','',tekst) #telefoonnummer
    tekst = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+', '', re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+', '', tekst))
    tekst = re.sub(r'[-\'`~!@#$%^&*()_|+=?;:\'",.<>\{\}\[\]\\\/]', ' ', tekst)
    return re.sub(r'\s+', ' ', tekst)

def xtremwords(wordlist,min_v,max_v):
    """This function returns a list of words with more than "max_v" occurences or less than "min_v" occurences.
    Input: list of words, minimum occurences and maximum occurences
    Ouput: list of "extreme" words."""
    smallwords=Counter(wordlist)
    return(list([k for k,v in smallwords.items() if (v < min_v or v > max_v)]))

def removewords(inputtext,stopword,min_v=2,max_v=999999):
    """This function removes stopwords, words with minimum or maximum occurences and word with one letter.
    Input: string of text, list of stopwords, minimum and maximum value.
    Output: the text, in the form of a list of words, without certain words."""
    wordlist=inputtext.lower()
    wordlist=list(tokenize(wordlist,deacc=True)) #cut words out of string
    smallwords=xtremwords(wordlist,min_v=min_v,max_v=max_v)
    stopword.extend(list(smallwords)) #combine stopwords and smallwords
    stopword=set(tuple(stopword)) #Way to speed up the process
    combilist=[[i, j] for i, j in zip(wordlist, list(map(len, map(str, wordlist))))] #smart way to calculate lenght of words
    return([word[0] for word in combilist if (word[1]>1 and word[0] not in stopword)])

def writetext(filename,inputmatrix):
    """This function takes an inputmatrix of length n and dimension 1 and puts this into the given file.
    If a file exists, it will be deleted. If more dimensions are given, the first will be used.
    Input: name of the file, a matrix to put into the file
    Output: a file with the information stored in the matrix."""
    f=open(filename,'w',encoding='utf-8',errors='ignore')
    for i in range(len(inputmatrix)):
        temp=inputmatrix[i,0]
        if type(temp)==float and temp != temp:
            templist=[]
        else:
            f.write(temp+'\n')
    f.close()

#read data
dfxls=pd.read_excel(sourcefile,encoding='utf-8',errors='ignore')

#create indicator for in or outgoing mail
dfxls['Inkomend']=(dfxls['afzendernaam']!='KZA Planning') #als de afzender "KZA planning" is komt hier dus "FALSE"
dfxls['status']=(definenumber(dfxls['Map']))

#select relevant columns
dfxls=dfxls[['Inkomend','status','afzendernaam','Ontvanger','verzenddatum','Onderwerp','tekst']]

#write textdump
nptext=dfxls.as_matrix(['tekst'])
tm=time.time()
writetext(filename=textfilename,inputmatrix=nptext)
print(time.time()-tm)





mailtext=readfiles([textfilename])
mailtext=mailtext.replace('\n',' ')
mailtext=ReplaceTokens(mailtext)
mailwords=removewords(inputtext=mailtext,min_v=10,max_v=25000,stopword=stopword)

print(len(mailwords)) #aantal woorden
print(len(list(set(mailwords)))) #aantal unieke woorden
