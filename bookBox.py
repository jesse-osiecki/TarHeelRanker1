#Jesse Osiecki for GB's Tar Heel Reader

from buzhug import Base
import json
import os
#import book


class bookDBHandler:

    def __init__(self):

        self.userdir = os.getcwd()
        self.bookDB = Base(self.userdir + '/db/bookDB').open()
        #this selects the whole db, even though it specifies json as a requirement
        self.resultset = self.bookDB.select()

    def loadDBIn(self):
        for r in self.resultset:
            #load specific book's json from bookDB
            jsonObj = json.loads(r.json)
            dbID = r.__id__
            #put all relavant info into convienient fields. I'm sure there is a quicker way involving commas with Python, will look at later
            status = jsonObj.get('status')
            rating_count = jsonObj.get('rating_count')
            slug = jsonObj.get('slug')
            language = jsonObj.get('language')
            author = jsonObj.get('author')
            rating_value = jsonObj.get('rating_value')
            title = jsonObj.get('title')
            modified = jsonObj.get('modified')
            bust = jsonObj.get('bust')
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
            text = []
            #do the same for the pages
            for p in pages:
                text.append(p['text']
            #insert this all into a nice little object
            #thisBook =

    def closeDB(self):
        self.bookDB.cleanup()
        self.bookDB.close()
