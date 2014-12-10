NLP-Proj-Spam-Ham
=================

email Spam detection using ML algorithms
----------------------------------------
This is a class project for NLP course that I did with IIIT Hyderabad during Monsoon 2014.

It uses a Naive Bayesian classifier to determine whether an email is spam or not spam (ham)

It requires SQLITE3 to store its model which is used to determin the spam/ham. Essentially, the project consists of the following components:

(1) Classifier (NBSpamClassifier.py) : This reads the train files and creates two output files (outtot.txt and outword.txt)

(2) DB scripts are used to load these files on SQLITE3 DB tables (TOT_TAB and WORD_TAB)

(3) Ananlyser (NBSpamAnalyzerDirectory) that runs on the test files and classifies mails. Different analyzers are created so that it can work either on a single file or on all files in a directory.

(4) Test and Train datasets are to be stored on the directories as shown in the Script/Bayesian folder of this repository.

(5) Following Python packages are used: sys, os.path, glob, sqlite3, math, nlt, matplotlib

(6) Test and train datasets are taken from http://www.aueb.gr/users/ion/data/enron-spam/

Future work: Develop, train and test SVM classifier for spam detection
