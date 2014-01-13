#!/usr/bin/python
# -*- coding: utf-8 -*-


import wikipedia
import pagegenerators
import codecs
import catlib
import sys
from urllib import urlopen
from StringIO import StringIO
import re
import json

siteFamily      = 'wikisource'
siteLangCode    = 'ml'
wikiSite = wikipedia.Site(code=siteLangCode, fam=siteFamily)
url="http://tools.wmflabs.org/tsreports/?wiki=mlwikisource&report=DC2014_fullist&format=json"
json_data=urlopen(url).read()
json_data=StringIO(json_data)
data=json.load(json_data)
key,value = data.items()
noofarticles=len(value[1])
stat={}
pagecount={}
count=1
per=noofarticles*100/1784
stat={}
pagedetails={}
sumchar=0
sumpages=0
counter=1
for i in value[1]:
   creator = i[u'User'][u'fulltitle'][11:]
   page=i[u'Page'][u'fulltitle']
   noofchar=int(i[u'Page length'])
   if u'വർഗ്ഗം' in page:
      print "Boom"
      continue
   if creator in stat:
        stat[creator] = stat[creator]+noofchar
        pagecount[creator]=pagecount[creator]+1
   else:
       stat[creator] = noofchar
       pagecount[creator]=1
   print count
   count = count+1
wikipedia.stopme()
out=' <meta charset="UTF-8"><link href="css/bootstrap.css" rel="stylesheet" /><body style="margin-left:10%;margin-right:10%;">    <h1 style="text-align:center;">        <img src="images/Wikisource-logo.png" width="100px" height="100px" /><br /><big>വിക്കിഗ്രന്ഥശാല    </big>   <br /><a href="https://ml.wikisource.org/wiki/WS:DC2014">ഡിജിറ്റൈസേഷൻ മത്സരത്തിന്റെ </a>കണക്കുകൾ  </h1> <div class="progress  progress-striped active">  <div class="progress-bar "  role="progressbar" aria-valuenow="'+str(noofarticles)+'" aria-valuemin="0" aria-valuemax="100" style="width: '+str(per)+'%">    <span class="sr-only">45% Complete</span>  </div></div>'
out=out+'<table class="table table-bordered"><tr><th>സ്ഥാനം</th><th>പേര്</th><th>അക്ഷരങ്ങളുടെ എണ്ണം</th><th>താളുകളുടെ എണ്ണം</td</th></tr>'
for key,value in sorted(stat.iteritems(), key=lambda (v,k): (k,v),reverse=True):
    out=out+"<tr><td>"+str(counter)+"</td><td><a href='http://ml.wikisource.org/wiki/User:"+key.encode("UTF-8") + "'>"+key.encode("UTF-8")+"</a></td><td><a href='http://ml.wikisource.org/wiki/Special:Contributions/" + key.encode("UTF-8")+"'>"+ str(value) + "</a></td><td>"+str(pagecount[key])+"</td></tr>"
    counter=counter+1
    sumchar=sumchar+value
    sumpages=sumpages+pagecount[key]
out=out+"<tr><th></th><th> ആകെ  </th><th>"+str(sumchar)+"</th><th>"+str(sumpages)+"</th></tr>"
out=out+"</table>"
out=out+'<script src="https://code.jquery.com/jquery.js">  </script>  <script src="js/bootstrap.min.js">  </script><div class="footer-fixed-bottom" style="text-align:center" >Designed by Balasankar C for <u><a href="http://ml.wikisource.org">Malayalam Wikisource Community</a></u><br /> Technical Support - <u><a href="http://smc.org.in">Swathanthra Malayalam Computing</a></u></div> </body>'
fp = open("/var/www/clients/client23/web27/web/ProofreadingContest/index.html","w")
fp.write(out)
fp.close()
