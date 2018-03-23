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
        R=input("What about {}? [K]EEP or [D]ISCARD? ".format(Book)).lower()
        #q.kill()
        if 'd' in R:
            os.remove(Path+'/'+Book)
        else:
            W=open(dbfile, 'a')
            W.write(Path+'/'+Book+'\n')

            W.close()


