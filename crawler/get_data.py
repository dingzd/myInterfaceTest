#!usr/bin/env python
#-*-coding:utf-8-*-
from urllib import request
import chardet
import re,pymysql

def getList():
    url = "http://www.quanshuwang.com/book/9/9055"
    response = request.urlopen(url)
    html = response.read()
    charset = chardet.detect(html)
    text = html.decode(charset['encoding'])
    # print(text)
    reg = r'<li><a href="(.*?)" title=".*?">(.*?)</a></li>'
    reg = re.compile(reg)
    urllist = re.findall(reg,text)
    return  urllist
# print(getList())
def getContent(url):
    response = request.urlopen(url)
    html = response.read()
    text = html.decode('gbk')
    # print(text)
    reg = r'style5\(\);</script>((?:.|\n)*?)<script type="text/javascript">style6'
    reg = re.compile(reg)
    # print(re.findall(reg,text)[0])
    return re.findall(reg,text)[0]
    # print(content)

class BookDB:
    def __init__(self):
        self.conn = pymysql.connect("127.0.0.1","root","dingzd123","xiaoshuo")

    def select(self,sql):
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            return result
        except Exception as e:
            print(e)

    def insert(self,title,content):
        cur = self.conn.cursor()
        cur.execute("inset into daomubiji values(null,'%s','%s')" %(title,content))
        cur.close()
        self.conn.commit()

# if __name__=='__main__':
#     mydb = BookDB()
#     sql = "select * from daomubiji"
#     mydb.select(sql)

m=0
while m<5:
    for i in getList():
        title = i[1]
        content = getContent(i[0])
        # print(content)
        with open("daomubiji.txt",'w') as f:
            f.write('\r'+title+'\r\n')
            f.write(content)
            f.close()
        # mydb=BookDB()
        # mydb.insert(title,content)
    m=m+1




