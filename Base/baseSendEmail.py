from datetime import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fileinput import filename

from Base.basePath import BasePath as BP
from Base.baseUtils import read_config_ini,make_zip

class HandleEmail():

    def __init__(self):
        config = read_config_ini(BP.CONFIG_FILE)
        email_config = config['邮件发送配置']
        self.host = email_config['host']
        self.port = int(email_config['port'])
        self.sender = email_config['sender']
        self.send_email = email_config['send_email']
        self.receive_email = eval(email_config['receive_email'])
        self.pwd = email_config['pwd']
        self.subject = email_config['subject']

    # 添加文本
    def add_text(self,text):
        return MIMEText(text,'plain','utf-8')

    # 添加html文本
    def add_hmml(self,html):
        return MIMEText(html,'html','utf-8')

    # 添加附件，图片，txt,pdf,zip
    def add_accessory(self,filepath):
        res = MIMEText(open(filepath,'rb').read(),'base64','utf-8')
        res.add_header('Content-Disposition','attachment',filename=os.path.basename(filepath))
        return res

    # 添加主题 发件人 收件人
    def add_subject_attach(self,attach_info:tuple,send_date=None):
        msg = MIMEMultipart('mixed')
        msg['Subject'] = self.subject
        #
        msg['From'] = self.send_email
        msg['To'] = ';'.join(self.receive_email)
        if send_date:
            msg['Date'] = send_date
        else:
            msg['Date'] = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
        if isinstance(attach_info,tuple):
            for i in attach_info:
                msg.attach(i)
        return msg

    # 发送邮件
    def send_email_oper(self,msg):
        smtp = None
        try:
            smtp = smtplib.SMTP(self.host, port=self.port)
            smtp.login(self.send_email, self.pwd)
            smtp.sendmail(self.send_email, self.receive_email, msg.as_string())
            print("{0}给{1}发送邮件成功！发送时间为：{2}".format(self.send_email,self.receive_email,datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')))
        except Exception as e:
            if smtp:
                smtp.quit()
            smtp = smtplib.SMTP_SSL(self.host,port=self.port)
            smtp.login(self.send_email,self.pwd)
            smtp.sendmail(self.send_email,self.receive_email,msg.as_string())
            print("{0}给{1}发送邮件成功！发送时间为：{2}".format(self.send_email,self.receive_email,datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')))
        finally:
            if smtp:
                smtp.quit()


    def send_public_email(self,send_date=None,text='',html='',filetype='HTML'):
        '''邮件发送公共方法'''
        attache_info = []
        text_plain = self.add_text(text=text)
        attache_info.append(text_plain)
        if html:
            text_html = self.add_html_text(html=html)
            attache_info.append(text_html)
        elif filetype == 'ALLURE':
            allure_zip = make_zip(BP.ALLURE_REPORT_PATH,os.path.join(BP.ALLURE_REPORT_PATH,'allure.zip'))
            file_attach = self.add_accessory(filepath=allure_zip)
            attache_info.append(file_attach)
        elif filetype == 'HTML':
            file_attach = self.add_accessory(filepath=os.path.join(BP.HTML_PATH,'auto_reports.html'))
            attache_info.append(file_attach)
        elif filetype == 'XML':
            file_attach = self.add_accessory(filepath=os.path.join(BP.XML_PATH,'auto_reports.xml'))
            attache_info.append(file_attach)
        # 添加主题和附件信息到msg
        attache_info = tuple(attache_info)
        msg = self.add_subject_attach(attach_info=attache_info,send_date=send_date)
        # 发送邮件
        self.send_email_oper(msg)

if __name__ == '__main__':
    text = '本邮件由系统自动发出，无需回复：\n各位同事，大家好，以下为本次测试报告！'
    HandleEmail().send_public_email(send_date=None,text=text,html='',filetype='HTML')