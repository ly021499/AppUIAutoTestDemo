#!/usr/bin/python
import os
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from core.read_config import config
from core.config_log import logger
from smtplib import SMTP


class ConfigEmail(object):

    """
    1. 导入邮件所需模块
    2. 定义邮箱头部
    3. 定义邮箱附件
    4. 获取最新的报告
    5. 写入附件
    6.发送邮件
    """

    def __init__(self):
        self.username = config.get_email("username")
        self.password = config.get_email("password")
        self.host = config.get_email("host")
        self.content = config.get_email("content")
        self.subject = config.get_email("subject")
        self.reciever = config.get_email("reciever")
        self.filename = config.get_email("filename")
        self.mmp = MIMEMultipart()
        self.smtp = SMTP()

    def email_header(self):
        """
        定义邮件头部信息
        :return:
        """
        self.mmp["From"] = self.username
        self.mmp["To"] = self.reciever
        self.mmp["subject"] = self.subject

    def email_attachment(self):
        """
        定义邮件附件
        :return:
        """
        list_dir = os.listdir(config.REPORT_DIR)
        # 根据文件的修改时间进行排序
        list_dir.sort(key=lambda x: os.path.getmtime(config.REPORT_DIR + "\\" + x))
        # 构建文件路径，-1代表最新时间的文件
        att_file_path = os.path.join(config.REPORT_DIR, list_dir[-1])
        att_file = MIMEApplication(open(att_file_path, 'rb').read())
        att_file.add_header('Content-Disposition', 'attachment', filename=self.filename)
        self.mmp.attach(att_file)

    def email_content(self):
        """
        定义邮件正文
        :return:
        """
        content = MIMEText(self.content, _charset="utf-8")
        self.mmp.attach(content)

    def send_email(self):
        """
        发送邮件步骤：
        1.连接邮件服务器
        2.登录邮箱
        3.传入邮箱文本内容
        4.发送邮件
        5.关闭smtp连接
        :return:
        """

        # 调用方法添加各项信息
        self.email_header()
        self.email_content()
        self.email_attachment()

        try:
            self.smtp.connect(self.host)
            self.smtp.login(self.username, self.password)
            self.smtp.sendmail(self.username, self.reciever, self.mmp.as_string().encode())
            logger.info("biubiubiu!!!~~~  导弹发射成功!@#$%  颤抖吧~~~  *&^%愚蠢的人类")
        except Exception as e:
            logger.error("警告警告：// 导弹未进入指定发射轨道，赶紧抢救，否则你家要炸了啊~~~\n 错误信息：{}".format(e))

        finally:
            self.smtp.quit()


if __name__ == '__main__':
    ce = ConfigEmail()
    ce.send_email()
