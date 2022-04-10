#coding=utf-8
import psutil,time,os
import signal
import pygame
import datetime
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
from email.mime.base import MIMEBase
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog

import smtplib, os


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


class sendmeil:
    def __init__(self):
        # self._file=_file
        # self.filename=os.path.split(self._file)[1]
        # self.ext=os.path.splitext(self._file)[1].replace('.','')
        self.from_addr = "li_xianghuay@163.com"
        self.password = "ri123654"  # "mxzgoepapvimcahj"
        self.to_addr = "zijinshanmao@163.com"
        self.smtp_server = "smtp.163.com"

        self.add_att = []

    def add_from(self, fileph):
        filename = os.path.split(fileph)[1]
        # ext=os.path.splitext(fileph)[1].replace('.','')
        att = MIMEBase('application', 'octet-stream')
        att.set_payload(open(fileph, 'rb').read())
        att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', filename))
        encoders.encode_base64(att)

        self.add_att.append(att)

    def msg_set(self):
        msg = MIMEMultipart('alternative')
        msg['From'] = _format_addr('月半弯 <%s>' % self.from_addr)
        msg['To'] = _format_addr('管理员 <%s>' % self.to_addr)
        msg['Subject'] = Header('来自花儿的问候……', 'utf-8').encode()
        msg.attach(MIMEText('帐户掉线通知。', 'plain', 'utf-8'))
        #for att in self.add_att:
           # msg.attach(att)

        return msg

    def sendmile(self):
        msg = self.msg_set()
        server = smtplib.SMTP(self.smtp_server, 25)
        server.set_debuglevel(1)
        server.login(self.from_addr, self.password)
        try:
            server.sendmail(self.from_addr, [self.to_addr], msg.as_string())
            server.quit()
            return True
        except Exception as e:
            server.quit()
            print(e)
            return False
class monitor_proc():
    def __init__(self):
        self.root = Tk()
        self.root.wm_attributes("-topmost", 1)
        self.root.title('你值得拥有')
        width_n = self.root.winfo_screenwidth() / 2 - 200
        height_n = self.root.winfo_screenheight() / 2 - 200
        self.root.geometry('400x500+%d+%d' % (int(width_n), int(height_n)))
        Label(self.root,width=7).grid(row=0,column=0)
        Label(self.root).grid(row=1,column=0)
        Label(self.root).grid(row=3,column=0)
        Label(self.root).grid(row=5,column=0)
        Label(self.root).grid(row=7,column=0)

    def play_musc(self,file_path,loop_tag=True):
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)  # 载入一个音乐文件用于播放
        while True:
            # 检查音乐流播放，有返回True，没有返回False
            # 如果没有音乐流则选择播放
            if pygame.mixer.music.get_busy() == False:  # 检查是否正在播放音乐
                pygame.mixer.music.play()  # 开始播放音乐流
                if not loop_tag:
                    break
    def monitor_start(self,time_tag=3):
        start_time = int(time.time())
        while int(time.time()) - start_time < 60:
            all_proc = psutil.pids()
            proc_dic = {proc:[None,0] for proc in all_proc if psutil.Process(proc).name() == "mhmain.exe"}
            if proc_dic:
                print(proc_dic)
                break
            else:
                time.sleep(5)
        while True:
            time.sleep(5)
            for proc in proc_dic.keys():
                try:
                    proc_ins=psutil.Process(proc)
                except:
                    self.monitor_start()
                proc_io=proc_ins.io_counters()
                last_io,last_error_num=proc_dic.get(proc)
                print("游戏编号:%s" % proc)
                print(proc_io)
                print(last_io)
                if proc_io == last_io:
                    last_error_num += 1
                    proc_dic[proc]=[proc_io,last_error_num]
                    print("数据错误%s" % last_error_num)
                    print("错误时间：%s" % datetime.datetime.now())
                    if int(time.time())-start_time < 60:
                        kill_com="tskill %s" % proc
                        os.system(kill_com)
                        proc_dic=proc_dic.pop(proc)
                        self.monitor_start()
                else:
                    proc_dic[proc]=[proc_io,0]
                if last_error_num > time_tag:
                    print("掉线时间：%s" % datetime.datetime.now())
                    mm = sendmeil()
                    mm.sendmile()
                    self.play_musc(r"F:\KuGou\周冰倩 - 真的好想你.mp3")
                print("==================================")
    def term(self):
        self.root.mainloop()
if __name__ == "__main__":

    proc_moniter=monitor_proc()
    #proc_moniter.term()
    proc_moniter.monitor_start()
