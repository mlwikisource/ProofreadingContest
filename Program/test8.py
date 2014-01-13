#!/usr/bin/python
# -*- coding: utf-8 -*-

"""ഒരു സൂചികാതാളിലെ എല്ലാ പേജുകളിലുള്ള ഉള്ളടക്കവും ഒരു പുതിയ പേജിലേക്ക് എഴുതാൻ
നിർമ്മിച്ചത്: ബാലശങ്കർ സി
നന്ദി: സുനിൽ വി.എസ്
05/01/2013
"""

import wikipedia
import pagegenerators
import codecs
import re

f = open("file.txt","w")
siteFamily      = 'wikisource'
siteLangCode    = 'ml'
pageNamespaceId = 106 #ഗ്രന്ഥശാലയുടെ ഐഡി. മാറ്റേണ്ട ആവശ്യമില്ല.
wikiSite = wikipedia.Site(code=siteLangCode, fam=siteFamily)
myTitle=u'താൾ:A Grammer of Malayalam 1863.pdf/195'
myPage=wikipedia.Page(site=wikiSite,title=myTitle)
myText = myPage.get()
print myText
match = re.findall(r'^<noinclude.*}}\n\n\n',myText)
myText=myText.replace(match[0],'')
match = re.findall(r'</noinclude>',myText)
myText=myText.replace(match[0],'')
match = re.findall(r'<noinclude>.*</div>',myText)
myText=myText.replace(match[0],'')
print len(myText)
print myText
'''a=list(myText)
print a
print len(a)
print "Before Encoding : "
print len(myText)   #അങ്ങനെ ഉണ്ടെങ്കിൽ ലിവൻ എറർ കാണിക്കും. 
print "After Encoding : "
print len(myText.encode("UTF-8"))
b=list(myText.encode("UTF-8"))
print b
print len(b)'''
wikipedia.stopme()
f.close()
