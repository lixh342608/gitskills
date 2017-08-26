#coding=utf-8
'''
Created on 2017年6月12日

@author: Administrator
'''
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.select import Select
import re,pickle,time,sys,platform
from time_out import waittime
from tkinter import *
import tkinter.messagebox

def writcol(col):
    with open("collocation.pic","wb") as f:
        pickle.dump(col, f)
def loadcol():
    try:
        with open("collocation.pic","rb") as f:
            col=pickle.load(f)   
            return col     
    except IOError:
        return 0


class lishitest:
    def __init__(self):
        
        self.driver=webdriver.Chrome('C:/chromedriver')
        self.driver.get('https://jr.yatang.cn')
        
        self.driver.maximize_window()
        self.wait=waittime(self.driver,30)
            
    def login(self,username,pwd):
        self.driver.get('https://jr.yatang.cn/NewLogin/index/referer/')
        self.driver.switch_to.frame(0)
        self.wait.visibility('xpath','//*[@id="js-username"]').send_keys(username)
        
        self.wait.visibility('xpath','//*[@id="js-password"]').send_keys(pwd)
        select=self.wait.visibility('id','_cache_time')
        Select(select).select_by_value('7200')
        
        
        self.wait.visibility('xpath','//*[@id="js-login"]').click()
        
        sleep(2)
        login_ele=self.wait.get_ele('xpath','//*[@id="top"]/div[1]/div/div[2]/a[2]')
        #print(login_ele.text)
        if login_ele.text=='免费注册':
            self.login(username,pwd)
        


    def wrrtenum(self,numer):
        if numer==None:
            dra_text=self.wait.visibility('id','mostaccount2').click()
            
            #numer=int(float(dra_text.strip('￥').replace(',','')))
        else:
                
            
            self.wait.visibility('id','amountt').send_keys(numer)
        
            
    

    def giter(self,pay_pwd,numer=None):
        gq_link=self.wait.visibility('css','body > div.zc_detail > div.zc_detail_box > a').get_attribute('href')
        self.driver.get(gq_link)
        ele = self.wait.presence('id','incheck')
        if ele:
            self.driver.refresh()
            self.wrrtenum(numer)
        #ele=self.persi_ele('incheck','id')
        #ele.click()
            self.miaochu(pay_pwd)
    def miaochu(self,pay_pwd):
        pay_ele=self.wait.visibility('id','ppay')
        pay_ele.send_keys(pay_pwd)
        text_ele = self.wait.visibility('id','reg_chk')
        text_ele.click()
        commit_ele=self.wait.clickable('id','button')
        commit_ele.click()
        
        check_ele=self.wait.visibility('xpath','/html/body/div[5]/div/div/div/div[1]/div[1]/b')
        print(check_ele.text)

    def timeset(self,username,pwd,numer=None):

        
        while True:
            now=time.strftime('%Y-%m-%d')
            if now!="2017-08-26":
                try:
                    sys.exit(0)
                except:
                    tkinter.messagebox.showinfo('报告', '程序已失效！')
                finally:
                    return 1
            self.driver.refresh()
            login_ele=self.wait.visibility('xpath','//*[@id="top"]/div[1]/div/div[2]/a[2]')
            if login_ele.text=='免费注册':
                self.login(username,pwd)
                self.driver.get('https://jr.yatang.cn/Crowdfunding')

            sleep(1)
            ti_text=self.wait.visibility('class','zc_sysj').text
            ti_list=re.findall("\d{1,2}",ti_text)
            #ti_sum=int(ti_list[0])*86400+int(ti_list[1])*3600+int(ti_list[2])*60+int(ti_list[3])
            ti_sum=int(ti_list[3])
            #ti_strip=time.mktime(time.strptime('2017-08-04 10:40:00', "%Y-%m-%d %H:%M:%S"))
            #ti_sum=int(ti_strip-time.time())-16
            print('距离投资股权时间还有%d秒' % ti_sum)
            if ti_sum>600:
                sleep(300)
                continue
            elif ti_sum>300:
                sleep(180)
                continue
            elif ti_sum>200:
                sleep(90)
                continue
            elif ti_sum>50:
                sleep(12)
                continue
            elif ti_sum>10:
                sleep(8)
                continue
            elif ti_sum>5:
                sleep(ti_sum-2)
                continue
            else:
                break
        return 0
def main_go():
    plat='Z6NRQGUFOYCRJGFWindows-7-6.1.7601-SP1'
    col_list=loadcol()
    if col_list==0:
        col_list=["","",""]

    root=Tk()
    width_n=root.winfo_screenwidth()/2-200
    height_n=root.winfo_screenheight()/2-150
    root.geometry('350x300+%d+%d' % (int(width_n),int(height_n)))

    lab1=Label(root,text="请输入雅堂帐户用户名:").pack()
    username_var=StringVar()
    Entry(root,textvariable=username_var).pack()
    username_var.set(col_list[0])

    lab2=Label(root,text="请输入雅堂帐户密码:").pack()
    pwd_var=StringVar()
    Entry(root,textvariable=pwd_var,show='*').pack()
    pwd_var.set(col_list[1])
    lab3=Label(root,text="请输入雅堂帐户交易密码:").pack()
    paypwd_var=StringVar()
    Entry(root,textvariable=paypwd_var).pack()
    paypwd_var.set(col_list[2])

    lab4=Label(root,text="请输入投资金额（置 空将默认为最大金额）:").pack()
    pranum_var=StringVar()
    Entry(root,textvariable=pranum_var).pack()
    pranum_var.set("")
    def click_on():
        if platform.node()+platform.platform()!=plat:root.destroy()
        username=username_var.get()
        pwd=pwd_var.get()
        paypwd=paypwd_var.get()
        pranum=pranum_var.get()
        if username and pwd and paypwd:
            col=[username,pwd,paypwd]
            writcol(col)
        
            lishi=lishitest()
            pac=lishi.timeset(username,pwd)
            if pac==0:
                if pranum:
                    lishi.giter(paypwd,pranum)
                else:
                    lishi.giter(paypwd)
            else:
                lishi.driver.quit()
                
        
        else:
            tkinter.messagebox.askokcancel("提示","除投资金额外所有项不可为空，如果有误将导致无法登录或抢秒时交易密码错误。")
 
    
    b1=Button(root,text="开始抢股权",command=click_on,bg="red",width=15,fg="blue").pack()
    root.mainloop()

if __name__=='__main__':
    main_go()

