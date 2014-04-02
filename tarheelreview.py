#!/usr/bin/python
from buzhug import Base
import sys
import os
import redis, redisbayes
import gib_detect
import markover
import random
import csv
import datetime

###opening remarks
print "\n**************************"
print "Welcome to Tar Heel Ranker v1.0. The goal of this project is to actively assist in the reviewing process of books that have no home. For more information contact Jesse Osiecki at osiecki@cs.unc.edu"
print "standard usage: python tarheelreview.py -FLAGS"
print "Flags are: r for redisbayes checker (Bayesian spam filter. Make sure Redis is running for this"
print "g for gibberish detector using markov chains on letter transitions"
print "m for markover -- markov chain filter using word transitions"
print "a for author check. Outputs number of books a given author has in the Database that are already reviewed"
print "s for rating check. Tests books current rating against a set value (4) and returns boolean if higher"
print "recommended usage is -masg"
print "NOTE: to end the program, simply press CTRL-D and the reviewed books will be noted in a file in the CWD"
print "\n\n**************************"

db = Base(os.getcwd() + '/db/bookDB').open()
#open redis
rb = redisbayes.RedisBayes(redis.StrictRedis(host='localhost', port=6379, db=0))
books = db.select(reviewed=False) #select all unreviewed
markov = markover.Markov()


def author_checker(aut):
    authored_books = db.select(author_id=aut, reviewed=True)
    return len(authored_books)
def rating_checker(rat, lim):
    return rat >= lim
redis_bayes = False
gibb = False
markover = False
author_check = False
rating_check = False

l = len(sys.argv)
c = 0
book_review_cache = {}


def print_to_file():
    filename = "books_reviewed" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + ".csv"
    with open(filename, 'wb') as f:
        w = csv.writer(f)
        for key, value in book_review_cache.iteritems():
            w.writerow([key ,  value])
while c < l-1:
    c+=1
    inp = sys.argv[c]
    if "r" in inp:
        redis_bayes = True
    if "g" in inp:
        gibb = True
    if "m" in inp:
        markover = True
    if "a" in inp:
        author_check = True
    if "s" in inp:
        rating_check = True 
#print redis_bayes, gibb, markover
#books = random.shuffle(books)
book_range = len(books) # we have to randomize this manually


try:
    for x in range(0,book_range):

        print "\n-------------------------------"
        good_choice = False #make sure we choose a new random book each time.
        while good_choice is False:
            b = random.choice(books)
            if b.ID not in book_review_cache.viewkeys():
                good_choice = True
                #print good_choice
        rb_score = 0
        gibb_score = 0
        mark_score = 0
        author_score = 0
        rating_score = 0
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
        if author_check:
            author_score = author_checker(b.author_id)
            #author_score = b.author_id
            print 'author_score: ', author_score
        if rating_check:
            rating_score = rating_checker(b.rating_value, 4)
            print 'rating_score: ', rating_score
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
except EOFError:
    print_to_file()
except KeyboardInterrupt:
    print_to_file()

