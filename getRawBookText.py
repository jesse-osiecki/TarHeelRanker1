#!/usr/bin/python2.7
#this is a commandline utility to quickly get book text for testing purposes
from buzhug import Base
import os
import sys
import json


db = Base(os.getcwd() + '/db/bookDB')
db.open()
c=0
l = len(sys.argv)
while c < l-1:
    c+=1
    inp = sys.argv[c]
    dupProtect = True
    bookID = int(inp)
    records = db.select(ID = bookID)
    bookText = ''
    slug = ''
    for r in records:
        j = json.loads(r.json)
        if j.get('ID') == bookID:
            text = j.get('pages')
            for p in text:
                bookText += p['text'] + '\n'
            slug = r.slug
            if dupProtect:
                break
    print bookText
db.close()
