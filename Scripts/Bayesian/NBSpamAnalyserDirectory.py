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

import sys, os.path, glob, sqlite3, math, nltk
import matplotlib.pyplot as plt

# define the global variables (constants) used in many functions

global C_vocSize
global C_polarity

# set up the constants - vocubulary size and polarity

C_vocSize = 65000
C_polarity = 0.5

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
        #print ("found uni: ", listword)
        return int(row[0])
    else:
        #print ("not found : ", listword)
        return(0)

def draw_pie (undeter, correct, incorrect):

    labels = 'Undetermined', 'Correct', 'Incorrect'

    sizes = []
    sizes.append(undeter)
    sizes.append(correct)
    sizes.append(incorrect)

    colors = ['gold', 'yellowgreen', 'red']
    explode = (0, 0.1, 0) # only "explode" the 2nd slice (i.e. 'Hogs')

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
    # Set aspect ratio to be equal so that pie is drawn as a circle
    # Create title and place it on the chart
    plt.axis('equal')
    plt.title('Accuracy Chart', bbox={'facecolor':'0.8', 'pad':5}, y = 1.08)

    plt.show()
    
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

def Bayesian_Analyzer (pathfile):
      
    print ("INFO - starting the Analyser with Vocabulary Size ", C_vocSize, \
           "and Polarity ratio ", C_polarity, '\n')

# calculate the class priors

    c_total = db_read_tot(["TOTFILE"])

    c_word_spam = db_read_tot(["POSWORD"])
    c_word_ham = db_read_tot(["NEGWORD"])
    p_c_spam = (db_read_tot(["POSFILE"])/c_total)
    p_c_ham = (db_read_tot(["NEGFILE"])/c_total)

    spamProb = math.log(p_c_spam)
    hamProb = math.log (p_c_ham)

    print ("Spam prob ", spamProb, "Ham Prob", hamProb)
    
# Define and set up counts for calculating accuracy later
    totaltest = 0
    nondetermined = 0
    correct = 0
    incorrect = 0
    outfile = open("outBayesian.txt", 'w')
    
# Loop through test data set and call Lapl_Smth to determine Spam/Ham
# for all files in the directory
# Calculate the undetermined, correct and incorrect number in a pie chart
# after all the files are processed
    path = "testspam"
    print ("INFO - Processing Spam test data set\n")
    for filename in glob.glob(os.path.join(path, '*spam.txt')):
        totaltest += 1
        emotion = Lapl_Smth (filename, outfile, "Spam", spamProb, hamProb, c_total, c_word_spam, c_word_ham)
        if emotion == 2:
            nondetermined += 1
        else:
            if emotion == 1:
                correct += 1
            else:
                incorrect += 1
        
    path = "testham"
    print ("INFO - Processing Ham test data set\n")
    for filename in glob.glob(os.path.join(path, '*ham.txt')):
        totaltest += 1
        emotion = Lapl_Smth (filename, outfile, "Ham", spamProb, hamProb, c_total, c_word_spam, c_word_ham)
        if emotion == 2:
            nondetermined += 1
        else:
            if emotion == 0:
                correct += 1
            else:
                incorrect += 1

# Now draw the pie chart                
    draw_pie(nondetermined, correct, incorrect)
    outfile.close
#---------------------------------------------------------------------------------------
    
def Lapl_Smth (testfile, outfile, emotext, spamProb, hamProb, c_total, c_word_spam, c_word_ham):
        
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
                
# The file is processed now and we have the tokens needed in testWord dictionary.
# Now compute the probability        
    for k in testWord.keys():
       # compute probability of each word - e.g. ["POS", <word>] and ["NEG", <word>]
        listw2 = []
        listw2.append (k)
        poswordlist = ["POS"] + listw2
        negwordlist = ["NEG"] + listw2

        spamProb = spamProb + math.log((db_read_word(poswordlist)+1) \
                   /(C_vocSize + c_word_spam))

        hamProb = hamProb + math.log((db_read_word(negwordlist)+1) \
                   /(C_vocSize + c_word_ham))

    polarity = abs((abs(spamProb) - abs(hamProb)))

    if polarity < C_polarity:
        print (testfile," cannot be determined. Original label ", \
               emotext)
        outtext = testfile + " cannot be determined. Original label " + emotext + '\n'
        outfile.write(outtext)
                
        detemotion = 2
    else:
        if (hamProb) > (spamProb):
            print (testfile, \
                   " is a ham. Original label ", emotext)
            outtext = testfile + " is a ham. Original label " + emotext + '\n'
            outfile.write(outtext)
            
            detemotion = 0
        else:
            print (testfile, \
                   " is a spam. Original label ", emotext)
            outtext = testfile + " is a Spam. Original label " + emotext+ '\n' 
            outfile.write(outtext)
            
            detemotion = 1
    
    print ("Spam prob = ", \
           spamProb, "Ham prob = ", hamProb, "polarity = ", polarity, '\n')

    outtext = " Spam prob = " + str(spamProb) + " Ham prob = " + str(hamProb) \
              + " polarity = " + str(polarity) + '\n'
    outfile.write(outtext)
    outfile.write('\n')

    return (detemotion)
#--------------------------------------------------------------------------------------------

#print ("total file :", db_read_tot(["TOTFILE"]))
pathfile = "testspam"
Bayesian_Analyzer (pathfile)
conn.close()
print ("DB connection closed")
