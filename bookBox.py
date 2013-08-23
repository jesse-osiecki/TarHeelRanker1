#Jesse Osiecki for GB's Tar Heel Reader

from buzhug import Base
import json

userdir = '/home/jesse/projects/TarHeelRanker/TarHeelRanker'
db = Base(userdir + '/db/bookDB').open()
resultset = db.select(['json'])

for r in resultset:

    #load specific book's json from bookDB
    jsonObj = json.loads(r.json)

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

    #printing pages for fun. Have to use pages json tag, then treat that obj as dict; 'text' has the text
    for p in pages:
        print p['text']
    print '------'
    break
db.close()
