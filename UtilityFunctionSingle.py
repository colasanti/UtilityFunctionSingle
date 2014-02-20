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

