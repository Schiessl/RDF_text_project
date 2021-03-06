#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division # floating numbers
import nltk
from numpy import zeros,dot
from numpy.linalg import norm
from nltk.metrics import *
from nltk.corpus import stopwords
import jellyfish
import sys, traceback, os

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
    pattern = r'''(?x) ([A-Z]\.)+ # set flag to allow verbose regexps
| \w+(-\w+)* # abbreviations, e.g. U.S.A.
| \$?\d+(\.\d+)?%? # words with optional internal hyphens
| \.\.\. # currency and percentages, e.g. $12.40, 82% # ellipsis
| [][.,;"'?():-_`] # these are separate tokens
'''
    no_punct = ' '.join(nltk.regexp_tokenize(text,pattern))
    return no_punct

# Cosine similarity
def add_word(w,dic):
    """It Adds words to a dictionary for words/count.
"""
    dic.setdefault(w,0) # setdefault() method to index words in a dictionary
    dic[w] += 1

def doc_vec(doc,key_idx):
    '''It creates vector of the words
'''
    v=zeros(len(key_idx))
    for word in doc.split():
        keydata=key_idx.get(word, None)
        if keydata: v[keydata[0]] = 1
    try:
        return v
    except:
        print "Error found:"
        traceback.print_exc(file=sys.stdout)

def cosine_similarity(doc1,doc2):
    """ (string, string) -> float
Return the coefficient of similarity between two texts. It equates 1 for
exact match and 0 to no similarity.
>>>cosine_similarity('shirt shoes pants socks
','short skirt ship')
1.0
>>>cosine_similarity('short skirt ship','short skirt ship')
0.0
"""
    # just to make it work!!! Should be revised. This step should not be required
    if len(doc1.split()) > len(doc2.split()):
        str1 = doc1
        str2 = doc2
    else:
        str1 = doc2
        str2 = doc1
    all_words=dict()
    for dat in [str1,str2]:
        [add_word(w,all_words) for w in dat.split()]
        # build an index of keys so that we know the word positions for the vector
        key_idx=dict() # key-> ( position, count )
        keys=all_words.keys()
        keys.sort()
# print keys
        for i in range(len(keys)):
            key_idx[keys[i]] = (i,all_words[keys[i]])
        
        del keys # it doesn't need to save the keys
        del all_words # neither the all_words
        v1=doc_vec(str1,key_idx)
        v2=doc_vec(str2,key_idx)
# print v1, v2
# print str1
# print str2
        try:
            return float(dot(v1,v2) / (norm(v1) * norm(v2))
                        )
        except:
            print "Error found:"
            traceback.print_exc(file=sys.stdout)

def jaccard(doc1,doc2):
    """ (string, string) -> float
Return the coefficient of similarity between two texts as the size of the
intersection divided by the size of the union of the texts. It equates 1 for
exact match and 0 to no similarity.
>>>jaccard('power','power')
1.0
>>>jaccard('power','abba')
0.0
"""
    union = set(doc1.split()).union(set(doc2.split()))
    intersec = set(doc1.split()).intersection(set(doc2.split()))
    try:
        return float(len(intersec)/len(union))
    except:
        print "Error found:"
        traceback.print_exc(file=sys.stdout)

def dice(doc1,doc2):
    """ (string, string) -> float
Return the coefficient of similarity between two sequence of strings. Based
on Jaccard coefficient, it gives twice the weigth to agreements. It equates
1 for exact match and 0 to no similarity.
>>>dice_coefficient('power','power')
1.0
>>>dice_coefficient('power','abba')
0.0
"""
    sum = (doc1.split()) + ((doc2.split()))
    intersec = set(doc1.split()).intersection(set(doc2.split()))
    try:
        return float(2.*len(intersec)/len(sum))
    except:
        print "Error found:"
        traceback.print_exc(file=sys.stdout)

def string_matching(label1, label2): #by Maedchen and Staab
    """ (string, string) -> float
Return the coefficient of similarity between two sequence of strings based on
the Levenshtein distance (edit distance). It equates 1 for exact match and
0 to no similarity.
>>>string_matching('power','power')
1.0
>>>string_matching('power','abba')
0.0
"""
    try:
        if float(min(len(label1),len(label2)) - edit_distance(label1, label2))/min(len(label1),len(label2)) < 0:
            return 0.0
        else:
            return float(min(len(label1),len(label2)) - edit_distance(label1, label2))/min(len(label1),len(label2))
    except:
        print "Error found:"
        traceback.print_exc(file=sys.stdout)

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

def lcs_length(X, Y):#still in development
    m = len(X)
    n = len(Y)
    # An (m+1) times (n+1) matrix
    C = [[0] * (n+1) for i in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if X[i-1] == Y[j-1]:
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    return (C)

                                
# def tanimoto(a,b):
# """ Tanimoto similarity is the so called Jaccard similarity """
# c = set(set(a.split()).intersection(set(b.split())))
# return float(
# len(c)/
# (len(set(a.split())) + len(set(b.split())) - len(c))
# )

def preproc(doc,numStemmer):
    pproc_doc = preproc_txt(no_punctuation(doc), numStemmer).lower() #number represent the stemmer algorithm to use
    return pproc_doc

if __name__ == '__main__':

    """ Example of the texts to compare"""
    doc1 = "Johann Sebastian Bach was born in March, 21st, in 1685 in Eisenach."
    #doc2 = "Johann Sebastian Bach was born in March, 21st, in 1685 in Eisenach."
    doc2 = "Bach was born in March, 21st, in 1685 in Eisenach."
    #doc2 = "Johann Sebastian Bach was born in March, 21st, in 1685 in Eisenach. a this are is an i me mey myself we our ours ourselves you your yourself he him his himself she her hers herself it its itself they them theirs"
    #doc2 ="Elvis is dead"
    #doc1 = "shirt shoes pants socks"
    #doc2 = "shirt skirt shoes"

    """ Preprocessed documents """
    pproc_doc1 = preproc_txt(no_punctuation(doc1), 1).lower() #number represent the stemmer algorithm to use
    pproc_doc2 = preproc_txt(no_punctuation(doc2), 1).lower()
    
    print "Running Test...\n"
    print "Using original Doc1: %s\n\nUsing original Doc2: %s\n" % ( doc1, doc2 )

    print "Doc1. Preprocessed text: %s \n" % pproc_doc1
    print "Doc2. Preprocessed text: %s \n" % pproc_doc2
    
    # distance metrics
    # preprocessed text - stopwords, stemming, removing punctuation
    print "Cosine Similarity = %s \n" % round(cosine_similarity(pproc_doc1,pproc_doc2),3)
    print "Jaccard's coefficientt = %s \n" % round(jaccard(pproc_doc1, pproc_doc2),3)
    print "Jaccard's coefficientt = %s \n" % round(jaccard(preproc(doc1,1), preproc(doc2,1)),1)#function of preprocessing
    print "Dice Coefficient = %s \n" % round(dice(pproc_doc1, pproc_doc2),3)
    print "String Subset Measure = %s \n" % round(ss(pproc_doc1, pproc_doc2),3)
    print "String Matching similarity measure = %s \n" % round(string_matching(pproc_doc1, pproc_doc2),3)
    print "Jaro-Winkler distance = %s \n" % round(jellyfish.jaro_winkler(pproc_doc1, pproc_doc2),3)
    print "Edit distance (Levenshtein) = %s \n" % round(edit_distance(pproc_doc1, pproc_doc2),3)
    print "Binary distance = %s \n" % round(1-binary_distance(pproc_doc1, pproc_doc2),3) # only return whether two strings exactly match or not
    #print "Longest common subsequence = %s \n" % lcs_length(pproc_doc1, pproc_doc2)