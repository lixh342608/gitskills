#coding=utf-8
'''
Created on 2017年6月18日

@author: Administrator
'''
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart  
from email.utils import parseaddr, formataddr
from email.mime.base import MIMEBase

import smtplib,os

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
class sendmeil:
    def __init__(self,_file):
        self._file=_file
        self.filename=os.path.split(self._file)[1]
        self.ext=os.path.splitext(self._file)[1].replace('.','')
        self.from_addr = "li_xianghuay@163.com"
        self.password = "ri123654"#"mxzgoepapvimcahj"
        self.to_addr = "zijinshanmao@163.com"
        self.smtp_server = "smtp.163.com"
    def msg_set(self):
        msg = MIMEMultipart()  
        msg['From'] = _format_addr('Python爱好者 <%s>' % self.from_addr)
        msg['To'] = _format_addr('管理员 <%s>' % self.to_addr)
        msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()
        msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))    
        
        with open(self._file, 'rb') as f:
            # 设置附件的MIME和文件名，这里是png类型:
            mime = MIMEBase('image', self.ext, filename=self.filename)
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename=self.filename)
            
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            msg.attach(mime)
        return msg
    def sendmile(self):
        msg=self.msg_set()
        server = smtplib.SMTP(self.smtp_server, 25)
        server.set_debuglevel(1)
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, [self.to_addr],msg.as_string())
        server.quit()


if __name__=='__main__':
    mm=sendmeil('C:/Users\Administrator.Z6NRQGUFOYCRJGF/Desktop/tu.jpg')
    mm.sendmile()

   
    