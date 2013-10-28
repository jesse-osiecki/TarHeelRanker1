#!/usr/bin/python2.7
#this is a script that uses the bookDB to train
#bogofilter using the bogoWrapper python wrapper in this package
from buzhug import Base
import os
import redis
import redisbayes
import sys


def good_train(result, rb):
    for b in result:
        if b.script_review_status is 1:#added condition that rating should be high as well to even dataset
            rb.train('good', b.text)
            print "trained ham: ", str(b.ID), "\n"

def bad_train(result, rb):
    for b in result:
        if b.script_review_status is 0:
            rb.train('bad', b.text)
            print "trained spam: ", str(b.ID), "\n"


##arguments
rating_cutoff = 0  # no rating cutoff by default. 4 is higher than possible
for index, el in enumerate(sys.argv):
    if el == '-R':
        rating_cutoff = int(sys.argv[index+1])

if rating_cutoff <= 3:
    print 'rating_cutoff set to ', rating_cutoff

#main part of script
#open book db and load them in
userdir = os.getcwd()
db = Base(userdir + '/db/bookDB').open()
resultset_good = db.select(rating_value = [rating_cutoff,3])
resultset_bad = db.select(publish_status = False)
#open redis
rb = redisbayes.RedisBayes(redis.StrictRedis(host='localhost', port=6379, db=0))
#train the books
good_train(resultset_good, rb)
bad_train(resultset_bad, rb)
db.close()
