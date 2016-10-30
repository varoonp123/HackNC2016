#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 14:45:51 2016

@author: Varoon
"""


"""
GOAL: given query, mine geocoded tweets related to the query, classify them as positive or negative, export json file with states and num_positive and num_negative tweets
"""
from twython import Twython
from geopy.geocoders import Nominatim
import time
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.metrics import precision_recall_curve, auc
from sklearn.model_selection import ShuffleSplit
from sklearn.base import BaseEstimator
import numpy as np
import csv, collections, nltk
from sklearn import neighbors
from sklearn.externals import joblib
from classifying_tweets import LinguisticVectorizer
import sys


#Import pretrained classifier. Trained in classifying_tweets.py

print 'reading classifier'
a=joblib.load(open('tfidf_linguistic_tweet_MultinomialNB_classifier.pkl','rb'))
print 'read classifier'

#Establish connection to twitter API. 
consumer_key='TpCYKB3NtWrkiRdVUUNmHx82h'
consumer_secret='jd5zqkdtjsu1uZHBUCwjBplTkrn3otYB7k54ljmDJ8VyQQoYXX'
access_token='791825707156594688-WDa6SKm0ihheIJKp5lKaISO30oLDPw7'
access_token_secret='cw09NaXRry3RdX0s3nssGp86y8ISr4gwKUoCYAHIdaIis'

twitter = Twython(consumer_key, consumer_secret, oauth_version = 2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(consumer_key, access_token=ACCESS_TOKEN)

#Establish Geocoder
geocoder = Nominatim()
STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
json_result = [None]*50

#Load geographic centers of each state
geo_centers_dict = [{"State": "Alabama","Lat":32.806671, "Long":-86.79113},{"State": "Alaska","Lat":61.370716, "Long":-152.404419},{"State": "Arizona","Lat":33.729759, "Long":-111.431221},{"State": "Arkansas","Lat":34.969704, "Long":-92.373123},{"State": "California","Lat":36.116203, "Long":-119.681564},{"State": "Colorado","Lat":39.059811, "Long":-105.311104},{"State": "Connecticut","Lat":41.597782, "Long":-72.755371},{"State": "Delaware","Lat":39.318523, "Long":-75.507141},{"State": "District of Columbia","Lat":38.897438, "Long":-77.026817},{"State": "Florida","Lat":27.766279, "Long":-81.686783},{"State": "Georgia","Lat":33.040619, "Long":-83.643074},{"State": "Hawaii","Lat":21.094318, "Long":-157.498337},{"State": "Idaho","Lat":44.240459, "Long":-114.478828},{"State": "Illinois","Lat":40.349457, "Long":-88.986137},{"State": "Indiana","Lat":39.849426, "Long":-86.258278},{"State": "Iowa","Lat":42.011539, "Long":-93.210526},{"State": "Kansas","Lat":38.5266, "Long":-96.726486},{"State": "Kentucky","Lat":37.66814, "Long":-84.670067},{"State": "Louisiana","Lat":31.169546, "Long":-91.867805},{"State": "Maine","Lat":44.693947, "Long":-69.381927},{"State": "Maryland","Lat":39.063946, "Long":-76.802101},{"State": "Massachusetts","Lat":42.230171, "Long":-71.530106},{"State": "Michigan","Lat":43.326618, "Long":-84.536095},{"State": "Minnesota","Lat":45.694454, "Long":-93.900192},{"State": "Mississippi","Lat":32.741646, "Long":-89.678696},{"State": "Missouri","Lat":38.456085, "Long":-92.288368},{"State": "Montana","Lat":46.921925, "Long":-110.454353},{"State": "Nebraska","Lat":41.12537, "Long":-98.268082},{"State": "Nevada","Lat":38.313515, "Long":-117.055374},{"State": "New Hampshire","Lat":43.452492, "Long":-71.563896},{"State": "New Jersey","Lat":40.298904, "Long":-74.521011},{"State": "New Mexico","Lat":34.840515, "Long":-106.248482},{"State": "New York","Lat":42.165726, "Long":-74.948051},{"State": "North Carolina","Lat":35.630066, "Long":-79.806419},{"State": "North Dakota","Lat":47.528912, "Long":-99.784012},{"State": "Ohio","Lat":40.388783, "Long":-82.764915},{"State": "Oklahoma","Lat":35.565342, "Long":-96.928917},{"State": "Oregon","Lat":44.572021, "Long":-122.070938},{"State": "Pennsylvania","Lat":40.590752, "Long":-77.209755},{"State": "Rhode Island","Lat":41.680893, "Long":-71.51178},{"State": "South Carolina","Lat":33.856892, "Long":-80.945007},{"State": "South Dakota","Lat":44.299782, "Long":-99.438828},{"State": "Tennessee","Lat":35.747845, "Long":-86.692345},{"State": "Texas","Lat":31.054487, "Long":-97.563461},{"State": "Utah","Lat":40.150032, "Long":-111.862434},{"State": "Vermont","Lat":44.045876, "Long":-72.710686},{"State": "Virginia","Lat":37.769337, "Long":-78.169968},{"State": "Washington","Lat":47.400902, "Long":-121.490494},{"State": "West Virginia","Lat":38.491226, "Long":-80.954453},{"State": "Wisconsin","Lat":44.268543, "Long":-89.616508},{"State": "Wyoming","Lat":42.755966, "Long":-107.30249}]
#Instantiating JSON format
for i in range(0,50):
    print i
    json_result[i] = {"State Name":STATES[i],"Num_Positive_Tweets":0, "Num_Negative_Tweets":0 }
QUERY = "microsoft"



#radius with almost all of the US. Close to getting all geotagged tweets for analysis 

for dict in range(0,len(geo_centers_dict)):
    tweet_text = []
    tweets=[]
    classifications=[]
    count=0
    results= twitter.search(q=QUERY,count=3,geocode ="%f,%f,100mi"%(geo_centers_dict[dict]['Lat'],geo_centers_dict[dict]['Long']), result_type='recent' )
    tweets = results['statuses']
    
    for tweet in tweets:
        
        tweets[count] = tweet
        count+=1

        
        #sleep right before hitting rate limit of twitter API. Sleep for 15 minutes
        if count%179==0:
            print 'sleeping'
            for i in range(0,len(tweets)):
                classifications[i] = a.predict(tweets[i]['text'])
                
                #try to set state given output of reverse geocode. Else set it to None. 
                
            
            json_result[dict] = {"State Name":STATES[dict], "Num_Positive_Tweets": count(classifications==1), "Num_Negative_Tweets": count(classifications==0)}

path = 'queries/' + str(int(time.time())) + '.json'
    
file = open(path, 'w')
file.write(json.dumps(dict))
print(path)
file.close()

            
