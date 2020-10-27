# /usr/bin/env python3
# coding=utf8

import sys, os, time, datetime, shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import logging as L
import traceback

L.basicConfig(level=L.DEBUG, format='[%(asctime)s] %(levelname)-8s %(message)s')


"""
function to simplify send email, default smtp is portal.system
"""

__version__ = '1.0'
__revision__ = '$Revision: 1 $'
__all__ = ['send']
__autor__ = "xuchunlong (15701588830@163.com)"


MAIL_SMTP = 'smtp.163.com'
USER = '15701588830@163.com'
PASS = 'PLYZQPQQLZGWYCCJ'


def smtp_send(mail_from, mail_to, subject, content='', attachlist=None, plainletter=True):
    subtype = 'plain' if plainletter else 'html'
    content_msg = MIMEText(content, _subtype=subtype, _charset='utf8')
    if attachlist is None:
        msg = content_msg
    else:
        if isinstance(attachlist, str):
            attachlist = [attachlist]
        msg = MIMEMultipart()
        msg.attach(content_msg)
        for x in attachlist:
            att = MIMEText(open(x, 'rb').read(), 'base64', 'utf8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="%s"' % os.path.basename(x)
            msg.attach(att)
    msg['Subject'] = subject
    if isinstance(mail_from, str):
        msg['From'] = "%s<%s>" % (mail_from.split('@')[0], mail_from)
    else:
        msg['From'] = "%s<%s>" % ( mail_from[0], mail_from[1])
    if isinstance(mail_to, str):
        msg['To'] = mail_to
    else:
        msg['To'] = ';'.join(mail_to)

    try:
        #s = smtplib.SMTP()
        #s.connect(MAIL_SMTP, 25)
        s = smtplib.SMTP_SSL(MAIL_SMTP, 465)
        s.login(USER, PASS)
        s.sendmail(msg['From'], mail_to, msg.as_string())
        print('succ')
        return True
    except Exception:
        print('fail')
        L.info('MAIL_ERR: %s' % traceback.format_exc())
        return False

def test():
    mail_from = (USER)
    mail_to = ['15701588830@163.com']
    '''
    subject = "测试邮件"
    content = "测试正文"
    smtp_send(mail_from, mail_to, subject, content, plainletter=True)
    '''
    subject = "测试邮件"
    content = "<h1>测试正文</h1>"
    smtp_send(mail_from, mail_to, subject, content, attachlist=['test.py'], plainletter=False)


if __name__ == '__main__':
    test()

