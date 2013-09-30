#this is a wrapper script for bogofilter.

import subprocess as sp
import logging as log
import os


def trainHAM(trainable_words, bogoDIR=os.getcwd()+"/.bogofilter"):
    p1 = sp.Popen(["echo", trainable_words], stdout=sp.PIPE)
    #-e is for emmbeded, makes return codes simple
    #-n is for ham
    p2 = sp.call(["bogofilter", "-e", "-n", "-d", bogoDIR], stdin=p1.stdout)
    p1.stdout.close()  # p1 SIGPIPE exit
    log.info("trainHAM on %s exitcode: %i", trainable_words, p2)
    return p2


def trainSPAM(trainable_words, bogoDIR=os.getcwd()+"/.bogofilter"):
    p1 = sp.Popen(["echo", trainable_words], stdout=sp.PIPE)
    #-e is for emmbeded, makes return codes simple
    #-s is for spam
    p2 = sp.call(["bogofilter", "-e", "-s", "-d",  bogoDIR], stdin=p1.stdout)
    p1.stdout.close()  # p1 SIGPIPE exit
    log.info("trainiSPAM on %s exitcode: %i", trainable_words, p2)
    return p2


def bogofilter(words, bogoDIR=os.getcwd()+"/.bogofilter"):
    p1 = sp.Popen(["echo", words], stdout=sp.PIPE)
    p2 = sp.call(["bogofilter", "-d", bogoDIR], stdin=p1.stdout)
    p1.stdout.close()  # p1 SIGPIPE exit
    log.info("bogofilter on %s exitcode: %i", words, p2)
    # 0 for spam; 1 for non-spam; 2 for unsure ; 3 for I/O or other errors.
    return p2
