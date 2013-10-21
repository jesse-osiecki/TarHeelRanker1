import bookBox

bdbh = bookBox.bookDBHandler()
bdbh.loadDBIn()
bgc = bookBox.bogoCheck(bdbh.membooks)
bgc.check()
