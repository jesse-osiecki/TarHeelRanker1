'''fetch all the books from the site, save them in a local db'''

from buzhug import Base
import urllib
import json
import os.path as osp
import sys

dbDir = '/home/jesse/projects/TarHeelRanker/TarHeelRanker/db'
mode = 'override'

bookDB = Base(osp.join(dbDir, 'bookDB')).create(
    ('ID', int),
    ('slug', unicode),
    ('author_id', int),
    ('reviewed', bool),
    ('language', unicode),
    ('json', unicode),
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
            bookDB.insert(
                ID=int(book['ID']), slug=book['slug'],
                author_id=int(book['author_id']), reviewed=book['reviewed'],
                language=book['language'], json=bytes)
        except:
            print book
            raise
    page += 1
    print >>sys.stderr, page

