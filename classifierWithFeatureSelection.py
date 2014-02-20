#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  classifierWithFeatureSelection.py
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
import math




def loadSpecies(speciesFile,stratifyType,classes,classType,stratType):
    
    data = open(speciesFile,"r")
    count =0
    for line in data:
        row = line.strip().split("\t")
        # print ("%s\t%s\t%s\t%s\t%s\t%d"%(row[0],row[1],row[2],row[3],row[4],len(row)-4))
        if (row[classType] in classes):
            print count,row[classType]
            count+=1
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






def featureSelect(speciesFile,speciesList,listSize,typeDefault,catOn):
    orderedList = []
    
    def addToList(name,val):
        n = 0
        orderedList[n][0]=name
        orderedList[n][1]=val
    
        while n< listSize-1  and orderedList[n][1] > orderedList[n+1][1]:
            holdn =  orderedList[n+1][0]
            holdv =  orderedList[n+1][1]
            orderedList[n+1][0] = orderedList[n][0]
            orderedList[n+1][1] = orderedList[n][1]
            orderedList[n][0] = holdn
            orderedList[n][1] = holdv
            n+=1
    
    
    for i in range(listSize):
        a = []
        a.append("E")
        a.append(0)
        orderedList.append(a)    
    
    data = open(speciesFile,"r")
    functions = {}
    types = typeDefault.copy()
    for line in data:
        typesc = []
        #row = line.split("\t")
        row = line.strip().replace(', ','\t').replace('; ','\t').replace(' / ','\t').split("\t")
        if speciesList.count(row[0])>0:
            types[row[catOn]]+=1
            for i in range (5, len(row)-4):
                if typesc.count(row[i]) == 0 :
                    typesc.append(row[i])
                    if (row[i] in functions)==False:
                        functions[row[i]]=typeDefault.copy()
                    functions[row[i]][row[catOn]] += 1

    data.close()
    typesTotal=0
    for k, v in types.iteritems():
        typesTotal += v
    for f in functions:
        t = 0
        for k, v in functions[f].iteritems():
            t += v
        tt = float(t)/typesTotal
        
        info = 0
        for k, v in functions[f].iteritems():
            n = float(v)/typesTotal
            if n > 0:
                tn  = float(types[k])/typesTotal
                info =  n * math.log( n/ ((tt) * tn))
        
        addToList(f,info)
        
    functionsList =[]
    for i in range(listSize-1,1,-1):
        functionsList.append(orderedList[i][0])
        #print orderedList[i][0],orderedList[i][1]
    
    return functionsList
    
def train(speciesFile,speciesList,aClassifier,catOn):
    
    data = open(speciesFile,"r")
    count =0
    
    for line in data:
        #row = line.strip().split("\t")
        row = line.strip().replace(', ','\t').replace('; ','\t').replace(' / ','\t').split("\t")
        if speciesList.count(row[0])>0:
            #print row[0]
            typesc = []
            aClassifier.incc(row[catOn])
            for i in range(5,len(row)):
                if typesc.count(row[i]) == 0 :
                    typesc.append(row[i])
                aClassifier.incf(row[i],row[catOn])

def trainFeatures(speciesFile,speciesList,selectedFeatures,useAll,aClassifier,catOn):
    
    data = open(speciesFile,"r")
    count =0
    
    for line in data:
        row = line.strip().replace(', ','\t').replace('; ','\t').replace(' / ','\t').split("\t")
        #row = line.split("\t")
        if speciesList.count(row[0])>0:
            #print row[0]
            aClassifier.incc(row[catOn])
            typesc = []
            for i in range(5,len(row)):
                if useAll or selectedFeatures.count(row[i])>0:
                    if typesc.count(row[i]) == 0 :
                        typesc.append(row[i])
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
    classes = {'N':0,'P':0}
    #classes = {'aerobic':0,'anaerobic':0,'facultative':0}
    #classes = {'aerobic':0,'anaerobic':0}


    
    stratifyType = {}
    testList =[]
    teachingList = []

    classType = gram
    #classType = metabolisam
    stratType = gram
    #stratType = metabolisam
    stratType = phylum
    
    
    loadSpecies(dataFile,stratifyType,classes.copy(),classType,stratType)
    createLists(stratifyType,teachingList,testList,4)
    selectedFunctions = featureSelect(dataFile,teachingList,500,classes.copy(),classType)
    
    #default = 0.5
    #weight = 1.0e-1
    #for x in range(1,20):
    #    total=0
    #    for i in range(10):
    #        random.shuffle(teachingList)
    #        splitPoint = len(teachingList)/3
    #        aClassifier =  naiveBayes({'N':0,'P':0},weight,default)
    #        train(dataFile,teachingList[splitPoint:],selectedFunctions[:x*2],aClassifier,gram)
    #        total+=validate(dataFile,teachingList[:splitPoint-1],aClassifier,gram)
    #    
    #    print"%d\t%.3f\t%.3e" % (x,float(total)/10, weight)
    #    random.shuffle(teachingList)
    #    aClassifier =  naiveBayes({'N':0,'P':0},weight,default)
    #    train(dataFile,teachingList,selectedFunctions[:x*2],aClassifier,gram)
    #    print validate(dataFile,testList,aClassifier,gram)
    #return 0

    default = 0.5
    weight = 1.0e-1
    #for i in range(1,50):
    #    aClassifier =  naiveBayes(classes,weight,default)
    #    random.shuffle(teachingList)
    #    trainFeatures(dataFile,teachingList,selectedFunctions[:i],False,aClassifier,classType)
    #    print i,validate(dataFile,testList,aClassifier,classType)
    aClassifier =  naiveBayes(classes.copy(),weight,default)
    random.shuffle(teachingList)
    trainFeatures(dataFile,teachingList,selectedFunctions[:40],False,aClassifier,classType)
    print 40,validate(dataFile,testList,aClassifier,classType)
    
    aClassifier =  naiveBayes(classes.copy(),1.0e-20,default)
    train(dataFile,teachingList,aClassifier,classType)
    print "All",validate(dataFile,testList,aClassifier,classType)
    

    return 0

if __name__ == '__main__':
	main()



#for x in range(10):
##        total=0
#        for i in range(10):
#            random.shuffle(teachingList)
#            splitPoint = len(teachingList)/3
#            aClassifier =  naiveBayes({'N':0,'P':0},weight,default)
#            train(dataFile,teachingList[splitPoint:],selectedFunctions,aClassifier,gram)
#            total+=validate(dataFile,teachingList[:splitPoint-1],aClassifier,gram)
#        
#        print"%.3f\t%.3e" % (float(total)/10, weight)
#        random.shuffle(teachingList)
#        aClassifier =  naiveBayes({'N':0,'P':0},weight,default)
#        train(dataFile,teachingList,selectedFunctions,aClassifier,gram)
#        print validate(dataFile,testList,aClassifier,gram)
#        weight=weight/5.0
#    return 0
