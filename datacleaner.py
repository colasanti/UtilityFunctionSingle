#!/usr/bin/env python


import sys

def cleanData():
    dataFile = sys.argv[1]
    outFile = sys.argv[2]
    data = open(dataFile,"r")
    out = open(outFile,"w")    
    metaboblisamList = {};
    classType = 4
    for line in data:
        row = line.strip().split("\t")
        #print ("%s\t%s\t%s\t%s\t%s\t%d"%(row[0],row[1],row[2],row[3],row[4],len(row)-4))
        for i in range(4):
            out.write("%s\t"%(row[i]))
        if row[4] == "aerobic":
            out.write("aerobe")
        else:
            if row[4] == "anaerobic":
                out.write("anaerobe")
            else:
                out.write(row[4])
        for i in range(5,len(row)):
            out.write("\t%s"%(row[i]))
        out.write("\n")    
        
        if not(row[classType] in metaboblisamList):
            metaboblisamList[row[classType]]=0
        metaboblisamList[row[classType]]+=1
    for a in metaboblisamList:    
        print a,metaboblisamList[a]
    
    data.close()
    out.close()
    return 0
    
def readData():
    dataFile = sys.argv[1]
    data = open(dataFile,"r")
    metaboblisamList = {};
    classType = 4
    for line in data:
        row = line.strip().split("\t")
        print ("%s\t%s\t%s\t%s\t%s\t%d"%(row[0],row[1],row[2],row[3],row[4],len(row)-4))
        if not(row[classType] in metaboblisamList):
            metaboblisamList[row[classType]]=0
        metaboblisamList[row[classType]]+=1
    for a in metaboblisamList:    
        print a,metaboblisamList[a]
    
    data.close()
    return 0
    
def main():
    #cleanData()
    readData()
if __name__ == '__main__':
    main()

