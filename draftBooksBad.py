#this script finds books that were once published
#by THR and then removed, and sets them as bad,
#so that bogofilter has a bad training set

import sqlite3 as lite
import bookBox as bb
import pickle


unfound = []
fil = open('badguys', 'r+')
con = lite.connect('scratch/db.sqlite')
cur = con.cursor()
cur.execute("SELECT rowid, *  FROM books ORDER BY rowid")
rows = cur.fetchall()
#go through the list of books and make note of which ones dont exist in bookDB
bdbh = bb.bookDBHandler()
bdbh.loadDBIn()
#shit algorithm man, good thing we are only doing this ~1 time
for r in rows:
    isPublished = False
    slug = r[2]
    aID = r[3]
    for m in bdbh.membooks:
        if slug == m.slug:
            isPublished = True
            break
    if (not isPublished):
        #append the slug and author id if not found;
        #from what I can tell names are not necessarily unique?
        print r[1], slug, aID, ' is unpublished\n'
        unfound.append(r[1])
bdbh.closeDB()
pickle.dump(unfound, fil)
fil.close()
