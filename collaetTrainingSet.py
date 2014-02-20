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
#  Collate the data  organisms_for_training_set181213_list.txt
#  With the phylum data phylumSEEDGenomes.txt
#  d.setdefault(word, []).append(x)


import sys

def loadPhylum(phylumFile):
    phylumDict = {};
    data = open(phylumFile, "r")
    for line in data:
        row = line.strip().split("\t")
        if len(row) == 2:
            phylumDict[row[0]]= row[1]
    
    data.close()
    return phylumDict

def loadSpecies(rawSpeciesFile,speciesFile,phylumDict):
    data = open(rawSpeciesFile,"r")
    out = open(speciesFile,"w")
    speciesDict = {}
    count = 1
    for line in data:
        row = line.strip().split("\t")
        genomeID = row[0]
        name = row[1]
        names = name.strip().split(" ")
        shortName = "%s %s" % (names[0], names[1])
        if speciesDict.get(shortName,False) == False:
            speciesDict[shortName] = 1
            if len(row) >2 and row[2] !="" and row[2] !="?":
                metabolisam = row[2].strip()
            else:
                metabolisam ="unknown"
            if len(row) >3 and row[3] !="" and row[3] !="?":
                gram = row[3].strip()
            else:
                gram ="unknown"
                
            phylum  = phylumDict.get(genomeID,False)
            if phylum != False:
                out.write("%s\t%s\t%s\t%s\t%s\n"%(genomeID,name,phylum,gram,metabolisam))
                count+=1
            
    out.close()
    data.close()
    return 0
    


def main():
    phylumDict = loadPhylum(sys.argv[1])
    loadSpecies(sys.argv[2],sys.argv[3],phylumDict)
    return 0

if __name__ == '__main__':
	main()

