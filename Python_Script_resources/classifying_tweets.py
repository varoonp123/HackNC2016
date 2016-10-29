#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 18:15:16 2016

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

#GOAL: Given tweets, use first classifier (Linguistic Characteristics) to determine if tweet has sentiment. Use
#FeatureUnion to link that vectorizer with a tfidf vectorizer, determining if it is positive/negative sentiment


#Loads SentiwordNet, a publication by researchers at Istituto di Scienza e Tecnologie dell’Informazione
#Gives most words in the english language positivity and negativity scores between 0 and 1.

#Make sure SentiWordNet file and training set are in the same directory as this. 
def load_sent_word_net():
    print 'loading sent word net'
    sent_scores = collections.defaultdict(list)
    with open("SentiWordNet_3.0.0_20130122.txt", "r") as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        for line in reader:
            if line[0].startswith("#"):
                continue
            if len(line)==1:
                continue
            POS,ID,PosScore,NegScore,SynsetTerms,Gloss = line
            if len(POS)==0 or len(ID)==0:
                continue
            #print POS,PosScore,NegScore,SynsetTerms
            for term in SynsetTerms.split(" "):
               # drop number at the end of every term
                term = term.split("#")[0]
                term = term.replace("-", " ").replace("_", " ")
                key = "%s/%s"%(POS,term.split("#")[0])
                sent_scores[key].append((float(PosScore),
                float(NegScore)))
        for key, value in sent_scores.iteritems():
            sent_scores[key] = np.mean(value, axis=0)
    return sent_scores

    
def create_ngram_model():
   print 'creating ngram model'
   tfidf_ngrams = TfidfVectorizer(stop_words='english', decode_error='ignore',analyzer="word", binary=False)
   clf = MultinomialNB(alpha=1.0)
   pipeline = Pipeline([('vect', tfidf_ngrams), ('clf', clf)])
   return pipeline
#FIRST CLASSIFIER WILL DETERMINE IF TWEET HAS SENTIMENT


class LinguisticVectorizer(BaseEstimator):
    'creating ling vectorizer'
    
    def get_feature_names(self):
        return np.array(['sent_neut', 'sent_pos', 'sent_neg',
            'nouns', 'adjectives', 'verbs', 'adverbs',
            'allcaps', 'exclamation', 'question', 'hashtag',
            'mentioning'])
    def _get_sentiments(self,d):
        
        sent = tuple(d.split())
        tagged = nltk.pos_tag(sent)
        pos_vals=[]
        neg_vals=[]
        nouns=0
        adjs=0
        verbs=0
        adverbs=0
        
        #for each word and part of speech tag in tagged array
        
        for w,t in tagged:
            
            p,n=0,0
            sent_pos_type=None
            if t.startswith("NN"):
                sent_pos_type = "n"
                nouns+=1
            elif t.startswith("JJ"):
                sent_pos_type = "a"
                adjs+=1
            elif t.startswith("VB"):
                sent_pos_type = "v"
                verbs+=1
            elif t.startswith("RB"):
                sent_pos_type = "r"
                adverbs+=1
            if sent_pos_type is not None:
                sent_word = "%s/%s"%(sent_pos_type,w)
                if sent_word in sent_word_net:
                    p,n =sent_word_net[sent_word]
            pos_vals.append(p)
            neg_vals.append(n)
        l=len(sent)
        avg_pos_val = np.mean(pos_vals)
        avg_neg_val = np.mean(neg_vals)
        return [1-avg_pos_val - avg_neg_val , avg_pos_val, avg_neg_val, nouns/l, adjs/l, verbs/l, adverbs/l]
    def transform(self, documents):
        obj_val, pos_val, neg_val, nouns, adjs, verbs, adverbs = np.array([self._get_sentiments(d) for d in documents]).T
        allcaps=[]
        exclamation=[]
        question=[]
        hashtag=[]
        mentioning=[]
        for d in documents:
            allcaps.append(np.sum([t.isupper() for t in d.split() if len(t)>2]))
            exclamation.append(d.count("!"))
            question.append(d.count("?"))
            hashtag.append(d.count("#"))
            mentioning.append(d.count("@"))
            
            #return np array with number of calculated punctuation, number of allcap words
        print 'transforming'
        return np.array([obj_val, pos_val, neg_val, nouns, adjs, verbs, adverbs, allcaps, exclamation,question,hashtag, mentioning]).T
    def fit(self, documents, y=None):
        print 'fitting'
        return self

#FeatureUnion links two output vectors of two different estimators
def create_union_model(params=None):
    #----------------------------------ADD PREPROCESSING HERE-------------------
    def preprocess_tweet(string):
        return string.lower().replace("-"," ").replace("_"," ")
    tfidf_ngrams = TfidfVectorizer(preprocessor = preprocess_tweet)
    ling_features = LinguisticVectorizer()
    ALL_FEATURES = FeatureUnion([('ling',ling_features), ('tfidf',tfidf_ngrams)])
    clf = MultinomialNB(alpha = 1.0)
    pipeline = Pipeline([('all',ALL_FEATURES),('clf',clf)])
    if params:
        pipeline.set_params(**params)
    print 'creating union model'
    return pipeline
    
def train_model(clf_factory, X, Y):
    # setting random_state to get deterministic behavior
    cv = ShuffleSplit(n_splits=1, test_size=0.01, train_size= 0.99,random_state=0)
    
    scores = []
    pr_scores = []

    for train, test in cv.split(X):
        
        X_train= [X[i] for i in train]
        y_train =[Y[j] for j in train]
        X_test=[X[i] for i in test]
        y_test = [Y[i] for i in test]
        print len(train)
        print len(test)
        print type(test)
        print type(train)
        clf = clf_factory
        clf.fit(X_train, y_train)
        test_score = clf.score(X_test, y_test)
        scores.append(test_score)
        proba = clf.predict_proba(X_test)
        precision, recall, pr_thresholds = precision_recall_curve(y_test, proba[:,1])
        pr_scores.append(auc(recall, precision))
       
    summary = (np.mean(scores), np.std(scores), np.mean(pr_scores), np.std(pr_scores))
    print "%.3f\t%.3f\t%.3f\t%.3f"%summary
 
data = open("Sentiment_Analysis_Dataset.csv")
data.next()     #Skip first line of header
X=[None]*1578628
Y=[None]*1578628
count=0
sent_word_net = load_sent_word_net()
count=0
for line in data:
    splitting = line.split(',')
    X[count]=splitting[3]
    Y[count] = int(splitting[1])
    count+=1
    
print X[500]
print Y[500]



unioned_features = create_union_model()
train_model(unioned_features, X,Y)
