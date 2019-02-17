#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 20:24:16 2019

@author: monkiehau
"""
import operator
import pandas as pd
from pandas import DataFrame as DF
import json
import urllib.request
import numpy.random as rand
import numpy as np


def runsuggest(emotion,Lat_LNG):
    emo = {}
    emo['sad']= "bar"
    emo['disgust']= "bar"
    emo['scared']= "gym"
    emo['neutral']= "restaurant"
    emo['happy']= "gym"
    emo['angry']= "cinema"
    emo['surprised']= "store"
    
    
    
    '''
    keyword = input("")
    name = input("")
    location = input("")
    radius = input("")
    user_rating = input("")
    '''
    df={}
    
    google_nearby_Search = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    location = str(Lat_LNG['lat'])+",%20"+str(Lat_LNG['lng'])
    location="43.1361950,%20-70.9267410"
    radius="10000"
    
    try:
        
        u_in = emotion
        
    except:
        u_in ="happy"
        
    
    keyword=emo[u_in]
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
    sort_df = sort_df.sort_values(by=['rating'],ascending=False)
     
    print("Historical Experience in "+keyword)
    print(sort_df.sort_values(by=['rating'],ascending=False))
    
    sort_df.to_csv(keyword+'history.csv', index=False)
    
    
    loc_dover = "43.1953080,%20-70.8743810"#&opennow
    dover_url = google_nearby_Search+"location="+loc_dover+"&radius="+radius+"&keyword="+keyword+"&rankby="+rankby+"&key=AIzaSyAtTESyXpOa9WuicoLMGWpWkebGbIIBFfs"
    with urllib.request.urlopen(dover_url) as url:
        data2 = json.loads(url.read().decode())
    
    data2 = data2['results']
    json.dumps(data2)
    df2 = DF(data2)
    sort_df2 = df2[['name','rating']]

    lat =[]
    lng = []
    
    for i in data2: 
        lat.append(i['geometry']['location']['lat'])
        lng.append(i['geometry']['location']['lng'])
    
    sort_df2['Lat'] = lat
    sort_df2['Long'] = lng

    print(keyword + " around you")
    print(sort_df2)
    been = []
    rate = []
    for i in range(len(sort_df2)):
        if sum(sort_df2.loc[i]['name'] == sort_df['name']):
            been.append(int(sort_df[sort_df2.loc[i]['name'] == sort_df['name']]['been']))
            rate.append(float(sort_df[sort_df2.loc[i]['name'] == sort_df['name']]['rating']))
        else:
            been.append(0)
            rate.append(sort_df2.loc[i]['rating'])
            
        
    sort_df2['rating'] = rate
    sort_df2['been'] = been
    print(keyword + " around you (personali2ze)")
    print(sort_df2.sort_values(by=['rating'],ascending=False))
    sort_df2 = sort_df2.sort_values(by=['rating'],ascending=False)
    sort_df2 = sort_df2.iloc[0:5,:]

            
    
    
    return [sort_df2,sort_df2.to_json(orient='records'),sort_df]



#runsuggest("sad")

