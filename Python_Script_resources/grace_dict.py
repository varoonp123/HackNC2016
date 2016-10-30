#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 10:20:57 2016

@author: Varoon
"""

STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
json_result = []

#Load geographic centers of each state
geo_centers_dict = [None]*50

geofiles = open('geo_centers.csv','r')
print geofiles
lines = geofiles.readline()
for line in lines:
    print line
    newdic ={}
    stateList = line.split(',')
    print stateList
    newdic={"State":stateList[0], "Lat":stateList[1], "Long":stateList[2]}
    geo_centers_dict.append(newdic)
    