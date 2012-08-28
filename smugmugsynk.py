#!/usr/bin/env python

import encodings

def u8(s):
    if type(s) == type(u""):
        return encodings.utf_8.encode(s)[0]
    return s

import httplib2

import random
import time
import os
import os.path
import sys
sys.path.append('smuggler-read-only/src/api/')
from smuggler import Smuggler

import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open('smugmugsynk.cfg'))


import md5



username = config.get('Smugmug','username')
password = config.get('Smugmug','password')
key = config.get('Smugmug','key')

smugmug = Smuggler()

# Gah! 
smugmug.http = httplib2.Http( disable_ssl_certificate_validation=True)

smugmug.login.withPassword(username,password,key)

l = smugmug.albums.get()
random.shuffle(l)

for p in l:






    print "Working on %s " % ( u8(p['Title']))
    print p

    dir = u8(p['Title'])



    desc = u8(smugmug.albums.getInfo(p['id'])['Description'])

    if not os.path.exists(dir):
        os.mkdir(dir)

    if desc and not os.path.exists(dir + os.sep + 'description'):
        open(dir + os.sep + 'description','w').write(desc)

    imgs = smugmug.images.get(p['id'])
    random.shuffle(imgs)

    for q in imgs:

        get = True
        fname = dir + os.sep + u8(smugmug.images.getInfo(q['id'])['FileName'])
        
        caption = u8(smugmug.images.getInfo(q['id'])['Caption'])

        print "Checking %s (%s)" % ( u8(smugmug.images.getInfo(q['id'])['FileName']), u8(smugmug.images.getInfo(q['id'])['OriginalURL']))

        if os.path.exists(fname):
            contents = open(fname).read()

            if  md5.md5(contents).hexdigest() ==  smugmug.images.getInfo(q['id'])['MD5Sum']:               
                get = False
            else:
                print "  Bad md5sum, fetching again."

        if caption and not os.path.exists(fname + '.caption.txt'):
            open(fname + '.caption.txt','w').write(caption)


        if get:
            (resp, content) = httplib2.Http().request(smugmug.images.getInfo(q['id'])['OriginalURL'])

            try:
                open(fname,'w').write(content)
            except:
                print "Failed to write %s " % fname 


            time.sleep(1)

