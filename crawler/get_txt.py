#!usr/bin/env python
#-*-coding:utf-8-*-
import requests
import threading,re
from bs4 import BeautifulSoup

#请求头字典
req_header={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate,br',
'Accept-Language':'zh-CN,zh;q=0.9,zh-TW;q=0.8',
'Cookie':'UM_distinctid=1627ff7ce8f30-007b85df11fcdb-3e3d560e-100200-1627ff7ce906c; CNZZDATA1261736110=177590318-1522562603-https%253A%252F%252Fblog.csdn.net%252F%7C1522562603; cscpvrich8662_fidx=1; cscpvrich8669_fidx=1; twtext_10490=1; 91turn_10489=1; bookid=1; bcolor=; font=; size=; fontcolor=; width=; Hm_lvt_5ee23c2731c7127c7ad800272fdd85ba=1522565370,1522565740,1522566114,1522566665; tanwanhf_10487=2; tanwanhf_10484=2; tanwanhf_10485=2; tanwanhf_10486=2; Hm_lpvt_5ee23c2731c7127c7ad800272fdd85ba=1522566669; PPad_id_PP=2; tanwanpf_10488=2; tanwanpf_10483=2; chapterid=260824; chaptername=%25u8BB8%25u7ACB%25u56FD%25u5916%25u4F20',
'Host':'www.qu.la',
'Connection':'keep-alive',
'Referer':'https://www.qu.la/book/1/260824.html',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
}
req_url_base='http://www.qu.la/book/'           #小说主地址
req_url=req_url_base+"1/"                       #单独一本小说地址
txt_section='260824.html'                       #某一章页面地址

#请求当前章节页面  params为请求参数
r=requests.get(req_url+str(txt_section),params=req_header)
#soup转换
soup=BeautifulSoup(r.text,"html.parser")
#获取章节名称
section_name=soup.select('#wrapper .content_read .box_con .bookname h1')[0].text
#获取章节文本
section_content=soup.select('#wrapper .content_read .box_con #content')[0]
for ss in section_content('script'):                #删除无用项
    ss.decompose()
section_text=section_content.text
#按照指定格式替换章节内容，运用正则表达式
section_text=re.sub( '\s+', '\r\n\t', section_text).strip('\r\n')
print('章节名:'+section_name)
print("章节内容：\n"+section_text)

fo = open('1.txt', "ab+")         #打开小说文件
# 以二进制写入章节题目 需要转换为utf-8编码，否则会出现乱码
fo.write(('\r' + section_name + '\r\n').encode('UTF-8'))
# 以二进制写入章节内容
fo.write((section_text).encode('UTF-8'))
fo.close()        #关闭小说文件