#!/usr/bin/python
# -*- coding: utf-8 -*-


import wikipedia
import pagegenerators
import codecs
import catlib
import sys
siteFamily	= 'wikisource'
siteLangCode	= 'ml'
category = str(sys.argv[1]).decode("UTF-8")
wikipedia.setLogfileStatus(True)
wikiSite = wikipedia.Site(code=siteLangCode, fam=siteFamily)
cat = catlib.Category(wikiSite,"Category:"+category)
fp = open("count.csv","w")
list = cat.articlesList(recurse=False)
out = {}
for i in list:
    print i.title()
    creator = i.getCreator()
    out[i.title()]=creator[0]
wikipedia.stopme()
valuelist=[]
for key,value in out.items():
    valuelist.append(value)
valueset = set(valuelist)
valueunique=[]
for i in valueset:
    valueunique.append(i)
countlist = {}
for i in valueunique:
    count = valuelist.count(i)
    countlist[i]=count
sortname = sorted(countlist.items(), key=lambda x:x[1])
stat={}
for i in sortname:
    splited=str(i).split(',')
    name=splited[0][3:-1]
    count=splited[1][:-1]
    stat[name]=count
for key,value in stat.items():
    fp.write(key.encode("UTF-8") + "," + str(value) + "\n")
fp.close()
