#!/usr/bin/python
from buzhug import Base
import sys
import os
import redis, redisbayes
import gib_detect
import markover
import random

db = Base(os.getcwd() + '/db/bookDB').open()
#open redis
rb = redisbayes.RedisBayes(redis.StrictRedis(host='localhost', port=6379, db=0))
books = db.select(reviewed=False) #select all unreviewed
markov = markover.Markov()

redis_bayes = False
gibb = False
markover = False

l = len(sys.argv)
c = 0
book_review_cache = {}
while c < l-1:
    c+=1
    inp = sys.argv[c]
    if "r" in inp:
        redis_bayes = True
    if "g" in inp:
        gibb = True
    if "m" in inp:
        markover = True
#print redis_bayes, gibb, markover
for b in random.shuffle(books):
    rb_score = 0
    gibb_score = 0
    mark_score = 0
    print b.text
    if redis_bayes:
        rb_score = rb.score(b.text)
        print 'rb_score: ' , rb_score
    if gibb:
        gibb_score = gib_detect.detect(b.text)
        print 'gibb_score: ' , gibb_score
    if markover:
        mark_score = markov.score_text(b.text)
        print 'mark_score: ' , mark_score
    while True:
        feelings = raw_input('^^Would you say that this is a good book? Y/n --> ').lower()
        yes = set(['yes', 'y'])
        no = set(['no', 'n'])
        if feelings in yes:
            feelings = True
            break
        elif feelings in no:
            feelings = False
            break
        else:
            print "Please enter a valid Y/n"
    book_review_cache[b.ID] = feelings
    print book_review_cache
