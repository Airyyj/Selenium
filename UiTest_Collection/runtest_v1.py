# -*-coding:utf-8-*-
# Time:2017/7/1-0:18
# Author:YangYangJun
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import smtplib
import unittest
import time
from HTMLTestRunner import HTMLTestRunner
from email.header import Header
from email.mime.text import MIMEText
import baseinfo
from email.mime.multipart import MIMEMultipart

from selenium import webdriver


def get_Result(filename):
    driver = webdriver.Firefox()
    driver.maximize_window()
    ##得到测试报告路径
    result_url = "file://%s" % filename
    driver.get(result_url)
    time.sleep(5)
    result = driver.find_element_by_xpath("html/body/div[1]/p[3]").text
    result = result.split(':')
    driver.quit()
    return  result[-1]



def send_Mail(file_new,result):
    f = open(file_new, 'rb')
    # 读取测试报告正文
    mail_body = f.read()
    f.close()
    try:
        smtp = smtplib.SMTP(baseinfo.Smtp_Server, 25)
        sender = baseinfo.Smtp_Sender
        password = baseinfo.Smtp_Sender_Password
        receiver = baseinfo.Smtp_Receiver
        smtp.login(sender, password)
        msg = MIMEMultipart()
        # 编写html类型的邮件正文，MIMEtext()用于定义邮件正文
        # 发送正文
        text = MIMEText(mail_body, 'html', 'utf-8')
        text['Subject'] = Header('未名企鹅UI自动化测试报告', 'utf-8')
        msg.attach(text)
        # 发送附件
        # Header()用于定义邮件标题
        msg['Subject'] = Header('[执行结果：' + result + ']'+ '未名企鹅UI自动化测试报告' + now, 'utf-8')
        msg_file = MIMEText(mail_body, 'html', 'utf-8')
        msg_file['Content-Type'] = 'application/octet-stream'
        msg_file["Content-Disposition"] = 'attachment; filename="TestReport.html"'
        msg.attach(msg_file)
        # 定义发件人，如果不写，发件人为空
        msg['From'] = sender
        # 定义收件人，如果不写，收件人为空
        msg['To'] = ",".join(receiver)
        tmp = smtp.sendmail(sender, receiver, msg.as_string())
        print tmp
        smtp.quit()
        return True
    except smtplib.SMTPException as e:
        print(str(e))
        return False


if __name__ == '__main__':
    # 测试用例路径
    test_dir = baseinfo.test_dir
    # 测试报告存放路径
    report_dir = baseinfo.test_report

    test_discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py')
    now = time.strftime("%Y-%m-%d-%H_%M_%S")
    filename = report_dir + 'result-' + now + '.html'
    print filename
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp, title='未名企鹅UI自动化测试报告', description='用例执行情况')
    runner.run(test_discover)
    fp.close()
    result = get_Result(filename)

    mail = send_Mail(filename,result)
    if mail:
        print("发送成功！")
    else:
        print("发送失败！")



