#this is a script that uses the bookDB to train bogofilter using the bogoWrapper python wrapper in this package
from bookBox import *
import bogoWrapper

def trainGood(dbH):
	


#main part of script
#open book db and load them in
dbHandler = bookDBHandler()
dbHandler.loadDBIn()
#train the good books
trainGood(dbHandler)
#train the bad books
trainBad(dbHandler)
dbHandler.closeDB()
