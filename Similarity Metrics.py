#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division # floating numbers
import nltk
from numpy import zeros,dot
from numpy.linalg import norm
from nltk.metrics import *
from nltk.corpus import stopwords
#from fuzzycomp import fuzzycomp
import jellyfish

# preprocessing step to remove stop words and stem words.
def preproc_txt(doc, stemm):
    ''' Returns a string processed by removing a stopwords and words with the 
    length less than three character. Also, we can tokenize/lemmatize by using
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
    pattern = r'''(?x) ([A-Z]\.)+    # set flag to allow verbose regexps 
    | \w+(-\w+)*                     # abbreviations, e.g. U.S.A.   
    | \$?\d+(\.\d+)?%?               # words with optional internal hyphens
    | \.\.\.                         # currency and percentages, e.g. $12.40, 82% # ellipsis
    | [][.,;"'?():-_`]               # these are separate tokens
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
    return v

def cosine_similarity(doc1,doc2):
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
#         print keys
        for i in range(len(keys)):
            key_idx[keys[i]] = (i,all_words[keys[i]])
        
        del keys # it doesn't need to save the keys
        del all_words # neither the all_words
        v1=doc_vec(str1,key_idx)
        v2=doc_vec(str2,key_idx)
#         print v1, v2
#         print str1
#         print str2
        return float(dot(v1,v2) / (norm(v1) * norm(v2)+10**(-200))) # the power is just to avoid division by 0 

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
    return float(len(intersec)/len(union))
    
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
    if float(min(len(label1),len(label2)) - edit_distance(label1, label2))/min(len(label1),len(label2)) < 0:
        return 0.0
    else:
        return float(min(len(label1),len(label2)) - edit_distance(label1, label2))/min(len(label1),len(label2))

def dice_coefficient(a, b):
    """ (string, string) -> float 
    Return the coefficient of similarity between two sequence of strings. Based 
    on Jaccard coefficient, it gives twice the weigth to agreements. It equates 
    1 for exact match and 0 to no similarity.
    >>>dice_coefficient('power','power')
    1.0
    >>>dice_coefficient('power','abba')
    0.0
    """
    if not len(a) or not len(b): return 0.0
    if len(a) == 1:  a=a+u'.'
    if len(b) == 1:  b=b+u'.'
 
    a_bigram_list=[]
    for i in range(len(a)-1):
      a_bigram_list.append(a[i:i+2])
    b_bigram_list=[]
    for i in range(len(b)-1):
      b_bigram_list.append(b[i:i+2])
 
    a_bigrams = set(a_bigram_list)
    b_bigrams = set(b_bigram_list)
    overlap = len(a_bigrams & b_bigrams)
    dice_coeff = overlap * 2.0/(len(a_bigrams) + len(b_bigrams))
    return dice_coeff

def lcs_length(X, Y):
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
#     """ Tanimoto similarity is the so called Jaccard similarity """
#     c = set(set(a.split()).intersection(set(b.split())))
#     return float(
#                  len(c)/
#                  (len(set(a.split())) + len(set(b.split())) - len(c))
#                  )

if __name__ == '__main__':
    print "Running Test...\n"

    """ Texts to compare"""
    doc1 = "Johann Sebastian Bach was born in March, 21st, in 1685 in Eisenach."
    #doc1 = "Johann Sebastian Bach was born in March, 21st, in 1685 in Eisenach. a this are is an i me mey myself we our ours ourselves you your yourself he him his himself she her hers herself it its itself they them theirs"
    #doc2 = "Johann Sebastian Bach was born in March, 21st, in 1685 in Eisenach."
    #doc2 = "Bach was born in March, 21st, in 1685 in Eisenach." 
    #doc2 ="Johann Sebastian Bach (b. 21 March 1685, d. 28 July 1750) was a German composer, organist, harpsichordist, violist, and violinist of the Baroque period. He was born in Eisenach and died in Leipzig."
    #doc2 ="Angelina Jolie was born in the United States of America, and she is married to Brad Pitt"
    doc2 = "Johann Sebastian Bach was born in March, in Eisenach "
    #doc2 ="Elvis is dead"
#     doc1 = "shirt shoes pants socks" 
#     doc2 = "shirt skirt shoes"
#     doc1 = """When I'M a Duchess, she said to herself, (not in a very hopeful tone though), 
#     I won't have any pepper in my kitchen AT ALL. Soup does very well without--Maybe it's 
#     always pepper that makes people hot-tempered...strange woman is distributing food for the masses"""
#     doc1 = """DENNIS: Listen, strange women lying in ponds distributing swords is no basis for 
#     a system of government. Supreme executive power derives from a mandate from the masses, not 
#     from some farcical aquatic ceremony."""
#     doc2 = """DENNIS: Listen, strange women lying in ponds distributing swords is no basis for 
#     a system of government. Supreme executive power derives from a mandate from the masses, not 
#     from some farcical aquatic ceremony."""
#     
#     doc1 = "Johann Sebastian Bach was born in 1685 in Eisenach"
#     doc1 = "In Eisenach, in the year of 1685, Johann Sebastian Bach was born."
#     doc1 = "Johann Sebastian Bach (b. 21 March 1685, d. 28 July 1750) was a German composer, organist, harpsichordist, violist, and violinist of the Baroque period. He was born in Eisenach and died in Leipzig."
#     doc2 = "Johann Sebastian Bach birthDate 1685-07-28 birthPlace Eisenach"


    """ Preprocessed documents """
    pproc_doc1 = preproc_txt(no_punctuation(doc1), 1).lower() #number represent the stemmer algorithm to use
    pproc_doc2 = preproc_txt(no_punctuation(doc2), 1).lower() #number represent the stemmer algorithm to use
    #pproc_doc1 = preproc_txt(doc1, 1).lower()
    #pproc_doc2 = preproc_txt(doc2, 1).lower()
    
#     print "Using original Doc1: %s\n\nUsing original Doc2: %s\n" % ( doc1, doc2 )
    print "Doc1. Preprocessed text: %s \n" % pproc_doc1 
    
    print "Doc2. Preprocessed text: %s \n" % pproc_doc2
    
    
    print "Cosine Similarity %s \n" % cosine_similarity(pproc_doc1,pproc_doc2)
#     print "Jaccard's coefficient Stop Words %s" % jaccard(pproc_doc1, pproc_doc2)
#     print "Jaccard's coefficient Stop Words %s" % jaccard((stopword(doc1)), stopword(doc2))
#     print "Jaccard's coefficient %s" % jaccard(doc1, doc2)
    print "Jaccard's coefficient pre processed text %s \n" % jaccard(pproc_doc1, pproc_doc2)
#     print "Tanimoto's coefficient %s" % tanimoto(doc1, doc2)
    # other distance metrics
#     print "Binary distance %s" % (1-binary_distance(doc1,doc2)) # only return whether two strings exactly match or not
#     print "Edit distance (Levenshtein) %s" % edit_distance(doc1, doc2)
    print "Edit distance (Levenshtein) pre processed text %s \n" % edit_distance(pproc_doc1, pproc_doc2)

#     print "Fuzzycomp Edit distance (Levenshtein) pre processed text %s \n" % fuzzycomp.levenshtein_distance(pproc_doc1, pproc_doc2)
#     print "Fuzzycomp Jaccard distance pre processed text %s \n" % fuzzycomp.jaccard_distance(pproc_doc1, pproc_doc2)
#     print "Fuzzycomp Hamming distance pre processed text %s \n" % fuzzycomp.hamming_distance(pproc_doc1, pproc_doc2)
    #print "Fuzzycomp Jaro distance pre processed text %s \n" % fuzzycomp.jaro_distance(pproc_doc1, pproc_doc2)
    #print "Fuzzycomp Jaro-Winkler distance pre processed text %s \n" % fuzzycomp.jaro_winkler(pproc_doc1, pproc_doc2)
    print "Jellyfish Jaro-Winkler distance pre processed text %s \n" % jellyfish.jaro_winkler(pproc_doc1, pproc_doc2)
    print "Dice Coefficient pre processed text %s \n" % dice_coefficient(pproc_doc1, pproc_doc2)
    print "Longest common subsequence pre processed text %s \n" % lcs_length(pproc_doc1, pproc_doc2)
    print "String Matching similarity measure pre processed text %s \n" % string_matching(pproc_doc1, pproc_doc2)