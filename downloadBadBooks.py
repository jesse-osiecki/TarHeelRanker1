
from buzhug import Base
import urllib2 as urllib
import json
import sys
import pickle
import os

#now ge those books
unfound = []
fil = open('badguys', 'r+')
unfound = pickle.load(fil)
print 'pickle loaded'
userdir = os.getcwd()
bookDB = Base(userdir + '/db/bookDB').open()
host = 'http://gbserver3a.cs.unc.edu'
bookAsJson = '/book-as-json/?id=%s'
for un in unfound:
    try:
        url = host + bookAsJson % un
        print un
        print 'loading ', url
        fp = urllib.urlopen(host + bookAsJson % un)
        bytes = fp.read().decode('utf-8')
        book = json.loads(bytes)
        print 'url loaded', fp
        try:
            #make sure record doesnt exist? Implelement later
            #check the stock reviewed status and put it in the
            #field I will play with
            #2 is unsure spam, 1 is HAM, 0 is spam.
            #The json only has T/F right now so will work with that
            spam_stat = 0
            pub = False
            t = ''
            pages = book['pages']
            for p in pages:
                t += p['text'] + '\n'
            bookDB.insert(
                ID=int(book['ID']), slug=book['slug'],
                author_id=int(book['author_id']), reviewed=book['reviewed'], publish_status=pub,
                text=unicode(t), rating_value=int(book['rating_value']),
                rating_total=int(book['rating_count']),
                audience=unicode(book['audience']),
                language=book['language'], json=bytes, script_review_status=spam_stat)
        except:
            print book
            raise
        print >>sys.stderr, un
    except urllib.HTTPError as e:
        print e.code
fil.close()
