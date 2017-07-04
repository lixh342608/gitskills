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
from tkinter import *
from tkset import *
import tkinter.messagebox
import tkinter.filedialog

import smtplib,os
from statsmodels.tsa.vector_ar.tests.results.results_svar_st import b_var
from prompt_toolkit.renderer import HeightIsUnknownError

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
class sendmeil:
    def __init__(self):
        #self._file=_file
        #self.filename=os.path.split(self._file)[1]
        #self.ext=os.path.splitext(self._file)[1].replace('.','')
        self.from_addr = "li_xianghuay@163.com"
        self.password = "ri123654"#"mxzgoepapvimcahj"
        self.to_addr = "zijinshanmao@163.com"
        self.smtp_server = "smtp.163.com"
        
        self.add_att=[]
    def add_from(self,fileph):
        filename=os.path.split(fileph)[1]
        #ext=os.path.splitext(fileph)[1].replace('.','')
        att = MIMEBase('application', 'octet-stream')  
        att.set_payload(open(fileph, 'rb').read())  
        att.add_header('Content-Disposition', 'attachment', filename=('gbk','',filename) )  
        encoders.encode_base64(att)  
  
        self.add_att.append(att)  
    def msg_set(self):
        msg = MIMEMultipart('alternative')  
        msg['From'] = _format_addr('Python爱好者 <%s>' % self.from_addr)
        msg['To'] = _format_addr('管理员 <%s>' % self.to_addr)
        msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()
        msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))    
        for att in self.add_att:
            msg.attach(att)
        '''with open(self._file, 'rb') as f:
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
            msg.attach(mime)'''
        return msg
    def sendmile(self):
        msg=self.msg_set()
        server = smtplib.SMTP(self.smtp_server, 25)
        server.set_debuglevel(1)
        server.login(self.from_addr, self.password)
        try:
            server.sendmail(self.from_addr, [self.to_addr],msg.as_string())
            server.quit()
            return True
        except Exception as e:
            server.quit()
            print(e)
            return False
class xupi:
    def __init__(self):
        self.pack=0
        self.root=Tk()
        self.root.title("晒出你的美照")
        width_n=self.root.winfo_screenwidth()/2-200
        height_n=self.root.winfo_screenheight()/2-150
        self.root.geometry('350x300+%d+%d' % (int(width_n),int(height_n)))
    def send_pi(self):
        def click_on():
            if b_var.get()=='舍我其谁':
                filename=tkinter.filedialog.askopenfilename(initialdir = 'd:/')
                mm=sendmeil()
                mm.add_from(filename)

                fc=mm.sendmile()
                if fc:
                    lab1_var.set('乖哦，发送成功了！')
                    b_var.set('我要抢标')
            else:
                self.root.destroy()
                self.pack=1
        lab1_var=StringVar()  
        lab1=Label(self.root,textvariable=lab1_var,font=50,width=50,height=10)
        lab1_var.set("照片格式仅支持png,gif哦。")
        lab1.pack()
        b_var=StringVar()
        
        b1=Button(self.root,textvariable=b_var,command=click_on,bg="red",width=15,fg="blue").pack(side=BOTTOM,pady=10)
        b_var.set("舍我其谁")
        self.root.mainloop()
        return self.pack
if __name__=='__main__':
    '''mm=sendmeil()
    mm.add_from('C:/Users\Administrator.Z6NRQGUFOYCRJGF/Desktop/tu.jpg')

    fc=mm.sendmile()
    print(fc)'''
    xp=xupi()
    pack=xp.send_pi()
    if pack:
        yue=yuebiao_gui()
        yue.main_go()
        
    
    

   
    