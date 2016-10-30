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
#a=joblib.load(open('tfidf_linguistic_tweet_MultinomialNB_classifier.pkl','rb'))
print 'read classifier'

#Establish connection to twitter API. 
consumer_key='TpCYKB3NtWrkiRdVUUNmHx82h'
consumer_secret='jd5zqkdtjsu1uZHBUCwjBplTkrn3otYB7k54ljmDJ8VyQQoYXX'
access_token='791825707156594688-WDa6SKm0ihheIJKp5lKaISO30oLDPw7'
access_token_secret='cw09NaXRry3RdX0s3nssGp86y8ISr4gwKUoCYAHIdaIis'

twitter = Twython(consumer_key, consumer_secret, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()

twitter = Twython(consumer_key, consumer_secret, access_token,access_token_secret)

#Establish Geocoder
geocoder = Nominatim()
STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
json_result = [None]*50

#Instantiating JSON format
for i in range(0,50):
    json_result[i] = {"State Name":STATES[i],"Num_Positive_Tweets":0, "Num_Negative_Tweets":0 }
QUERY = "hillary"
count =0
coords=0
geo=0
place=0
tweet_text = []
tweet_coords = []
tweets=[]
classifications=[]
geolocations = []
#radius with almost all of the US. Close to getting all geotagged tweets for analysis 
tweets = twitter.cursor(twitter.search,q="QUERY",count=1,geocode ="40.0,-100.0,60mi" )
for tweet in tweets:
    tweets[count] = tweet
    count+=1
    print tweet.keys()
    sys.exit(0)
    print tweet['coordinates']
    
    #sleep right before hitting rate limit of twitter API. Sleep for 15 minutes
    if count%179==0:
        print 'sleeping'
        for i in range(0,len(tweets)):
            classifications[i] = a.predict(tweets[i]['text'])
            s= geocoder.reverse(tweets[i]['coordinates'])
            
            #try to set state given output of reverse geocode. Else set it to None. 
            try:
                if re.split(', ', s.encode("ascii","ignore"))[3] == "United States of America":
                    geolocations[i] = re.split(', ', s.encode("ascii","ignore"))[2] 
            except:
                geolocations[i] = None
        for j in range(0,50):
            json_result[j]["Num_Positive_Tweets"] = count(classifications[classifications==1 and geolocations is not None])
            json_result[j]["Num_Negative_Tweets"] = count(classifications[classifications==0 and geolocations is not None])
        path = 'queries/' + str(int(time.time())) + '.json'
            
        file = open(path, 'w')
        file.write(json.dumps(dict))
        print(path)
        file.close()
        time.sleep(15*60) 
        
print count
print coords
print geo
print place
"""
geocoder = Nominatim()
location = geocoder.reverse("4.0,-100.0)
print location.
"""