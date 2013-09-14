import bookBox as b

bhandle = b.bookDBHandler()
bhandle.loadDBIn()
#create new author check and run it
authorc = b.authorCheck(bhandle.membooks)
authorc.check()
authorc.printAuthorDict()
