#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division # floating numbers
import nltk
import re
import sys, traceback, os
import xlrd

#change the current working directory in order to use my functions
os.chdir('/Users/marceloschiessl/RDF_text_project') 

import similarity_Metrics
from similarity_Metrics import *
from similarity_Metrics import jaccard, ss, dice
#from queryingSparql import createPhysicalFile
    
############ Doc input ###########
arqExcel = '/Users/marceloschiessl/Documents/workspaceWTA/NLP prog/dados/TESTES ONTOLOGIA/arqExcel.xlsx'
##################################

# preprocessing step to remove stop words and stem words.
def preproc_txt(doc, stemm):
    ''' Returns a string processed by removing a stopwords and words with the 
    length less than three character. Also, it can tokenize/lemmatize by using
    Porter and Lancaster algorithms and the Wordnet lemmatizer '''
    tokens = nltk.word_tokenize(doc)
    stpw = [word for word in tokens if word not in stopwords.words('english') and len(word) > 3]
    if stemm == 1:
        lemma = nltk.WordNetLemmatizer()
        stmw = [lemma.lemmatize(word) for word in stpw]
        text = nltk.Text(stmw)
    elif stemm == 2:
        stemmer = nltk.PorterStemmer()
        stmw = [stemmer.stem(word) for word in stpw]
        text = nltk.Text(stmw)
    elif stemm == 3:
        stemmer = nltk.LancasterStemmer()
        stmw = [stemmer.stem(word) for word in stpw]
        text = nltk.Text(stmw)
    else:
        text = nltk.Text(stpw)
    
    pproc_txt = ' '.join(text)
    return pproc_txt

def no_punctuation(text):
    '''(string) -> string
    Extract puncts, marks and other symbols, but it preserves some others. See 
    the commentaries in the pattern variable.
    >>>no_punctuation(no_punctuation("I'm sick!")
    I ' m sick
    >>>print no_punctuation("thing, ball, football?!#")
    thing , ball , football ?
    '''
    pattern = r'''(?x) ([A-Z]\.)+    # set flag to allow verbose regexps 
    | \w+(-\w+)*                     # abbreviations, e.g. U.S.A.   
    | \$?\d+(\.\d+)?%?               # words with optional internal hyphens
    | \.\.\.                         # currency and percentages, e.g. $12.40, 82% # ellipsis
    | [][.,;"'?():-_`]               # these are separate tokens
    '''
    no_punct = ' '.join(nltk.regexp_tokenize(text,pattern))
    return no_punct

def preproc(doc,numStemmer):
    pproc_doc = preproc_txt(no_punctuation(doc), numStemmer).lower() #number represent the stemmer algorithm to use
    return pproc_doc
    
    

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

def compare(arqExcel, abaReference, abaCompare):

    wb = xlrd.open_workbook(arqExcel)
    
    text1 = []
#     sh = wb.sheet_by_index(abaReference) # if we have only the sheets' index
    sh = wb.sheet_by_name(abaReference)

    for rownum in range(sh.nrows):
        line = str(sh.row_values(rownum))
        text1.append(line.rstrip().split(","))

    text2 = []
#     sh = wb.sheet_by_index(abaCompare) # if we have only the sheets' index
    sh = wb.sheet_by_name(abaCompare)
    for rownum in range(sh.nrows):
        line = str(sh.row_values(rownum))
        text2.append(line.rstrip().split(","))

    str1 = ''
    str2 = ''
    wFile = str(abaCompare) + ".excel.output.txt"
    to_file = open(wFile, 'w') #opening the file to write
    print>>to_file, 'line x Files lineFile1 lineFile2 Jaccard SubsetString Dice' #creating header
    for i in range(len(text1)):
        lin1 = ''.join(text1[i])
        str1 = lin1

        for j in range(len(text2)):
                lin2 = ''.join(text2[j])
#             if lin2.find('#') != -1:
#                 str2a = re.sub(r'https?://[^# ]+#?', '', lin2)
#                 str2b = re.sub('None', '', str2a)
#                 str2 = re.sub(r'[()]', '', str2b)
                str2 = lin2
                #print '============'
                print>>to_file, str(i) + 'x' + str(j) + ' | ' + preproc(str1,1) + ' | ' + preproc(str2,1) + ' | ' + 'Jaccard = ' + str(round(jaccard(preproc(str1,1),preproc(str2,1)))) + ' | ' + 'String Subset = ' + str(round(ss(preproc(str1,1),preproc(str2,1)),2)) + ' | ' + 'Dice = ' + str(round(dice(preproc(str1,1),preproc(str2,1)),2))
                print str(i) + 'x' + str(j) + ' | ' + preproc(str1,1) + ' | ' + preproc(str2,1) + ' | ' + 'Jaccard = ' + str(round(jaccard(preproc(str1,1),preproc(str2,1)))) + ' | ' + 'String Subset = ' + str(round(ss(preproc(str1,1),preproc(str2,1)),2)) + ' | ' + 'Dice = ' + str(round(dice(preproc(str1,1),preproc(str2,1)),2))
    
    to_file.close() #closing the file
    return             

#defining files to be compared
#sheets'names: [u'Ref', u'Classes Ref', u'Properties Ref', u'BIBTEX', u'BIB  Classes', u'Properties BIB', u'FOAF', u'Classes Foaf', u'Properties Foaf']

#Comparing Classes:
#Classes Ref x Classes BIB
#Classes Ref x Classes FOAF
#
#Comparing Properties:
#Properties Ref x Properties BIB
#Properties Ref x Properties FOAF

#Classes
# print compare(arqExcel, u'Classes Ref', u'BIB  Classes')
# print compare(arqExcel, u'Classes Ref', u'Classes Foaf')
#Properties
# print compare(arqExcel, u'Properties Ref', u'Properties BIB')
print compare(arqExcel, u'Properties Ref', u'Properties Foaf')
