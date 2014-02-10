#!/usr/bin/python
from buzhug import Base
import sys
import os
import redis, redisbayes
import gib_detect
import markover

db = Base(os.getcwd() + '/db/bookDB').open()
#open redis
rb = redisbayes.RedisBayes(redis.StrictRedis(host='localhost', port=6379, db=0))
books = db.select(reviewed=False) #select all unreviewed

redis_bayes = False
gibb = False
markover = False

l = len(sys.argv)
c = 0
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
for b in books:
    rb_score = 0
    gibb_score = 0
    mark_score = 0
    if redis_bayes:
        rb_score = rb.score(b.text)
    if gibb:
        gibb_score = gib_detect.detect(b.text)
    if markover:
        mark_score = 
    
