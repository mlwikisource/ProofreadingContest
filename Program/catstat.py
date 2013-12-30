#!/usr/bin/python
# -*- coding: utf-8 -*-


import wikipedia
import pagegenerators
import codecs
import catlib
import sys
#പ്രധാന പ്രോഗ്രാം ഇവിടെ തുടങ്ങുന്നു. 
#ആവശ്യത്തിനനുസരിച്ച് മാറ്റങ്ങൾ ഇതിനു താഴെ വരുത്തുക
siteFamily	= 'wikisource'
siteLangCode	= 'ml'
category = str(sys.argv[1]).decode("UTF-8")
wikipedia.setLogfileStatus(True)
wikiSite = wikipedia.Site(code=siteLangCode, fam=siteFamily)
cat = catlib.Category(wikiSite,"Category:"+category)
fp = open("a.csv","w")
#പ്രധാനതാളിലെ സംശോധകരെ പരിശോധിക്കുന്നു.
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
print valuelist
valueset = set(valuelist)
valueunique=[]
for i in valueset:
    valueunique.append(i)
countlist = {}
for i in valueunique:
    count = valuelist.count(i)
    countlist[i]=count

for key,value in countlist.items():
    fp.write(key.encode("UTF-8") + "," + str(value) + "\n")
fp.close()
