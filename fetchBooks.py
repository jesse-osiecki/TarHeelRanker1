'''fetch all the books from the site, save them in a local db'''

import os
from buzhug import Base
import urllib
import json
import os.path as osp
import sys

dbDir = os.getcwd()
dbDir += '/db'
mode = 'override'

bookDB = Base(osp.join(dbDir, 'bookDB')).create(
    ('ID', int),
    ('slug', unicode),
    ('author_id', int),
    ('reviewed', bool),
    ('language', unicode),
    ('json', unicode),
    ('script_review_status', int),
    mode=mode)

page = 1
host = 'http://gbserver3a.cs.unc.edu'
find = ('/find/?search=&category=&reviewed=&audience=&language=' +
        '&json=1&page=%d')
bookAsJson = '/book-as-json/?id=%s'
while True:
    findURL = host + find % page
    fp = urllib.urlopen(findURL)
    bytes = fp.read().decode('utf-8')
    data = json.loads(bytes)
    if len(data['books']) == 0:
        break
    for info in data['books']:
        fp = urllib.urlopen(host + bookAsJson % info['ID'])
        bytes = fp.read().decode('utf-8')
        book = json.loads(bytes)
        try:
            #make sure record doesnt exist? Implelement later
            #check the stock reviewed status and put it in the field I will play with
            #2 is unsure spam, 1 is HAM, 0 is spam. The json only has T/F right now so will work with that
            spam = 2
            if book['reviewed']:
                spam = 1


            bookDB.insert(
                ID=int(book['ID']), slug=book['slug'],
                author_id=int(book['author_id']), reviewed=book['reviewed'],
                language=book['language'], json=bytes, script_review_status=spam)
        except:
            print book
            raise
    page += 1
    print >>sys.stderr, page

