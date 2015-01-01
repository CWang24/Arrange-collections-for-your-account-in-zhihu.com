#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -- coding: utf-8 --
import requests
import re
import os


s = requests.session()
login_data = {'email': 'XXX@XXX', 'password': '*********'}
s.post('http://www.zhihu.com/login', login_data)
print 'Visiting collections homepage...'
r = s.get('http://www.zhihu.com/collections/mine')
mycollections =open("mycollections.html","w")
print >> mycollections , "%s"   % (r.text.encode('utf-8'))
print "Homepage saved. Now parsing for "+u"收藏夹",'names and corresponding weblinks'
mycollections.close()
#parse the page we saved just now
ccc=[]
scj_names_n_weblinks =open("scj_names_n_weblinks.txt","w")
for line in open("mycollections.html"):
	if  line.find('<a href="/collection/')!=-1:
		x=line
		ccc.append(x)

#trim list ccc for info
d = {}
for hang in ccc:
	pattern = re.compile('"(.*)".*>(.*)<')
	res = pattern.search(hang).groups()
	d[res[1]]="www.zhihu.com"+res[0]
	print >> scj_names_n_weblinks,  res[1]+"\n"+d[res[1]]+"\n"
scj_names_n_weblinks.close()
#to save all answers from all scj to one page
Answers =open("Answers.html","w")
for key in d.keys():	
	#.decode('utf8').encode('gbk') this is VERY IMPORTANT in displaying 中文
	print 'now visiting '+u"收藏夹",key.decode('utf8').encode('gbk')+'...'
	print d[key]
	r = s.get("http://"+d[key])	
	print >> Answers , "%s"   % (r.text.encode('utf-8'))
	print "scj "+key.decode('utf8').encode('gbk')+" saved.\n"
Answers.close()
print 'All answers in all your',u"收藏夹",'has now be saved in Answers.html, and it\'s opening...'
os.system("Answers.html")
