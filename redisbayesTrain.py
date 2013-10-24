#this is a script that uses the bookDB to train
#bogofilter using the bogoWrapper python wrapper in this package
from buzhug import Base
import os
import redis
import redisbayes


def train(result, rb):
    for b in result:
        if b.script_review_status is 1:
            rb.train('good', b.text)
            print "trained ham: ", str(b.ID), "\n"
        elif b.script_review_status is 0:
            rb.train('bad', b.text)
            print "trained spam: ", str(b.ID), "\n"

#main part of script
#open book db and load them in
userdir = os.getcwd()
db = Base(userdir + '/db/bookDB').open()
resultset= db.select()
#open redis
rb = redisbayes.RedisBayes(redis.StrictRedis(host='localhost', port=6379, db=0))
#train the books
train(db, rb)
db.close()
