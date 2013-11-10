#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division # floating numbers
import nltk
import re

def jaccard(a,b):
    """ The Jaccard's similarity between two texts """
    union = set(a.split()).union(set(b.split())) #len(a | b) #or a.union(b)
    intersec = set(a.split()).intersection(set(b.split()))#len(a & b) #or a.intersection(b)
    return float(
                 len(intersec)/
                 len(union)
                 )
    
############ Doc input ###########
file_read1 = '//Users/marceloschiessl/Documents/workspaceWTA/NLP prog/dados/TESTES ONTOLOGIA/doc1.txt'
file_read2 = '//Users/marceloschiessl/Documents/workspaceWTA/NLP prog/dados/TESTES ONTOLOGIA/doc2.txt' 
file_read3 = '//Users/marceloschiessl/Documents/workspaceWTA/NLP prog/dados/TESTES ONTOLOGIA/doc3.txt'
##################################

with open(file_read1) as file:
    text1 = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        text1.append(line.rstrip().split(","))
with open(file_read2) as file:
    text2 = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        text2.append(line.rstrip().split(","))

#for i in range(len(text1)):
#    for j in range(len(text2)):
#        print i, j, jaccard(str(text1[i]),str(text2[j]))
#
for i in range(len(text1)):
    lin1 = ''.join(text1[i])
    if lin1.find('#') != -1:#check whether there's a label in the line
        str1 = re.search(r'#(.*)', lin1).group(1)

    for j in range(len(text2)):
        lin2 = ''.join(text2[j])
        if lin2.find('#') != -1:
            str2 = re.search(r'#(.*)', lin2).group(1)
            
            print '============'
            print i, 'x',j, '-', str1.lower(), '-',str2.lower(), '-','Jaccard Similarity = ', jaccard(str1.lower(),str2.lower())