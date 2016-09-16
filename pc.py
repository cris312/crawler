#!/usr/bin/python
import urllib2
import urllib
import re
import os
import csv
dat = {}
class PC:
	def __init__(self,baseUrl):
		self.baseURL = baseUrl
		self.tool = Tool()
	def getPage(self,pageNum):
		try:
			url = self.baseURL + str(pageNum)
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			#print response.read()
			return response.read().decode('utf-8')
		except urllib2.URLError,e:
			if hasattr(e,"reason"):
				print e.reason
				return None
	def getContent(self,pageNum):
		page = self.getPage(pageNum)
		pattern = re.compile('<tr class="table-link.*?>(.*?)</tr>',re.S)
		result = re.findall(pattern,page)
		if result:
			#x = self.tool.replace(result[0])
			#print x.strip()
			return result
		else:
			return None
	def getData(self,result):
		reLen = len(result)
		pattern = re.compile('<td class="">(.*?)</td>',re.S)
		k = 0
		for i in range(0,reLen):
			d = re.findall(pattern,result[i])
			dat[k]={"Filing_Name":d[0],"Filing_Date":d[1],"District_Court":d[2],"Exchange":d[3],"Ticker":d[4]}
			k += 1
		num = k
		return dat
class Tool:
	removeTd = re.compile('<td class="">|</td>')
	def replace(self,x):
		x = re.sub(self.removeTd,"",x)
		return x
baseUrl = 'http://securities.stanford.edu/filings.html?page='
pc = PC(baseUrl)
csvfile = file('aa.csv','wb')
writer = csv.writer(csvfile)
for i in range(1,214):
	print i
	res = pc.getContent(i)
	da = pc.getData(res)
	if (len(da)!=0):
		for k in range(0,len(da)):
			writer.writerow([(dat[k]["Filing_Name"]).strip(),(dat[k]["Filing_Date"]).strip(),(dat[k]["District_Court"]).strip(),(dat[k]['Exchange']).strip(),(dat[k]['Ticker']).strip()])
	#print k
	#print (dat[k]["Filing_Name"]+" ").strip()
	#print (dat[k]["Filing_Date"]+" ").strip()
	#print (dat[k]["District_Court"]+" ").strip()
	#print (dat[k]['Exchange']+" ").strip()
	#print (dat[k]['Ticker']+" ").strip()
	#print "\n"
csvfile.close()
