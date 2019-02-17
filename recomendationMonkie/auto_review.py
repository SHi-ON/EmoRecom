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

def autorev(keyword,rate_in,name):
    
    emo = {}
    emo['sad']= "bar"
    emo['neutral']= "restaurant"
    emo['happy']= "gym"
    emo['angry']= "cinema"
    emo['surprised']= "store"
    
    df={}
    
    google_nearby_Search = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    location="43.1361950,%20-70.9267410"
    radius="10000"
    #keyword=input("")
    opennow=True
    rankby="prominence"# distance#&opennow
    apiurl = google_nearby_Search+"location="+location+"&radius="+radius+"&keyword="+keyword+"&rankby="+rankby+"&key=AIzaSyAtTESyXpOa9WuicoLMGWpWkebGbIIBFfs"
    '''
    try:
        rate_in = input("")
    except:
        rate_in = 3
    
    
    name = input("")
    '''
    sort_df = pd.read_csv(keyword+'history.csv')
    
     
    print("Old Rating of "+name)
    print(sort_df.sort_values(by=['rating'],ascending=False))
    
    new_rating = (float(sort_df[sort_df['name']==name]['rating']) * float(sort_df[sort_df['name']==name]['been']) + rate_in)/(float(sort_df[sort_df['name']==name]['been'])+1)
    new_rating = int(new_rating*10)/10
    
    ratechange = list(sort_df['rating'])
    ratechange[(sort_df[sort_df['name']==name].index)[0]] = new_rating
    
    sort_df['rating'] = ratechange
    been = sort_df['been'] + (sort_df['name'] == name)
    sort_df['been'] = been
    
    sort_df.to_csv(keyword+'history.csv', index=False)
    
    
    return sort_df


#autorev("gym",5,"Hamel Student Recreation Center")
