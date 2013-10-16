#this is a script that uses the bookDB to train
#bogofilter using the bogoWrapper python wrapper in this package
from bookBox import *
import bogoWrapper


def train(dbH):
    for b in dbH.membooks:
        if b.script_review_status is 1:
            st = ''
            for p in b.text:
                st+= p
                st+='\n'
            bg = bogoWrapper.trainHAM(st)
            print "trained ham: ", str(b.dbID), "\n"
            print "bogofilter exit status: ", str(bg)
        elif b.script_review_status is 0:
            st = ''
            for p in b.text:
                st += p
                st += '\n'
            bg = bogoWrapper.trainSPAM(st)
            print "trained spam: ", str(b.dbID), "\n"
            print "bogofilter exit status: ", str(bg)

#main part of script
#open book db and load them in
dbHandler = bookDBHandler()
dbHandler.loadDBIn()
#train the books
train(dbHandler)
dbHandler.closeDB()
