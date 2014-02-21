#!/usr/bin/env python
# Caculate a utility function for the phenotypes that emerge out of the fuctional roles of a set of bacterial genomes

# version 1.0 single class -ve gram stain or + gram stain

# Read in the genome id phentype class and list of functions from a tab delimied text file
#   separate line for each genome
#   id \t name \t phylum \t metabolisam \t gram \t funtion0 \t function1 \t ..... functionN
#   the functoions may have to be further parsed to separate out for multi function genes

# for each function count the number of times it occurs in a genome of a classtype

# Calculate a utility function for each functional type
# The utility functions are: Mutual Information Chi squared and frequencey

# for each class keep a list of the top 100 functions as measured by there utility function
# Create ordered stack
#  two dimensional array function name and value
#  if maximum value set all values to minimum
#  keep trackof bottom value
#  if new value is larger than last value add to stack
#   starting from the top compare eac value with the new value if it is larger
#   replace the value and push the stack down
import math
import sys
import UpdatedSortedArray

def log2(a):
    if a==0:
        return 0
    return math.log(a)/math.log(2)

def featureSelect(speciesFile,classList,listSize,catOn):
    
    data = open(speciesFile,"r")
    functions = {}
    types = classList.copy()
    for line in data:
        typesc = []
        row = line.strip().replace(', ','\t').replace('; ','\t').replace(' / ','\t').split("\t")
        if row[catOn] in classList:
            #print row[0],row[catOn]
            types[row[catOn]]+=1
            for i in range (5, len(row)-4):
                # count oly one instance per genome
                if typesc.count(row[i]) == 0 :
                    typesc.append(row[i])
                    if (row[i] in functions)==False:
                        functions[row[i]]=classList.copy()
                    functions[row[i]][row[catOn]] += 1

    data.close()
   
    
    sa = UpdatedSortedArray.UpdatedSortedArray(listSize)   
    N = types['N']+types['P']
    
    pID = 'P'
    allNeg = float(N) - types[pID]
    allPos = float(types[pID])
    for f in functions:
        t = functions[f]['P']+functions[f]['N']
        
        neg = float(t) -functions[f][pID]
        pos = float(functions[f][pID])

        n00 = allNeg-neg #genomes that are not of class and do not have Function
        n01 = neg # Genomes not in class but has function
        n10 = allPos-pos #Genome in of class but does not have function 
        n11 = pos #Genome in class and does have function

        I1=0
        if ((n11+n10)*(n11+n01))>0:
            I1 = (n11/N) * log2((N*n11)/((n11+n10)*(n11+n01))) 
        
        I2 = 0
        if ((n10+n00)*(n11+n01))>0:
            I2 = (n01/N) * log2((N*n01)/((n01+n00)*(n11+n01))) 
        
        I3 = 0
        if((n01+n10)*(n10+n00)) > 0:
            I3 = (n10/N) * log2((N*n10)/((n11+n10)*(n10+n00))) 
        
        I4=0
        if((n01+n00)*(n10+n00))>0:
            I4 = (n00/N) * log2((N*n00)/((n01+n00)*(n10+n00)))
        I = I1+I2+I3+I4
        sa.addData(f,I)
        
    y = sa.getArray()
    for i in range(len(y)):
        print y[i][0], y[i][1],functions[y[i][0]]['N'],functions[y[i][0]]['P']



def main():
    #featureSelect(sys.argv[1],{"aerobe":0,"anaerobe":0,"facultative":0},100,4)
    featureSelect(sys.argv[1],{"P":0,"N":0},50,3)

    return 0

if __name__ == '__main__':
    main()