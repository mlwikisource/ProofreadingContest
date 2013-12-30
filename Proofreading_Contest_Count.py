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
fp = open("a.csv","w")
list = cat.articlesList(recurse=True)
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
namelist=[]
countlist=[]
for i in sortname:
    splited=str(i).split(',')
    name=splited[0][3:-1]
    count=splited[1][1:-1]
 #   namelist.append(name)
 #   countlist.append(count)
    stat[name]=int(count)
#bothlist=zip(countlist,namelist)
#bothlist.sort()
#print bothlist
out="<table>"
for key,value in sorted(stat.iteritems(), key=lambda (v,k): (k,v),reverse=True):
    out=out+"<tr><td>[[User:"+key.encode("UTF-8") + "]]</td><td>[[Special:Contributions/" + key.encode("UTF-8")+"|"+ str(value) + "]]</td></tr>"
out=out+"</table>"
resultPage="User:Balasankarc\count"
myResultPage=wikipedia.Page(site=wikiSite,title=resultPage)
myResultPage.put(out,comment=ur"Calculating Count")
fp.close()
