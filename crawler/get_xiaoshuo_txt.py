#!usr/bin/env python
#-*-coding:utf-8-*-
import requests,re,time,os
from bs4 import BeautifulSoup

#小说下载函数
#id：小说编号
#txt字典项介绍
# title：小说题目
# first_page：第一章页面
# txt_section：章节地址
# section_name：章节名称
# section_text：章节正文
# section_ct：章节页数
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
# req_url_base='http://www.qu.la/book/'           #小说主地址
req_url_base='http://www.biquge.com.tw/'
def get_txt(txt_id):
    txt={}
    txt['title']=''
    txt['id']=str(txt_id)
    try:
        print("请输入需要下载的小说编号：")
        txt['id']=input()
        req_url=req_url_base+ txt['id']+'/'                        #根据小说编号获取小说URL
        print("小说编号："+txt['id'])
        res=requests.get(req_url,params=req_header)             #获取小说目录界面
        soups=BeautifulSoup(res.text,"html.parser")           #soup转化
        #获取小说题目
        txt['title']=soups.select('#wrapper .box_con #maininfo #info h1')[0].text
        txt['author']=soups.select('#wrapper .box_con #maininfo #info p')
        #获取小说最近更新时间
        txt['update']=txt['author'][2].text
        #获取最近更新章节名称
        txt['lately'] = txt['author'][3].text
        #获取小说作者
        txt['author']=txt['author'][0].text
        #获取小说简介
        txt['intro']=soups.select('#wrapper .box_con #maininfo #intro')[0].text.strip()
        print("编号："+'{0:0>8}   '.format(txt['id'])+  "小说名：《"+txt['title']+"》  开始下载。")
        print("正在寻找第一章页面。。。")
        #获取小说所有章节信息
        first_page=soups.select('#wrapper .box_con #list dl dd a')
        print(first_page[0]['href'])
        #获取小说总章页面数
        section_ct=len(first_page)
        print("小说章节数：" + str(section_ct))
        #获取小说第一章页面地址
        first_page = first_page[0]['href'].split('/')[2]
        print("第一章地址寻找成功："+ first_page)
        #设置现在下载小说章节页面
        txt_section=first_page
        #打开小说文件写入小说相关信息
        fo = open('{0:0>8}-{1}.txt.download'.format(txt['id'],txt['title']), "ab+")
        fo.write((txt['title']+"\r\n").encode('UTF-8'))
        fo.write((txt['author'] + "\r\n").encode('UTF-8'))
        fo.write((txt['update'] + "\r\n").encode('UTF-8'))
        fo.write((txt['lately'] + "\r\n").encode('UTF-8'))
        fo.write(("*******简介*******\r\n").encode('UTF-8'))
        fo.write(("\t"+txt['intro'] + "\r\n").encode('UTF-8'))
        fo.write(("******************\r\n").encode('UTF-8'))
        #进入循环，写入每章内容
        while(1):
            try:
                #请求当前章节页面
                r=requests.get(req_url+str(txt_section),params=req_header)
                #soup转换
                soup=BeautifulSoup(r.text,"html.parser")
                #获取章节名称
                section_name=soup.select('#wrapper .content_read .box_con .bookname h1')[0]
                section_text=soup.select('#wrapper .content_read .box_con #content')[0]
                for ss in section_text.select("script"):   #删除无用项
                    ss.decompose()
                #获取章节文本
                section_text=re.sub( '\s+', '\r\n\t', section_text.text).strip('\r\n')#
                print(section_text)
                #获取下一章地址
                txt_section=soup.select('#wrapper .content_read .box_con .bottem2 #A3')[0]['href']
                #判断是否最后一章，当为最后一章时，会跳转至目录地址，最后一章则跳出循环
                if(txt_section=='./'):
                    print("编号："+'{0:0>8}   '.format(txt['id'])+  "小说名：《"+txt['title']+"》 下载完成")
                    break
                #以二进制写入章节题目
                fo.write(('\r'+section_name.text+'\r\n').encode('UTF-8'))
                #以二进制写入章节内容
                fo.write((section_text).encode('UTF-8'))
                print(txt['title']+' 章节：'+section_name.text+'     已下载')
                #print(section_text.text.encode('UTF-8'))
            except:
                print("编号："+'{0:0>8}   '.format(txt['id'])+  "小说名：《"+txt['title']+"》 章节下载失败，正在重新下载。")
        fo.close()
        os.rename('{0:0>8}-{1}.txt.download'.format(txt['id'],txt['title']), '{0:0>8}-{1}.txt'.format(txt['id'],txt['title']))
    except:     #出现错误会将错误信息写入dowload.log文件，同时答应出来
        fo_err = open('dowload.log', "ab+")
        try:
            fo_err.write(('['+time.strftime('%Y-%m-%d %X', time.localtime())+"]：编号：" + '{0:0>8}   '.format(txt['id']) + "小说名：《" + txt['title'] + "》 下载失败。\r\n").encode('UTF-8'))
            print('['+time.strftime('%Y-%m-%d %X', time.localtime())+"]：编号："+'{0:0>8}   '.format(txt['id'])+  "小说名：《"+txt['title']+"》 下载失败。")
            os.rename('{0:0>8}'.format(txt['id']) + '-' + txt['title'] + '.txt.download',
                  '{0:0>8}'.format(txt['id']) + '-' + txt['title'] + '.txt.error')
        except:
            fo_err.write(('['+time.strftime('%Y-%m-%d %X', time.localtime())+"]：编号："+'{0:0>8}   '.format(txt['id'])+"下载失败。\r\n").encode('UTF-8'))
            print('['+time.strftime('%Y-%m-%d %X', time.localtime())+"]：编号："+'{0:0>8}   '.format(txt['id'])+"下载失败。")
        finally: #关闭文件
            fo_err.close()

get_txt(3353)