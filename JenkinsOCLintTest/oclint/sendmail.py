#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr
import smtplib
import sys
import os

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

file_name=sys.argv[1]
current_time=sys.argv[2]
password=sys.argv[3]

htmlf=open(file_name,'r')
htmlcont=htmlf.read()

from_addr = 'mademaorobot@163.com'
server_host = 'smtp.163.com'
to_addr = ['ismademao@gmail.com']

msg = MIMEMultipart()
msg['From'] = _format_addr(u'%s' % from_addr)
to = ','.join(to_addr)
msg['To'] = to
msg['Subject'] = Header(u'OCLint检测报告' + current_time, 'utf-8').encode()

msg.attach(MIMEText(htmlcont, 'html', 'utf-8'))

# 添加附件就是加上一个MIMEBase，从本地读取一个图片:
with open(file_name, 'rb') as f:
    # 设置附件的MIME和文件名，这里是png类型:
    mime = MIMEBase('application', 'octet-stream', filename=file_name)
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename=file_name)
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)

server = smtplib.SMTP(server_host)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, to_addr, msg.as_string())
server.quit()
