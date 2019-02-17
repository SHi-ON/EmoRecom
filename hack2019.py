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

emo = {}
emo['sad']= "bar"
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
location="43.1361950,%20-70.9267410"
radius="10000"

try:
    u_in = input("")
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
sort_df.columns =['Name', 'Rating']
sort_df['been'] = rand.randint(1,5,size = len(sort_df))
maxi = pd.Series(data=[5.0]*len(sort_df))
sort_df['Rating'] = maxi.combine((sort_df['Rating']-(rand.randint(-10,10,size = len(sort_df))/10)), min)

 
print("Historical Experience in "+keyword)
print(sort_df.sort_values(by=['Rating'],ascending=False))


loc_dover = "43.1953080,%20-70.8743810"#&opennow
dover_url = google_nearby_Search+"location="+loc_dover+"&radius="+radius+"&keyword="+keyword+"&rankby="+rankby+"&key=AIzaSyAtTESyXpOa9WuicoLMGWpWkebGbIIBFfs"
with urllib.request.urlopen(dover_url) as url:
    data2 = json.loads(url.read().decode())





data2 = data2['results']
df2 = {}
for i in data2:
    try :
        df2[keyword][i['name']]=i['rating']

    except:
        df2[keyword]={}
        df2[keyword][i['name']]=i['rating']

sort_df2 = DF.from_dict(sorted(df2[keyword].items(), key=operator.itemgetter(1), reverse=True))
sort_df2.columns =['Name', 'Rating']
sort_df2['been'] = 0
print(keyword + " around you")
print(sort_df2)
been = []
rate = []
for i in range(len(sort_df2)):
    if sum(sort_df2.loc[i]['Name'] == sort_df['Name']):
        been.append(int(sort_df[sort_df2.loc[i]['Name'] == sort_df['Name']]['been']))
        rate.append(float(sort_df[sort_df2.loc[i]['Name'] == sort_df['Name']]['Rating']))
    else:
        been.append(0)
        rate.append(sort_df2.loc[i]['Rating'])
        
    
sort_df2['Rating'] = rate
sort_df2['been'] = been
print(keyword + " around you (personalize)")
print(sort_df2.sort_values(by=['Rating'],ascending=False))








