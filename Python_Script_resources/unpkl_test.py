#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 19:43:09 2016

@author: Varoon
"""

#if the pickled classifier is in the directory, shows results of prediction for command line strings

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
import pickle
import sys

print 'reading classifier'
a=joblib.load(open('tfidf_linguistic_tweet_MultinomialNB_classifier.pkl','rb'))
print 'read classifier'
if len(sys.argv)>0:
    args = sys.argv
    args.append("i love the amazing great spectacle.")
    results = a.predict(args)
    for i in range(1,len(args)):
        print 'Classification: %d\n-------------String: %s\n\n\n'%(results[i], args[i])
print '\n 0 DENOTES A NEGATIVE SENTIMENT AND 1 DENOTES A POSITIVE SENTIMENT'