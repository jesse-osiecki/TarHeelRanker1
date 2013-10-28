#!/usr/bin/python2.7
#this script finds books that were once published
#by THR and then removed, and sets them as bad,
#so that bogofilter has a bad training set

import sqlite3 as lite
import pickle
#import sys
from buzhug import Base
import os


unfound = []
fil = open('badguys', 'r+')
con = lite.connect('scratch/db.sqlite')
cur = con.cursor()
cur.execute("SELECT rowid, *  FROM books ORDER BY rowid")
rows = cur.fetchall()
#go through the list of books and make note of which ones dont exist in bookDB
#bdbh = bb.bookDBHandler()
#bdbh.loadDBIn()
bdbh = Base(os.getcwd() + '/db/bookDB').open()
#shit algorithm man, good thing we are only doing this ~1 time
for r in rows:
    isPublished = False
    bID = r[1]
    slug = r[2]
    aID = r[3]
    result = bdbh.select(ID=bID)
    if len(result) > 0:
        print 'result set ', len(result)  # result is not guaranteed to be 0
        isPublished = True
    if (not isPublished):
        #append the slug and author id if not found;
        #from what I can tell names are not necessarily unique?
        print isPublished, slug, bID, ' is unpublished\n'
        unfound.append(bID)
bdbh.close()
pickle.dump(unfound, fil)
fil.close()
