#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division # floating numbers
import nltk
from nltk.metrics import jaccard_distance
from nltk.corpus import stopwords
import math
import sys, traceback, os

#change the current working directory in order to use my functions
os.chdir('/Users/marceloschiessl/RDF_text_project') 

import similarity_Metrics

    
############ Doc input ###########
file_read1 = '/Users/marceloschiessl/Documents/JSB_DBpedia.txt' 
file_read2 = '/Users/marceloschiessl/Documents/RW_DBpedia.txt' 
#file_read2 = '/Users/marceloschiessl/Documents/SB_DBpedia.txt' 
file_read3 = '/Users/marceloschiessl/Documents/Wikipedia_JSBach.txt' 
#file_read3 = '/Users/marceloschiessl/Documents/www_baroquemusic_org_jsbach_html_JSBach.TXT' 

doc1 = str(open(file_read1,'r').read().split('\n')) #opening the file to read and getting rid of the new line character(\n)
doc2 = str(open(file_read2, 'r').read().split('\n'))
reference_txt = str(open(file_read3,'r').read().split('\n'))
##################################

###### Preprocessing texts ######
pproc_reference_txt = similarity_Metrics.preproc_txt(str(reference_txt), 1).lower() #number represent the stemmer algorithm to use
pproc_doc1 = similarity_Metrics.preproc_txt(str(doc1), 1).lower()
pproc_doc2 = similarity_Metrics.preproc_txt(str(doc2), 1).lower()

print 'Pre processed reference_txt ', pproc_reference_txt
print ''
print 'Pre processed doc1 ', pproc_doc1
print ''
print 'Pre processed doc2 ', pproc_doc2
print ''

print "### Original documents ###"

print "String Subset Measure reference_txt x doc1 = %s " % round(similarity_Metrics.ss(reference_txt, doc1),4)
print "String Subset Measure reference_txt x doc2 = %s " % round(similarity_Metrics.ss(reference_txt, doc2),4)
print "Jaccard's coefficient reference_txt x doc1 = %s " % round(similarity_Metrics.jaccard(reference_txt, doc1),4)
print "Jaccard's coefficient reference_txt x doc2 = %s " % round(similarity_Metrics.jaccard(reference_txt, doc2),4)
print "Dice's coefficient reference_txt x doc1 = %s " % round(similarity_Metrics.dice(reference_txt, doc1),4)
print "Dices's coefficient reference_txt x doc2 = %s \n" % round(similarity_Metrics.dice(reference_txt, doc2),4)
#
print "### Preprocessed documents ###"

print "Cosine Similarity  reference_txt x doc1 = %s " % round(similarity_Metrics.cosine_similarity(pproc_reference_txt,pproc_doc1),4)
print "Cosine Similarity  reference_txt x doc2 = %s " % round(similarity_Metrics.cosine_similarity(pproc_reference_txt,pproc_doc2),4)
print "String Subset Measure reference_txt x doc1 = %s " % round(similarity_Metrics.ss(pproc_reference_txt, pproc_doc1),4)
print "String Subset Measure reference_txt x doc2 = %s " % round(similarity_Metrics.ss(pproc_reference_txt, pproc_doc2),4)
print "Jaccard's coefficient reference_txt x doc1 = %s " % round(similarity_Metrics.jaccard(pproc_reference_txt, pproc_doc1),4)
print "Jaccard's coefficient reference_txt x doc2 = %s " % round(similarity_Metrics.jaccard(pproc_reference_txt, pproc_doc2),4)
print "Dice coefficient reference_txt x doc1 = %s " % round(similarity_Metrics.dice(pproc_reference_txt, pproc_doc1),4)
print "Dice coefficient reference_txt x doc2 = %s \n" % round(similarity_Metrics.dice(pproc_reference_txt, pproc_doc2),4)