# -*- coding: utf-8 -*-


from celery_app import app
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from celery_app.weather_spider import s
import smtplib


def _format_addr(content):
    name, addr = parseaddr(content)
    return formataddr((Header(name, 'utf-8').encode(),
                       addr))


@app.task
def send():
    from_addr = "example@163.com"
    password = "password"
    to_addr = ["xxxxx@qq.com", "xxxx@qq.com", "xxxxx@sina.com"]
    cc_addr = ["xxxxxxx@hotmail.com"]
    smtp_server = "smtp.163.com"
    msg = MIMEText(u"天气预报结果如下：\n" + s.search(), 'plain', 'utf-8')
    msg['From'] = _format_addr(u'宋冶 <%s>' % from_addr)
    msg['To'] = ",".join(to_addr)
    msg["Cc"] = "xiaoyewise@hotmail.com"
    msg['Subject'] = Header(u'实时天气预报', 'utf-8').encode()
    try:
        server = smtplib.SMTP(smtp_server, 25)
        # server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr + cc_addr, msg.as_string())
        server.quit()
    except Exception as e:
        return e
    return "邮件发送成功！收件人<%s>" % ",".join(to_addr)


if __name__ == '__main__':
    send()
