#-------------------------------------------------------------------------------------------
# This module determines the probability for the input file to be a Spam or Ham
# It uses using Laplace's smoothing alrogithm.
#
# It uses the following tables to determine class prior and Spam/Ham probabilities
# db    ==> test.db
# table   ==> word_tab
#           contains postive/negative word counts for individual words
# table   ==> tot_tab
#           contains total positive/negative words and total/postive/negative file count
#-------------------------------------------------------------------------------------------

import sys, re, os, os.path, glob, codecs
import sqlite3, math, nltk

conn = sqlite3.connect('test.db')
print ("Database connected " )
cur = conn.cursor ()
print ("Cursor opened ")

def db_read_tot(listtot):

    cur.execute("SELECT count from tot_tab where name = ?", listtot)
    row = cur.fetchone()
    if (row):
        return int(row[0])
    else:
        #print ("not found : ", listtot)
        return(0)

def db_read_word(listword):

    cur.execute("SELECT count from word_tab where name = ? and word = ?", listword)
    row = cur.fetchone()
    if (row):
        print ("found uni: ", listdbq)
        return int(row[0])
    else:
        #print ("not found : ", listdbq)
        return(0)
    
#def wordTokenizier(line):
#    delimiters = "[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+|[.,!;:()^*'-/]"
#    tokenList = re.findall(delimiters, line)
#    return tokenList

def wordTokenizier(line):
# wordList will contain only Adjectives (JJ), Adverbs (RB), Verbs (VB) and Noun (NN)
    text = nltk.word_tokenize(line)
    wordList = []
    tokenizedSentence = nltk.pos_tag(text)
    for st in tokenizedSentence:
        
        if st[1][0:2] == "JJ"  or \
           st[1][0:2] == "RB"  or \
           st[1][0:2] == "VB"  or \
           st[1][0:2] == "NN" :
            wordList.append(st[0])
    return wordList

def Lapl_Smth(testfile):
    C_vocSize = 65000
    C_polarity = 0.7
    
    print ("starting read_file with Vocabulary Size ", C_vocSize, \
           "and Polarity ratio ", C_polarity)
    sentCount = 0
# calculate the class priors
    c_total = db_read_tot(["TOTFILE"]
    c_word_spam = db_read_tot(["POSWORD"])
    c_word_ham = db_read_tot(["NEGWORD"])
                          
    p_c_spam = db_read_tot(["POSFILE"])/c_total)
    p_c_ham = db_read_tot(["NEGFILE"])/c_total)

    
# Open & read file in a loop and collect all the words in a dictionary (testWord)
    for line in open(testfile):
        line = line.rstrip()
                
        words = wordTokenizier(line)
                 
        testWord = {}
        for w in words:
            if w in testWord:
                testWord[w] += 1
            else:
                testWord[w] = 1
                        
    spamProb = math.log(p_c_spam)
    hamProb = math.log (p_c_ham)
    
    for k in testBi.keys():
       # compute probability of each word - e.g. ["POS", <word>] and ["NEG", <word>]
        listw2 = []
        listw2.append (k)
        poswordlist = ["POS"] + listw2
        negwordlist = ["NEG"] + listw2

        spamProb = spamProb + math.log((db_read_word(poswordlist)+1) \
                   /(C_vocSize + c_word_spam))

        hamProb = hamProb + math.log((db_read_word(negwordlist)+1) \
                   /(C_vocSize + c_word_ham))

    polarity = spamProb/hamProb

    if polarity < C_Polarity:
        print ("Test Doc ", testfile, \
               " cannot be determine \- manual labelling needed")
    else:
        if hamProb > spamProb:
            print ("Test Doc ", testfile, " is a ham")
        else:
            print ("Test Doc ", testfile, " is a spam")
    
    print ("Test Document ", testfile, \
           "Spam prob = " spamProb, "Ham prob = ", hamProb)
            
print ("total file :", db_read_tot(["TOTFILE"]))

#testfile = "C:\Python34\Data\TOYDataEnglish.txt"
#Lapl_Smth (testfile)

conn.close()
print ("DB connection closed")
