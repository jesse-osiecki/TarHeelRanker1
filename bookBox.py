#Jesse Osiecki for GBs Tar Heel Reader

from buzhug import Base
import json
import os
import bogoWrapper as bg


class bogoCheck:
    def __init__(self, books):
        self.books = books
        self.checkedBooks = {}

    def check(self):
        for book in self.books:
            if book.reviewed:
                print book.slug, 'reviewed'
            else:
                allText = ''
                for i in book.text:
                    allText += i
                    allText += '\n'
                rval = bg.bogofilter(allText)
                #book.script_review_status = rval
                #this is mostly for debugging purposes
                #makes a dict of all books looked at and
                #what the final decision was in this specific
                #test
                self.checkedBooks[book.iD] = rval
                print 'Book', book.slug, book.iD, 'checked as ', rval


class authorCheck:
    def __init__(self, books):
        self.books = books
        self.authorDict = {}

    def cfheck(self):
        for book in self.books:
            if book.author not in self.authorDict:
                #if there is no key for the author,
                #make it and initialize to 0 score
                self.authorDict[book.author] = 0
            if book.reviewed:
                self.authorDict[book.author] += 1
            else:
                #will add more here eventually
                if int(book.created[0:4]) < 2011:
                    #if unreviwed and earlier than 2011 it is probably junk
                    self.authorDict[book.author] -= 1

    def printAuthorDict(self):
        for i in self.authorDict:
            print i, self.authorDict[i]


class book:
    def __init__(self, dd, s, rc, au, rv, tt, md,
                 rd, ad, tg, cd, lk,
                 ai, i, tx, pg, ct,
                 rt, txt, srs, slug):
        self.dbID = dd
        self.status = s
        self.rating_count = rc
        self.author = au
        self.rating_value = rv
        self.title = tt
        self.modified = md
        self.reviewed = rd
        self.audience = ad
        self.tags = tg
        self.created = cd
        self.link = lk
        self.author_ID = ai
        self.iD = i
        self.typex = tx
        self.pages = pg
        self.categories = ct
        self.rating_total = rt
        self.text = txt
        self.slug = slug
        print 'Creating book object:', 'dbID: ', self.dbID, self.slug, '\n'
        self.script_review_status = srs


class bookDBHandler:

    def __init__(self):

        self.userdir = os.getcwd()
        self.bookDB = Base(self.userdir + '/db/bookDB').open()
        #this selects the whole db, for now
        self.resultset = self.bookDB.select()

        #for loading the db in memory
        self.membooks = []

    def loadDBIn(self):
        for r in self.resultset:
            #load specific book's json from bookDB
            jsonObj = json.loads(r.json)
            dbID = r.__id__
            script_review_status = r.script_review_status
            #put all relavant info into convienient fields.
            #Im sure there is a quicker way involving commas
            #with Python, will look at later
            status = jsonObj.get('status')
            rating_count = jsonObj.get('rating_count')
            #slug = jsonObj.get('slug')
            #language = jsonObj.get('language')
            author = jsonObj.get('author')
            rating_value = jsonObj.get('rating_value')
            title = jsonObj.get('title')
            modified = jsonObj.get('modified')
            #bust = jsonObj.get('bust')
            reviewed = jsonObj.get('reviewed')
            audience = jsonObj.get('audience')
            tags = jsonObj.get('tags')
            created = jsonObj.get('created')
            link = jsonObj.get('link')
            author_id = jsonObj.get('author_id')
            iD = jsonObj.get('ID')
            typex = jsonObj.get('type')
            pages = jsonObj.get('pages')
            categories = jsonObj.get('categories')
            rating_total = jsonObj.get('rating_total')
            slug = r.slug
            text = []
            #do the same for the pages
            for p in pages:
                text.append(p['text'])
            #nice little book object
            #print dbID
            #break
            elBook = book(dbID, status, rating_count,
                          author, rating_value, title, modified,
                          reviewed, audience, tags, created, link,
                          author_id, iD, typex, pages, categories,
                          rating_total, text, script_review_status, slug)
            self.membooks.append(elBook)

    def saveDB(self):
        #for now the only thing that
        #should be saved is the script_reviewed_status
        for b in self.membooks:
            self.resultset[b.dbID].script_review_status = b.script_review_status

    def closeDB(self):
        self.bookDB.cleanup()
        self.bookDB.close()
