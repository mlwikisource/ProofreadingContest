﻿#!/usr/bin/python
# -*- coding: utf-8 -*-


import wikipedia
import pagegenerators
import codecs
import catlib
import sys
siteFamily	= 'wikisource'
siteLangCode	= 'ml'
category = "WSDCPages"
wikipedia.setLogfileStatus(True)
wikiSite = wikipedia.Site(code=siteLangCode, fam=siteFamily)
cat = catlib.Category(wikiSite,"Category:"+category)
fp = open("/var/www/clients/client23/web27/web/ProofreadingContest/index.html","w")
list = cat.articlesList(recurse=False)
noofarticles=len(list)
per=noofarticles*100/1496
stat={}
pagecount={}
for i in list:
    print i.title()
    creator = i.getCreator()
    noofchar=len(i.get())
    if creator[0] in stat:
        stat[creator[0]] = stat[creator[0]]+noofchar
        pagecount[creator[0]]=pagecount[creator[0]]+1
    else:
        stat[creator[0]] = noofchar
        pagecount[creator[0]]=1
wikipedia.stopme()
print stat
out='<link href="css/bootstrap.css" rel="stylesheet" /><body style="margin-left:10%;margin-right:10%;">    <h1 style="text-align:center;">        <img src="images/Wikisource-logo.png" width="100px" height="100px" /><br /><big>വിക്കിഗ്രന്ഥശാല    </big>   <br /> മത്സരത്തിന്റെ കണക്കുകൾ  </h1> <div class="progress  progress-striped active">  <div class="progress-bar progress-bar-danger"  role="progressbar" aria-valuenow="'+str(noofarticles)+'" aria-valuemin="0" aria-valuemax="100" style="width: '+str(per)+'%">    <span class="sr-only">45% Complete</span>  </div></div>'
out=out+'<table class="table table-bordered">'
for key,value in sorted(stat.iteritems(), key=lambda (v,k): (k,v),reverse=True):
    out=out+"<tr><td><a href='http://ml.wikisource.org/wiki/User:"+key.encode("UTF-8") + "'>"+key.encode("UTF-8")+"</a></td><td><a href='http://ml.wikisource.org/wiki/Special:Contributions/" + key.encode("UTF-8")+"'>"+ str(value) + "</a></td></tr>"
out=out+"</table>"
out=out+'<script src="https://code.jquery.com/jquery.js">  </script>  <script src="js/bootstrap.min.js">  </script><div class="footer-fixed-bottom" style="text-align:center" >Designed by <u><a href="http://ml.wikisource.org">Malayalam Wikisource</a></u></div> </body>'
resultPage="User:Balasankarc\count"
#myResultPage=wikipedia.Page(site=wikiSite,title=resultPage)
#myResultPage.put(out,comment=ur"Calculating Count")
fp.write(out)
fp.close()
fp = open("/var/www/clients/client23/web27/web/ProofreadingContest/index2.html","w")
stat=pagecount
out='<link href="css/bootstrap.css" rel="stylesheet" /><body style="margin-left:10%;margin-right:10%;">    <h1 style="text-align:center;">        <img src="images/Wikisource-logo.png" width="100px" height="100px" /><br /><big>വിക്കിഗ്രന്ഥശാല    </big>   <br /> മത്സരത്തിന്റെ കണക്കുകൾ  </h1> <div class="progress  progress-striped active">  <div class="progress-bar progress-bar-danger"  role="progressbar" aria-valuenow="'+str(noofarticles)+'" aria-valuemin="0" aria-valuemax="100" style="width: '+str(per)+'%">    <span class="sr-only">45% Complete</span>  </div></div>'
out=out+'<table class="table table-bordered">'
for key,value in sorted(stat.iteritems(), key=lambda (v,k): (k,v),reverse=True):
    out=out+"<tr><td><a href='http://ml.wikisource.org/wiki/User:"+key.encode("UTF-8") + "'>"+key.encode("UTF-8")+"</a></td><td><a href='http://ml.wikisource.org/wiki/Special:Contributions/" + key.encode("UTF-8")+"'>"+ str(value) + "</a></td></tr>"
out=out+"</table>"
out=out+'<script src="https://code.jquery.com/jquery.js">  </script>  <script src="js/bootstrap.min.js">  </script><div class="footer-fixed-bottom" style="text-align:center" >Designed by <u><a href="http://ml.wikisource.org">Malayalam Wikisource</a></u></div> </body>'
resultPage="User:Balasankarc\count"
#myResultPage=wikipedia.Page(site=wikiSite,title=resultPage)
#myResultPage.put(out,comment=ur"Calculating Count")
fp.write(out)
fp.close()

