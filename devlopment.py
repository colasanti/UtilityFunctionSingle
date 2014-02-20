#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  devlopment.py
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


import sys
import random
from classifier import naiveBayes

def loadSpecies(speciesFile,stratifyType,classType,stratType):
    
    data = open(speciesFile,"r")
    count =0
    for line in data:
        row = line.strip().split("\t")
        # print ("%s\t%s\t%s\t%s\t%s\t%d"%(row[0],row[1],row[2],row[3],row[4],len(row)-4))
        if testMember(row[classType]) :
            print row[classType]
            stratifyType.setdefault(row[stratType], []).append(row[0])
            count +=1
        
    #print count
    data.close()
    count =0 
    for key , instances in stratifyType.iteritems():
        #print "%s\t%d" % (key,len(instances))
        count +=len(instances)
    #print count
    return 0



def selection(types):
    return lambda x: types.count(x)>0
        
testmember = None

def train(speciesFile,speciesList,aClassifier,catOn):
    
    data = open(speciesFile,"r")
    count =0
    
    for line in data:
        row = line.strip().split("\t")
        if speciesList.count(row[0])>0:
            #print row[0]
            aClassifier.incc(row[catOn])
            for i in range(5,len(row)):
                aClassifier.incf(row[i],row[catOn])

            
def validate(speciesFile,speciesList,aClassifier,catOn):
    data = open(speciesFile,"r")
    count =0
    correct = 0
    for line in data:
        row = line.strip().split("\t")
        if speciesList.count(row[0])>0:
            predict = aClassifier.classify(row[5:len(row)]);
            actual = row[catOn]
            if predict == actual : 
                correct+=1
            count+=1
            #print"%s\t%s\t%s" %  (row[0],actual,predict)
    
    return 100.0 * (float(correct)/float(count))
    
def createLists (stratifyType,teachingList,testList,fraction):
    for key in stratifyType:
        random.shuffle(stratifyType[key])
        lisLength = len(stratifyType[key]) 
        if lisLength>(fraction*2):
             x = int(lisLength/fraction)
             for i in range(x,lisLength):
                testList.append(stratifyType[key].pop(0))
             
        for i in range(len(stratifyType[key])):
                teachingList.append(stratifyType[key].pop(0))
                
    return 0
    

def main():
    
    dataFile = sys.argv[1]
    genomeId = 0
    name = 1
    phylum = 2
    gram = 3
    metabolisam = 4

    global testMember
    testMember = selection(["N","P"])
    
    stratifyType = {}
    testList =[]
    teachingList = []

    classType = gram
    stratType = phylum
    
    
    loadSpecies(dataFile,stratifyType,classType,stratType)
    createLists(stratifyType,teachingList,testList,gram)
    
    weight = 1.0e-8
    default = 0.5
    for x in range(10):
        total=0
        for i in range(10):
            random.shuffle(teachingList)
            splitPoint = len(teachingList)/3
            aClassifier =  naiveBayes({'N':0,'P':0},weight,default)
            train(dataFile,teachingList[splitPoint:],aClassifier,gram)
            total+=validate(dataFile,teachingList[:splitPoint-1],aClassifier,gram)
        
        print"%.3f\t%.3e" % (float(total)/10, weight)
        random.shuffle(teachingList)
        aClassifier =  naiveBayes({'N':0,'P':0},weight,default)
        train(dataFile,teachingList,aClassifier,gram)
        print validate(dataFile,testList,aClassifier,gram)
        weight=weight/5.0
    return 0

if __name__ == '__main__':
	main()

