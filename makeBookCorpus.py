#!/bin/python2.7

from buzhug import Base
import os

db = Base(os.getcwd() + '/db/bookDB').open()

res = db.select(reviewed=True) #select all reviewed

for r in res:
    print r.text.encode('utf-8')
