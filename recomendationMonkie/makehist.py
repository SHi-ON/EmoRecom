#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 02:19:44 2019
make history file
@author: monkiehau
"""
import operator
import pandas as pd
from pandas import DataFrame as DF
import json
import urllib.request
import numpy.random as rand
import numpy as np

emo = {}
emo['sad']= "bar"
emo['disgust']= "bar"
emo['scared']= "gym"
emo['neutral']= "restaurant"
emo['happy']= "gym"
emo['angry']= "cinema"
emo['surprised']= "store"

for i in emo:
    
    '''
    keyword = input("")
    name = input("")
    location = input("")
    radius = input("")
    user_rating = input("")
    '''
    df={}
    
    google_nearby_Search = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    location="43.1361950,%20-70.9267410"
    radius="10000"
    keyword=emo[i]
    opennow=True
    rankby="prominence"# distance#&opennow
    apiurl = google_nearby_Search+"location="+location+"&radius="+radius+"&keyword="+keyword+"&rankby="+rankby+"&key=AIzaSyAtTESyXpOa9WuicoLMGWpWkebGbIIBFfs"
    
    
    
    
    
    with urllib.request.urlopen(apiurl) as url:
        data = json.loads(url.read().decode())
    
    data = data['results']
    
    
    
    for i in data:
        try :
            df[keyword][i['name']]=i['rating']
        except:
            df[keyword]={}
            df[keyword][i['name']]=i['rating']
    
    
    sort_df = DF.from_dict(sorted(df[keyword].items(), key=operator.itemgetter(1), reverse=True))
    sort_df.columns =['name', 'rating']
    sort_df['been'] = rand.randint(1,5,size = len(sort_df))
    maxi = pd.Series(data=[5.0]*len(sort_df))
    mini = pd.Series(data=[0.0]*len(sort_df))
    sort_df['rating'] = mini.combine(maxi.combine((sort_df['rating']-(rand.randint(-10,10,size = len(sort_df))/10)), min),max)
    
     
    print("Historical Experience in "+keyword)
    print(sort_df.sort_values(by=['rating'],ascending=False))
    
    sort_df.to_csv(keyword+'history.csv', index=False)
    
