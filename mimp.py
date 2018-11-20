# -*- coding: utf-8 -*-
"""This file contains functions to import and clean the data. The functions can be called independently or you can use the function "getcleantext" to get the whole process.
This function gives 3 variables: the dataframe, the raw text and the clean text.
@author: Kraan
"""

import pandas as pd
import os

mypath = os.path.realpath(__file__)
mypath = mypath[:mypath.find('mimp.py')]

Maildata=mypath+'Mailgegevens.xlsx'
textfilename=mypath+'mailtekst.txt'

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

def readdata(sourcefile=Maildata):
    #read data
    dfxls=pd.read_excel(sourcefile,encoding='utf-8',errors='ignore')

    #create indicator for in or outgoing mail
    dfxls['Inkomend']=(dfxls['afzendernaam']!='KZA Planning') #als de afzender "KZA planning" is komt hier dus "FALSE"
    #dfxls['status']=(definenumber(dfxls['Map']))
    status=[definenumber(row) for row in dfxls['Map']]
    dfxls['status']=status

    #select relevant columns
    dfxls=dfxls[['Inkomend','status','afzendernaam','Ontvanger','Verzenddatum','Onderwerp','tekst','conversationID']]

    #little bit of cleaning
    dfxls['tekst'] = dfxls['tekst'].replace({'\n':' '}, regex=True).replace({'\r':' '}, regex=True).replace({'#':' '}, regex=True)
    dfxls['tekst'] = dfxls['tekst'].replace({' +':' '}, regex=True)
    dfxls['tekst'] = dfxls['tekst'].replace({'ë':'e'}, regex=True).replace({'è':'e'}, regex=True).replace({'é':'e'}, regex=True).replace({'ü':'u'}, regex=True).replace({'ó':'o'}, regex=True).replace({'ö':'o'}, regex=True).replace({'ï':'i'}, regex=True)
    dfxls['ID']=dfxls.index #add ID

    return(dfxls)
