#!usr/bin/env python
#-*-coding:utf-8-*-

# list=['<a href="10560150.html" style="">第三百三十七章 玄蛟鳞</a>', <a href="10560131.html" style="">第三百三十六章 周元的实力</a>, <a href="/book/3137/10542706.html" style="">新书感言</a>, <a href="/book/3137/10542714.html" style="">第一章 蟒雀吞龙</a>]
#123344

str = "hello boy<[www.doiido.com]>byebye"
l = str.split("[")[1].split("]")[0]
print(l)