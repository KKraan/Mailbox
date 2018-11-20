# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 19:25:31 2018

@author: Kraan
"""

from mimp import readdata
from pandas import pd

dfxls=readdata()#read data

s1=dfxls.groupby(['conversationID'], sort=False)['Verzenddatum'].max() #get the date of the last mail in the conversation
s2=dfxls.groupby(['conversationID'], sort=False)['Verzenddatum'].min() #get date of first mail in conversation
s=pd.concat([s1.rename('max_date'), s2.rename('min_date')], axis=1) #add two dates together and change columnnames

dfxls_new=pd.merge(dfxls, s, left_on = 'conversationID', right_index=True, how = 'left') #add dates to original data

#create new column to identify first mail of outbound conversation
dfxls_new['first_mail']=(dfxls_new['Verzenddatum']==dfxls_new['min_date'])&(dfxls_new['Inkomend']==True)
