#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division # floating numbers
import nltk
import re
import sys, traceback, os

#change the current working directory in order to use my functions
os.chdir('/Users/marceloschiessl/RDF_text_project') 

import similarity_Metrics
from similarity_Metrics import *
from similarity_Metrics import jaccard, ss, dice
#from queryingSparql import createPhysicalFile
    
############ Doc input ###########
file_read1 = '/Users/marceloschiessl/Documents/workspaceWTA/NLP prog/dados/TESTES ONTOLOGIA/example_schematriples.txt'
file_read2 = '/Users/marceloschiessl/Documents/workspaceWTA/NLP prog/dados/TESTES ONTOLOGIA/bibtex.txt' 
file_read3 = '/Users/marceloschiessl/Documents/workspaceWTA/NLP prog/dados/TESTES ONTOLOGIA/foaf.txt'
##################################


def ss(reference_txt,doc1): #still in development
    """ (string, string) -> float 
    Return the proportion of the set A which overlaps the set B, which is 
    the reference text.
    >>>ss("shirt shoes pants","shirt shoes pants")
    1.0
    >>>ss("shirt shoes pants socks","shirt skirt shoes")
    0.83
    >>>ss("short skirt ship","shirt shoes pants socks")
    0.0
    """
    a = set(reference_txt.split())
    b = set(doc1.split())
    try:
        if len(a) or len(b) > 0:
            return float(
            (len(a.intersection(b)))*len(a.union(b))/
            (len(a)*len(b))
            )
        else:
            return 0.
    except Exception, e:
        print repr(e)
        return repr(e)


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
    wFile = compare + ".output.txt"
    to_file = open(wFile, 'w') #opening the file to write
    print>>to_file, 'line x Files lineFile1 lineFile2 Jaccard SubsetString Dice' #creating header
    for i in range(len(text1)):
        lin1 = ''.join(text1[i])
        if lin1.find('#') != -1:#check whether there's a label in the line
            str1a = re.sub(r'https?://[^# ]+#?', '', lin1)
            str1b = re.sub('None', '', str1a)
            str1 = re.sub(r'[()]', '', str1b)
        for j in range(len(text2)):
            lin2 = ''.join(text2[j])
            if lin2.find('#') != -1:
                str2a = re.sub(r'https?://[^# ]+#?', '', lin2)
                str2b = re.sub('None', '', str2a)
                str2 = re.sub(r'[()]', '', str2b)
                #print '============'
                print>>to_file, str(i) + 'x' + str(j) + ' | ' + str1.lower() + ' | ' + str2.lower() + ' | ' + 'Jaccard = ' + str(round(jaccard((str1),str2))) + ' | ' + 'String Subset = ' + str(round(ss(str1.lower(),str2.lower()),2)) + ' | ' + 'Dice = ' + str(round(dice(str1.lower(),str2.lower()),2))
                print str(i) + 'x' + str(j) + ' | ' + str1.lower() + ' | ' + str2.lower() + ' | ' + 'Jaccard = ' + str(round(jaccard((str1),str2))) + ' | ' + 'String Subset = ' + str(round(ss(str1.lower(),str2.lower()),2)) + ' | ' + 'Dice = ' + str(round(dice(str1.lower(),str2.lower()),2))
    
    to_file.close() #closing the file
    return             

#defining files to be compared
print compare(file_read1,file_read2)
print compare(file_read1,file_read3)

