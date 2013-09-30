import bookBox as b
#this is a script more or less for testing purposes. Get used to it
bhandle = b.bookDBHandler()
bhandle.loadDBIn()
#create new author check and run it
authorc = b.authorCheck(bhandle.membooks)
authorc.check()
authorc.printAuthorDict()

#put bogochecks here

#close and save
bhandle.saveDB()
bhandle.closeDB()
