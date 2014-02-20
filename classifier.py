#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2014 Dr Ricardo L Colasanti <ric@Chicago>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import math
import sys
class classifier:
    def __init__(self,fcDefault):
        # Counts of feature/category combinations
        self.fc={}
        # Counts of documents in each category
        self.cc={}
        self.fcDefault = fcDefault
    
    def incf(self,f,cat):
        self.fc.setdefault(f,self.fcDefault.copy())
        self.fc[f][cat]+=1
        #print"%s\t%s\t%d" % (f,cat, self.fc[f][cat])
    
    def catCount(self,cat):
        return float(self.cc[cat] )
         
    def totalCount(self):
        count=0
        for keys in self.cc:
            count+=self.catCount(keys)
        return count
               
    def fCount(self, f,cat):
        return float(self.fc[f][cat])
        
    def incc(self,cat):
        self.cc.setdefault(cat,0)
        self.cc[cat]+=1
    
    def fprob(self,f,cat):
        if self.cc[cat] == 0 : return 0
        return self.fCount(f,cat)/self.catCount(cat)
        
    def printAtributes(self,cat):
        for key in self.fc:
            print"%s\t%s\t%f" % (key,cat,self.weightedProb(key,cat))
        

        
    def weightedProb(self,f,cat,weight=1.0,ap=0.5):
        # Calculate current probability
        basicprob= self.fprob(f,cat)

        # Count the number of times this feature has appeared in
        # all categories
        totals=sum([self.fc[f][c] for c in self.cc.keys()])

        # Calculate the weighted average
        bp=((weight*ap)+(totals*basicprob))/(weight+totals)
        return math.log(bp)

class naiveBayes(classifier):
  
    def __init__(self,fcDefault,weight=1,default = 0.5):
        classifier.__init__(self,fcDefault)
        self.weight = weight
        self.default = default
  
    def docProb(self,features,catProbs):
        # Multiply the probabilities of all the features together
        # by addding the log of the probabilities together
        for f in features: 
            if self.fc.has_key(f):
                for key in catProbs:
                    catProbs[key]+=self.weightedProb(f,key,self.weight,self.default)

    
    def classify(self,features):
        catProbs = self.fcDefault.copy()
        self.docProb(features,catProbs)
        # Find the category with the highest probability
        max=-sys.float_info.max
        for key in catProbs:
            cFract=self.catCount(key)/self.totalCount()
            cProb = cFract * catProbs[key]
            if cProb>max: 
                max=cProb
                best=key
        return best
