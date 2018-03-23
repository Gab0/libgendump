#!/bin/python

from subprocess import Popen, PIPE

import os
import time
baseDir = 'books'
dbfile = 'reader'
try:
    DB = open(dbfile).read().split('\n')
except:
    DB = []

internalPreview=False
for Dir in os.listdir(baseDir):
    Path = baseDir+'/'+Dir
    print(Path)
    for Book in os.listdir(Path):
        BookPath = Path + '/' + Book
        if Path+'/'+Book in DB:
            continue
        try:
            q = Popen(['evince', BookPath], stdout=PIPE, stderr=PIPE)
            if internalPreview:
                q = Popen(['convert', Path + '/' + Book+'[0]', 'ppreview.png'])
                time.sleep(1)
                w = Popen(['fim', 'ppreview.jpeg'])
            
        except:
            print('Removing broken book;')
            os.remove(Path+'/'+Book)
            continue

        bookSize = round(os.stat(BookPath).st_size/1000000, 3)
        R=input("What about {bn}? {sz}mB     [K]EEP or [D]ISCARD? ".format(bn=Book, sz=bookSize)).lower()
        #q.kill()
        if 'd' in R:
            os.remove(Path+'/'+Book)
        else:
            W=open(dbfile, 'a')
            W.write(Path+'/'+Book+'\n')

            W.close()


