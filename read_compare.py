#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division # floating numbers
import nltk
import re
import sys, traceback, os

#change the current working directory in order to use my functions
os.chdir('/Users/marceloschiessl/RDF_text_project') 

from similarity_Metrics import jaccard, ss, pproc
from queryingSparql import createPhysicalFile
    
############ Doc input ###########
file_read1 = '//Users/marceloschiessl/Documents/workspaceWTA/NLP prog/dados/TESTES ONTOLOGIA/example_schematriples.txt'
file_read2 = '//Users/marceloschiessl/Documents/workspaceWTA/NLP prog/dados/TESTES ONTOLOGIA/bibtex.txt' 
file_read3 = '//Users/marceloschiessl/Documents/workspaceWTA/NLP prog/dados/TESTES ONTOLOGIA/foaf.txt'
##################################

def compare(reference, compare):
    with open(reference) as file:
        text1 = []
        for line in file:
            # The rstrip method gets rid of the "\n" at the end of each line
            text1.append(line.rstrip().split(","))
    with open(compare) as file:
        text2 = []
        for line in file:
            # The rstrip method gets rid of the "\n" at the end of each line
            text2.append(line.rstrip().split(","))
    str1 = ''
    str2 = ''
    for i in range(len(text1)):
        lin1 = ''.join(text1[i])
        if lin1.find('#') != -1:#check whether there's a label in the line
            str1a = re.sub(r'https?://[^# ]+#?', '', lin1)
            str1 = re.sub(r'[()]', '', str1a)
        for j in range(len(text2)):
            lin2 = ''.join(text2[j])
            if lin2.find('#') != -1:
                str2a = re.sub(r'https?://[^# ]+#?', '', lin2)
                str2 = re.sub(r'[()]', '', str2a)
                print '============'
                print i, 'x',j, '-', str1.lower(), '-',str2.lower(), '-','Jaccard Similarity = ', jaccard(pproc(str1,1),str2)
                #print i, 'x',j, '-', str1.lower(), '-',str2.lower(), '-','Jaccard Similarity = ', jaccard(str1.lower(),str2.lower()), 'String Subset = ', ss(str1.lower(),str2.lower())
    return             
    #print "Jaccard's coefficientt = %s \n" % round(jaccard(pproc(doc1,1), pproc(doc2,1)),3)

#defining files to be compared
print compare(file_read1,file_read2)
print compare(file_read1,file_read3)
