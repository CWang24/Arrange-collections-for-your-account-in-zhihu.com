#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -- coding: utf-8 --
import requests
import re
import os
email = raw_input("Enter your email address: ");
password = raw_input("Enter your password: ");
s = requests.session()
login_data = {'email': email, 'password': password}

s.post('http://www.zhihu.com/login', login_data)
print u"访问您的收藏夹首页中..."
r = s.get('http://www.zhihu.com/collections/mine')
mycollections =open("mycollections.html","w")
print >> mycollections , "%s"   % (r.text.encode('utf-8'))
print u"首页已保存。开始分析所有收藏夹",'...\n'
mycollections.close()

#parse the page we saved just now to get weblinks of collections
ccc=[]
for line in open("mycollections.html"):
	if  line.find('<a href="/collection/')!=-1:
		x=line
		ccc.append(x)

#trim list ccc for info
collection_links = {}
for hang in ccc:
	pattern = re.compile('"(.*)".*>(.*)<')
	res = pattern.search(hang).groups()
	collection_links[res[1]]="www.zhihu.com"+res[0]


tt_answer_count=0
tt_question_count=0
Answers =open("Answers.html","w")
for key in collection_links.keys():
	#逐个访问收藏夹
	question_count=0
	answer_count=0
	#.decode('utf8').encode('gbk') this is VERY IMPORTANT in displaying 中文
	print u"正在访问收藏夹",key.decode('utf8').encode('gbk')+'...'
	# print 'Address is:',collection_links[key]
	r = s.get("http://"+collection_links[key])	
	print >> Answers , "%s"   % (r.text.encode('utf-8'))
	#看看该收藏夹第一页有多少q和a
	content=r.text.encode('utf-8')
	question_count = content.count('zm-item-title')
	answer_count = content.count('/answer/content')
	print u"本页共有",answer_count,u"个答案以及",question_count,u"个问题"
	tt_answer_count=tt_answer_count+answer_count
	tt_question_count=tt_question_count+question_count
	#判断该收藏夹有多少页
	pattern = re.compile('\?page=(\d)')
	res = re.findall(pattern, content)
	if res:#含有多页
		# print res
		n=int(res[-2])
		print u"该收藏夹共有",n,u"页"
		pagescount=range(n+1)
		pagescount.pop(0)
		pagescount.pop(0)
		# print pagescount
		
		for page in pagescount:
			page_str=str(page)
			r = s.get("http://"+collection_links[key]+'?page='+page_str)#从第二页起每一页的地址
			print u"第"+page_str+u"页..."
			print >> Answers , "%s"   % (r.text.encode('utf-8'))
			#再次统计q和a个数
			content=r.text.encode('utf-8')
			question_count = content.count('zm-item-title')
			answer_count = content.count('/answer/content')
			print u"本页共有",answer_count,u"个答案以及",question_count,u"个问题"
			tt_answer_count=tt_answer_count+answer_count
			tt_question_count=tt_question_count+question_count
				
	print u"收藏夹",key.decode('utf8').encode('gbk'),u"已保存。",' \n'
Answers.close()
print u"您迄今为止总共收藏了",tt_question_count,u"个问题，以及",tt_answer_count,u"个答案"
print u"它们以及全部保存在了文件Answers.html中"
