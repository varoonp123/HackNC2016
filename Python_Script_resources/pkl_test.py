#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 19:42:00 2016

@author: Varoon
"""
from sklearn.externals import joblib
v=[None]*10
for i in range(0,10):
    print i
    v[i]=i

joblib.dump(v,"test.pkl")