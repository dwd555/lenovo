import requests,threading
from bs4 import BeautifulSoup
import time,json
import pymysql

def getInfo(url):
	conn = pymysql.connect(host='localhost',user='root',passwd='',db='notebook',port=3306,charset='utf8')
	cursor = conn.cursor()
	title=""
	ttm=""
	flash=""
	flashType=""
	cpu=""
	ScreenResolution=""
	os=""
	gpu=""
	disk=""
	gpuMemory=""
	notebookDetail={}
	detailUrl=url.replace(".html","_detail.html")
	reg=requests.get(detailUrl)
	soup=BeautifulSoup(reg.text,"html.parser")
	title=soup.select(".main .box .mark")[0].get_text()
	notebookDetail["title"]=title
	timeToMarket=soup.select(".box .out a")
	details=soup.select("tbody th")
	for i in details:
		data=i.next_sibling.next_sibling.a
		if data:
			notebookDetail[i.get_text()]=data.get_text()
			if i.get_text()=="上市时间":
				ttm=data.get_text()
			if i.get_text()=="内存容量":
				flash=data.get_text()
			if i.get_text()=="内存类型":
				flashType=data.get_text()
			if i.get_text()=="处理器":
				cpu=data.get_text()
			if i.get_text()=="分辨率":
				ScreenResolution=data.get_text()
			if i.get_text()=="操作系统":
				os=data.get_text()
			if i.get_text()=="显卡芯片":
				gpu=data.get_text()
			if i.get_text()=="硬盘容量":
				disk=data.get_text()
			if i.get_text()=="显存容量":
				gpuMemory=data.get_text()

	try:
		cursor.execute('INSERT INTO `lenovo` (`id`,`title`,`ttm`,`flash`,`flashType`,`cpu`,`ScreenResolution`,`os`,`gpu`,`disk`,`gpuMemory`) values (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' ,[title,ttm,flash,flashType,cpu,ScreenResolution,os,gpu,disk,gpuMemory])
		conn.commit()
	except:
		conn.rollback()
	conn.close()				


for j in range(0,34):
	url="http://product.pconline.com.cn/notebook/lenovo/"
	if j>0:
		url="http://product.pconline.com.cn/notebook/lenovo/"+str(j*25)+"s1.shtml"
	reg=requests.get(url)
	soup=BeautifulSoup(reg.text,"html.parser")
	tags=soup.find_all("a",class_="item-title-name")
	for i in tags:
		threading.Thread(target=getInfo,args=(i["href"],)).start()
