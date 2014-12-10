#-------------------------------------------------------------------------------
#
# This module is the Naive Bayesian classifier for Spam detection
# It takes files containing emails labelled as either Spam or Ham as input
# and calculates the following:
# 1) Total number of Spam/Ham mails (files)
# 2) Total number of all words in each category of Spam/Ham mails (files)
# 3) Total number of times a word appears in a Spam and Ham mail
#
#-------------------------------------------------------------------------------

print ("INFO - Starting Classifier - Importing libs")
import os, re, codecs, sys, nltk
import glob

# Set the codecs
sys.stdout = codecs.getwriter('UTF-8')(sys.stdout.detach())
    
def Bayesian_Classifier():

# dictionaries to hold training unigrams, bigrams and total spam (POS) and ham (NEG)
    trainUni, trainBi, trainEmotion = {}, {}, {}
    trainEmotion["POS"] = 1
    trainEmotion["NEG"] = 1
    trainEmotion["TOT"] = 1

    trainUni["POS"] = 1
    trainUni["NEG"] = 1
           
# Loop through train data set to build the unigram and bigram test dict
    #for traindata in spamfiles first :
    path = "trainspam"
    print ("INFO - Processing Spam train data set")
    for filename in glob.glob(os.path.join(path, '*spam.txt')):
        emotion  = "POS"
        trainEmotion[emotion] += 1
        trainEmotion["TOT"] += 1

        for line in open(filename):
            line =  line.replace(u'\ufeff', '')
            sent = line
            words = wordTokenizier(sent)

            for w in words:
                trainUni[emotion] += 1   #holds total words for SPAM or HAM
                biw = emotion + " " + w  #holds total of how many times a word appear in an emotion class
                if biw in trainBi:
                    trainBi[biw] += 1
                else:
                    trainBi[biw] = 1
                               
# Loop through train data set to build the unigram and bigram test dict
    #for traindata in hamfiles now :
    path = "trainham"
    print ("INFO - Processing Ham train data set")
    for filename in glob.glob(os.path.join(path, '*ham.txt')):
        emotion  = "NEG"
        trainEmotion[emotion] += 1
        trainEmotion["TOT"] += 1
               
        for line in open(filename):
            line =  line.replace(u'\ufeff', '')
            sent = line
            words = wordTokenizier(sent)

            for w in words:
                trainUni[emotion] += 1   #holds total words for SPAM or HAM
                biw = emotion + " " + w  #holds total of how many times a word appear in an emotion class
                if biw in trainBi:
                    trainBi[biw] += 1
                else:
                    trainBi[biw] = 1
                               
# dump the counts on the output files

    outwd = open('outword.txt', 'w')
    outfile = open('outtot.txt', 'w')
    
    for r in trainBi.items():
        outwd.write (str(r[0] + " " + str(r[1]))+ '\n')

    for r in trainUni.items():
        outfile.write (str(r[0] + "WORD" + " " + str(r[1]))+ '\n')
        
    outfile.write (str("TOTFILE " + str(trainEmotion["TOT"] - 1)) + '\n')
    outfile.write (str("POSFILE " + str(trainEmotion["POS"] - 1)) + '\n')
    outfile.write (str("NEGFILE " + str(trainEmotion["NEG"] - 1)) + '\n')
    outfile.close
    
    
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

Bayesian_Classifier ()
