# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 15:34:38 2018

@author: Simon
"""
import os
import sqlite3
import pandas as pd
import ast
import numpy as np

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from nltk.stem import WordNetLemmatizer
import re

files = os.listdir('./database_csv')

dataframes = []
for file in files:
    print("reading "+file)
    df = pd.read_csv('./database_csv/'+file, sep = ',', lineterminator='\n', header=0, encoding='latin-1')
    dataframes.append(df)


def clean_tweets(liste_df):
    df_tweets=pd.concat(liste_df)
    df_tweets=df_tweets.loc[df_tweets.place.notnull()]
    df_tweets.drop_duplicates(subset='tweet',inplace=True)
    df_tweets.reset_index(drop=True, inplace=True)
    df_tweets.drop(['location','user_location\r','langue'], axis=1, inplace=True)
    df_tweets['id']=df_tweets['id'].astype('int64')
    df_tweets.drop_duplicates(subset='tweet',inplace=True)
    df_tweets=df_tweets.join(df_tweets['place'].apply(ast.literal_eval).apply(pd.Series)['country'])
    return(df_tweets)
    
print("cleaning tweets")
dataframe = clean_tweets( dataframes )
print("tweets utiles : ",len(dataframe))

def pred_genre(dataframe):
    print("prediction des genres")
    print("reading names.csv")
    genders = pd.read_csv("./names/names.csv", sep = ',', header=0, encoding='latin-1')
    sizes = np.zeros(len(genders))
    names = pd.Series("",range(len(genders)))
    for i, row in genders.iterrows():
        sizes[i] = len(row['Name'])
        names[i] = row['Name'].lower()
    genders['Length'] = sizes
    genders['Name'] = names
    genders.sort_values(['Length'],ascending=False,inplace=True)
    
    dico = {}
    for i, row in genders.iterrows():
        dico[row['Name']]=row['prob.gender']
        
    male_titles = ['m', 'mr']
    female_titles = ['mrs', 'ms', 'miss', 'lady', 'mme', 'mlle']
    
    def pred_genre_2( username, dico, male_titles, female_titles):
        for t in male_titles:
            if( username.startswith(t+".") or username.startswith(t+" ")):
                return 'Male'
        for t in female_titles:
            if( username.startswith(t+".") or username.startswith(t+" ")):
                return 'Female'
        l1 = username.split(" ")
        mots = []
        for i in l1:
            l2 = i.split("-")
            mots += l2
        for mot in mots:
            try:
                genre = dico[mot]
                if( genre != 'Unknown'):
                    return genre
            except KeyError:
                pass
        return 'Unknown'
        
    print("prediction des genres")
    genres_predits = pd.Series(len(dataframe))
    for i, row in dataframe.iterrows() :
         genres_predits[i] = pred_genre_2(row['name'].lower(), dico, male_titles, female_titles)
    
    dataframe['gender_predicted'] = genres_predits
    print("prediction finie")
    return dataframe

dataframe = pred_genre(dataframe)


def analyse_sentiment(dataframe):
    print( "analyse des sentiments" )
    dataframe['text_lem'] = [''.join([WordNetLemmatizer().lemmatize(re.sub('[^A-Za-z]', ' ', line)) 
                                      for line in lists]).strip() for lists in dataframe['tweet']]       
    sid = SentimentIntensityAnalyzer()
    dataframe['sentiment_compound_polarity']=dataframe.text_lem.apply(lambda x:sid.polarity_scores(x)['compound'])
    dataframe['sentiment_neutral']=dataframe.text_lem.apply(lambda x:sid.polarity_scores(x)['neu'])
    dataframe['sentiment_negative']=dataframe.text_lem.apply(lambda x:sid.polarity_scores(x)['neg'])
    dataframe['sentiment_pos']=dataframe.text_lem.apply(lambda x:sid.polarity_scores(x)['pos'])
    dataframe['sentiment_type']=''
    dataframe.loc[dataframe.sentiment_compound_polarity>0,'sentiment_type']='POSITIVE'
    dataframe.loc[dataframe.sentiment_compound_polarity==0,'sentiment_type']='NEUTRAL'
    dataframe.loc[dataframe.sentiment_compound_polarity<0,'sentiment_type']='NEGATIVE'
    dataframe.drop(['sentiment_compound_polarity','sentiment_neutral', 
                    'sentiment_negative', 'sentiment_pos'], axis=1, inplace=True)
    print( "analyse finie" )
    return dataframe

dataframe = analyse_sentiment(dataframe)
dataframe.to_csv('webapp/data.csv', sep = ',', header=True, index=False)


"""
# lancer ensuite le script suivant dans "python manage.py shell" :

import pandas as pd
from datetime import datetime
from blog.models import *

dataframe = pd.read_csv('data.csv', sep = ',', lineterminator='\n', header=0, encoding='latin-1')
    
for i, x in dataframe.iterrows():
    x_date = datetime.strptime(x['created at'], '%a %b %d %H:%M:%S +0000 %Y')
    tw = Tweet(
            id=         x['id'],
            created_at= x_date,
            name=       x['name'],
            genre=      x['gender_predicted'], 
            place=      x['country'],
            sentiment=  x['sentiment_type\r'])
    tw.save()
    
print( "base de donnee complete." )

"""