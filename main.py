#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Zhihu Like Push
# Code By ivan
#需要自行填写邮箱信息

import sys
import re
import urllib2
import os
import smtplib
import time
import random
from time import strftime
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((\
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def SendSSLEmail(con):
    from_addr = ""       
    pwd = ""                     #密码
    to_addr = ""          #收件人
    smtp_server = "smtp.qq.com"

    msg = MIMEText(con, 'html', 'utf-8')
    msg['From'] = _format_addr(u'一凡的小助手 <%s>' % from_addr)
    msg['To'] = _format_addr(u'一凡 <%s>' % to_addr)
    msg['Subject'] = Header(u'知乎动态推送', 'utf-8').encode()
    
    server = smtplib.SMTP_SSL(smtp_server, 465)
    #server.set_debuglevel(1)
    server.login(from_addr, pwd)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def getHtml(url):
	heads = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
	'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
	'Accept-Language':'zh-cn,zh;q=0.5', 
	'Cache-Control':'max-age=0', 
	'Connection':'keep-alive', 
	'Host':'John', 
	'Keep-Alive':'115', 
	'Referer':url, 
	'User-Agent':'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.14) Gecko/20110221 Ubuntu/10.10 (maverick) Firefox/3.6.14'}
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	urllib2.install_opener(opener) 
	req = urllib2.Request(url)
	opener.addheaders = heads.items()
	respHtml = opener.open(req).read()
	html = respHtml.decode('utf-8')
	return html
def getInfo(html):
    get = re.compile('<span.*?class="zm-profile-setion-time.*?zg-gray.*?zg-right">(.*?)</span>.*?<a.*?class="question_link".*?target="_blank".*?href="(.*?)">(.*?)</a>',re.S)
    result = re.findall(get,html)
    return result
def outcontent(checkdata):
	f = open('./zhihu.txt', 'w')
	f.write(checkdata.encode('hex'))
	f.close()
	return True
def Checkupdate(checkcon):
    q = open('./zhihu.txt', 'r')
    tmpcon = q.read()
    print "读出tmp:" + tmpcon.decode('hex')
    print "传入con:" + checkcon
    if tmpcon == checkcon.encode('hex'):	
        return False
    else:
        return True

def Docheck(checkcon,mailcon):
    if Checkupdate(checkcon):
        outcontent(checkcon)
        SendSSLEmail(mailcon)
        print
        print "！发现变化：发送了一封邮件"
        return True 
    else:
    	print
        print "！没有任何变化" 
        return False


reload(sys)   
sys.setdefaultencoding('utf8')  
outcontent("")
while True:
    hash = ("https://m.zhihu.com/people/ivangeek","https://www.zhihu.com/people/ivangeek") #这里自行更改
    a =random.choice(hash)
    print a
    html = getHtml(a)
    data = getInfo(html)
    checkcon = data[0][2]
    print "【" + time.strftime('%Y-%m-%d %H:%M:%S') + "】"   
    print "当前话题：" + checkcon
    print
    mailcon =""
    for item in data:
        mailcon = mailcon + item[2] + "<br />"
        mailcon = mailcon + "http://www.zhihu.com" + item[1] + "<br />"
        mailcon = mailcon + item[0] + "<br />"    
    Docheck(checkcon,mailcon)
    print
    time.sleep(5)
