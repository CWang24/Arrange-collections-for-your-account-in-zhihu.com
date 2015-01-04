#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import os
print u"请先登陆知乎"
email = raw_input('输入注册邮箱地址: '.decode('utf-8').encode('gbk'))
password = raw_input('输入密码: '.decode('utf-8').encode('gbk'))
s = requests.session()
login_data = {'email': email, 'password': password}
print u"访问您的收藏夹首页中..."
s.post('http://www.zhihu.com/login', login_data)
r = s.get('http://www.zhihu.com/collections/mine')
mycollections =open("mycollections.html","w")
print >> mycollections , "%s"   % (r.text.encode('utf-8'))

mycollections.close()

#parse the page we saved just now to get weblinks of collections
ccc=[]
for line in open("mycollections.html"):
	if  line.find('<a href="/collection/')!=-1:
		x=line
		ccc.append(x)
if ccc:
	print u"首页已保存。开始分析所有收藏夹",'...\n'

		
	#trim list ccc for info
	collection_links = {}
	for hang in ccc:
		pattern = re.compile('"(.*)".*>(.*)<')
		res = pattern.search(hang).groups()
		collection_links[res[1]]="www.zhihu.com"+res[0]
		#每个收藏夹首页地址已存入哈希数组中

	tt_answer_count=0
	tt_question_count=0
	Answers =open("Answers.html","w")
	head='''<html lang="zh-CN" dropEffect="none" class="no-js ">
	<head>
	<meta charset="utf-8" />
	<title>所有收藏夹问题整合</title>
	</head>
	<body>'''
	print >> Answers,head

	for key in collection_links.keys():
		#逐个访问收藏夹
		question_count=0
		answer_count=0
		#.decode('utf8').encode('gbk') this is VERY IMPORTANT in displaying 中文
		print u"正在访问收藏夹",key.decode('utf8').encode('gbk')+'...'
		scjhead='''<hr style="height:3px;border:none;border-top:1px solid orange">
	<p>
	<a style="font-family:verdana;font-size:100%;color:black"><b>'''
		print >> Answers,scjhead
		print >> Answers,key	
		scjname_qlink='''</b></a>
	</p>
	<hr style="height:3px;border:none;border-top:1px dashed red">

	<p style="font-family:verdana;font-size:100%;color:blue">
	<a href="http://www.zhihu.com'''
		print >> Answers,scjname_qlink
		
		#print 问题链接
		r = s.get("http://"+collection_links[key])	
		content=r.text.encode('utf-8')
		
		
		content_lines=content.split('\n')
		flag=0
		for hang in content_lines:
			#若该行含有问题内容
			pattern = re.compile("zm-item-title.*(\/question\/\d*)..(.*)<\/a>")
			m=re.findall(pattern,hang)
			if m:
				res = pattern.search(hang).groups()
				print >> Answers, '<p style="font-family:verdana;font-size:90%;color:blue">'
				print >> Answers, '<a href="http://www.zhihu.com'+res[0]+'"style="text-decoration:none">'
				print >> Answers, '<b>'+res[1]+'</b></a></p>'
				
			#打印赞同票数
			pattern = re.compile('zm-item-vote-count.*">(\d*)<')
			res = re.findall(pattern,hang)
			zantong='''赞同  From '''
			if res:
				print >> Answers,'<p style="font-family:verdana;font-size:90%;color:black">'+res[0]+zantong
			#找作者
			pattern = re.compile('data-tip.*href="(\/people\/.*?<\/a>)')
			res = re.findall(pattern,hang)
			if res:
				
				print >> Answers, '<a href="http://www.zhihu.com'+res[0]+'</p>'
			
			if '</h3></div>' in hang:
				print >> Answers,'nimingyonghu </p>'
			#打印答案摘要及显示全部完整链接
			if flag == 1:
				
				if 'href="/question/' in hang:
					
					flag=0
					pattern = re.compile('href="(\/question\/.*<\/a>)')
					res = re.findall(pattern,hang)
					if res:
						print >> Answers,'<a href="http://www.zhihu.com'+res[0]
						print >> Answers,'<br><br>'
				if '</div>' in hang:
					flag=0
					print >> Answers,'<br><br>'
			if 'zh-summary' in hang:
				flag=1	
			if flag == 1:
				print >> Answers,hang
		
		
		#看看该收藏夹第一页有多少q和a
		content=r.text.encode('utf-8')
		question_count = content.count('<h2 class="zm-item-title"><a target="_blank" href="/question/')
		answer_count = content.count('/answer/content')
		print u"本页共有",answer_count,u"个答案",question_count,u"个问题"
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
				content=r.text.encode('utf-8')
				content_lines=content.split('\n')
				
				for hang in content_lines:
					
					#先找问题
					pattern = re.compile("zm-item-title.*(\/question\/\d*)..(.*)<\/a>")
					m=re.findall(pattern,hang)
					if m:
						res = pattern.search(hang).groups()
						print >> Answers, '<p style="font-family:verdana;font-size:90%;color:blue">'
						print >> Answers, '<a href="http://www.zhihu.com'+res[0]+'"style="text-decoration:none">'
						print >> Answers, '<b>'+res[1]+'</b></a></p>'
					
					#打印赞同票数
					pattern = re.compile('zm-item-vote-count.*">(\d*)<')
					res = re.findall(pattern,hang)
					zantong='''赞同  From '''
					if res:
						print >> Answers,'<p style="font-family:verdana;font-size:90%;color:black">'+res[0]+zantong
					#找作者
					pattern = re.compile('data-tip.*href="(\/people\/.*?<\/a>)')
					res = re.findall(pattern,hang)
					if res:
						
						print >> Answers, '<a href="http://www.zhihu.com'+res[0]+'</p>'
					
					if '</h3></div>' in hang:
						print >> Answers,'nimingyonghu </p>'		
					
					
					#打印答案摘要
					if flag == 1:
						
						if 'href="/question/' in hang:
							#此处有待处理链接信息
							flag=0
							pattern = re.compile('href="(\/question\/.*<\/a>)')
							res = re.findall(pattern,hang)
							if res:
								print >> Answers,'<a href="http://www.zhihu.com'+res[0]
								print >> Answers,'<br><br>'
						if '</div>' in hang:
							flag=0
							print >> Answers,'<br><br>'
					if 'zh-summary' in hang:
						flag=1	
					if flag == 1:
						print >> Answers,hang
				
				#再次统计q和a个数
				content=r.text.encode('utf-8')
				question_count = content.count('<h2 class="zm-item-title"><a target="_blank" href="/question/')
				answer_count = content.count('/answer/content')
				print u"本页共有",answer_count,u"个答案",question_count,u"个问题"
				tt_answer_count=tt_answer_count+answer_count
				tt_question_count=tt_question_count+question_count
					
		print u"收藏夹",key.decode('utf8').encode('gbk'),u"已保存。",' \n'

	jiewei='''<hr style="height:2px;border:none;border-top:4px double red">
	<p align="center">
	Author: C,Wang<br>
	Find me here: https://github.com/CWang24
	</p>
	</div>
	</body>
	</html>'''
	print >> Answers ,jiewei
	Answers.close()
	print u"您迄今为止总共收藏了",tt_question_count,u"个问题，以及",tt_answer_count,u"个答案"
	print u"它们已全部保存在了文件Answers.html中"
	zz = raw_input('打开Answers.html请输入y并回车，退出请直接回车'.decode('utf-8').encode('gbk'))
	if zz == 'y':
		os.system('Answers.html')
else:
	zz = raw_input('账号信息输入有误，请关闭程序后打开重试。'.decode('utf-8').encode('gbk'))
