#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 19:25:16 2016

@author: Varoon
"""
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
import pickle
from classifying_tweets import LinguisticVectorizer
clf = joblib.load('tfidf_linguistic_tweet_NB_classifier.pkl')
print 'done'