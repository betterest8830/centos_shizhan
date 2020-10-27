# /usr/bin/env python3
# coding=utf8

import os
import sys
import datetime

import smtp_send


mail_from = ('15701588830@163.com')
mail_to = ['15701588830@163.com']


def load_css():
    css = '''
        body{margin:0; font-family:Tahoma;Simsun;font-size:12px;}
        table{border:1px #E1E1E1 solid;}
        td{border:1px #E1E1E1 solid;}
        th{border:1px #E1E1E1 solid;}
        .title {font-size: 12px; COLOR: #FFFFFF; background-color:#3592D1;font-family: Tahoma; text-align:center;}
        .success {font-size: 12px; COLOR:#000000; background-color:#FFFFFF; font-family: Tahoma; text-align:center;}
        .warning {font-size: 12px; COLOR:#FFFFFF; background-color:#FFFFFF; font-family: Tahoma; text-align:center;}
        .error {font-size: 12px; COLOR:#FFFFFF; background-color:#F23E3E; font-family: Tahoma; text-align:center;}
    '''
    return css


def send_report(task_name, task_addr):
    title = task_name
    time_str = datetime.datetime.now().strftime('[%Y-%m-%d]')
    css = load_css()
    mail_title = time_str +  title
    content = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
    content += '<html lang="utf8"" xmlns="http://www.w3.org/1999/xhtml">'
    content += '<head>'
    content += '<title>' + title + '</title>'
    content += '<style type="text/css">' + css + '</style>'
    content += '<meta http-equiv="Content-Type" content="text/html; charset=utf8" />'
    content += '</head>'
    content += '<h1>' + mail_title + '</h1>'
    content += '<div>脚本位置：' + task_addr + '</div>'
    content += '</br>'
    content += '</body>'
    r = smtp_send.smtp_send(mail_from, mail_to, mail_title, content, attachlist=None, plainletter=False)


if __name__ == '__main__':
    task_name, task_addr = sys.argv[1], sys.argv[2]
    send_report(task_name, task_addr)
