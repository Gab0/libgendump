#!/bin/python

import connect
import parseIndex
import os
import time
import pandas as pd
import random
baseUrl = "http://genotypeinczgrxr.onion/LG/"
bookdir = 'books'

def mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def downloadBook(Connection, URL, filename):
    S = Connection.query(URL)
    A = open("%s" % filename, 'wb')
    if type(S) == str:
        S = S.encode('utf-8')
        print(S[:30])
    A.write(S)

def logDebug(message):
    print("[INFO] %s" % message)

def getIndex(Connection, indexnb):
    indexnb = index2str(indexnb)
    URL = baseUrl+indexnb+'/'

    logDebug(URL)
    Q=Connection.query(URL)
    return Q


#getIndex(17)
#getIndex(64)
index2str = lambda indexnb: "{0:0>4}".format(indexnb)

#sBOOK = "http://genotypeinczgrxr.onion/LG/0017/39a9d651c88f5a623f56190cb90fc103"


def processBookList(indexnb, booklist, progress, count):
    C=0
    for b, book in enumerate(booklist):
        try:
            if b < progress.loc[indexnb, 'Progress']:
                continue
        except KeyError:
            progress.loc[indexnb, 'Progress'] = 0

        URL = baseUrl+index2str(indexnb)+ '/' + book
        
        filetree = "books/%s" % index2str(indexnb)
        mkdir(filetree)
        filename = "%s/%s" % (filetree, book)

        if os.path.isfile(filename):
            continue

        zt = time.time()
        logDebug("downloading %i of %i - %s" % (b+1, len(booklist), book))
        try:
            downloadBook(Connection, URL, filename)
            C += 1
        except Exception as e:
            print(e)
        elapsed = time.time() - zt
        logDebug("Finished. %f\n" % elapsed)
        progress.loc[indexnb, 'Progress'] = b+1
        progress.to_csv('progress.csv')

        if C > count:
            return

def loadProgress():
    F = 'progress.csv'
    if os.path.isfile(F):
        progress = pd.DataFrame().from_csv(F)
    else:
        progress = pd.DataFrame(columns=['Progress'])

    return progress
if __name__ == "__main__":

    mkdir(bookdir)
    Connection = connect.TorConnection()
    progress = loadProgress()

    while True:
        indexnb = random.randrange(0,2100)
        W =getIndex(Connection, indexnb)

        booklist=parseIndex.parseHtml(W)
        processBookList(indexnb, booklist, progress, 10)


    Connection.kill()
