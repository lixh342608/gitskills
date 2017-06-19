#coding=utf-8
'''
Created on 2017年6月12日

@author: Administrator
'''
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import re,pickle,os
from time_out import waittime
from img_set import img_set
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
        self.driver.get('https://jr.yatang.cn/Financial/welfare')
        
        self.driver.maximize_window()
        self.wait=waittime(self.driver,10)
        
        
        
        
    def persi_ele(self,by_vale,byse='xpath'):
        while True:
            ele=self.wait.get_ele(byse,by_vale)
            if ele==0:
                continue
            else:
                if ele.is_displayed():
                    break
                else:
                    print("控件不可见！")
                    continue
        return ele 
    def lishinum(self):
        pr_ele=self.persi_ele('wf_move_box','class')
        ele_list=pr_ele.find_elements_by_class_name('wf_list_box')
        ele_list=filter(lambda x:x.get_attribute('iborrowid')!='0',ele_list)
        lishinumer=0
        ele_praser=0
        for i in ele_list:
            ele=i.find_element_by_class_name('wf_xq_lv')
            ele_pra=int(re.sub('\W','',ele.text))
            if ele_pra>ele_praser:
                ele_praser=ele_pra
                lishinumer=i.get_attribute('iborrowid')
        return lishinumer
    def set_xpath(self):
        lishinumer=self.lishinum()
        self.numer_xpath='//*[@id="amountt_%s"]' % lishinumer
        self.check_xpath='//*[@id="incheck_%s"]' % lishinumer
        self.ppay_xpath='//*[@id="ppay_%s"]' % lishinumer
        self.commit_xpath='//*[@id="button_%s"]' % lishinumer
        self.withdra_class='aj_withdrawalCash_%s' % lishinumer
        self.time_class='lefttime_%s' % lishinumer
            
    def login(self,username,pwd):
        self.driver.get('https://jr.yatang.cn/NewLogin/index/referer/')
        self.persi_ele('//*[@id="username"]').send_keys(username)
        
        self.persi_ele('//*[@id="password"]').send_keys(pwd)
        
        yzm=img_set(self.driver)
        self.persi_ele('//*[@id="sendnumber"]').send_keys(yzm)
        
        self.persi_ele('//*[@id="button"]').click()
        
        sleep(2)
        if self.driver.title=='雅堂金融—专注于家具产业领域供应链金融服务平台！':
            
            self.driver.get('https://jr.yatang.cn/Financial/welfare')
            sleep(0.5)
        else:
            
            
            self.login(username,pwd)
            



    def wrrtenum(self,numer):
        if numer==None:
            dra_text=self.persi_ele(self.withdra_class, 'class').text
            
            numer=int(float(dra_text.strip('￥').replace(',','')))
                
            
        self.persi_ele(self.numer_xpath).send_keys(numer)
        
            
    

    def giter(self,pay_pwd,numer=None):
        self.wrrtenum(numer)
        ele=self.persi_ele(self.check_xpath)
        ele.click()
        self.miaochu(pay_pwd)
    def miaochu(self,pay_pwd):
        pay_ele=self.persi_ele(self.ppay_xpath)
        pay_ele.send_keys(pay_pwd)
        commit_ele=self.persi_ele(self.commit_xpath)
        commit_ele.click()
        sleep(200)

    def timeset(self,username,pwd):
        self.set_xpath()
        
        while True:
            self.driver.refresh()
            login_ele=self.wait.get_ele('xpath','//*[@id="top"]/div[1]/div/div[2]/a[2]')
            if login_ele.text=='免费注册':
                self.login(username,pwd)
            ti_text=self.wait.get_ele('class',self.time_class).text
            ti_list=ti_text.split(':')
            ti_sum=int(ti_list[0])*3600+int(ti_list[1])*60+int(ti_list[2])
            #ti_sum=int(ti_list[2])
            #print('距离投秒时间还有%d秒' % ti_sum)
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
def main_go():
    
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
        username=username_var.get()
        pwd=pwd_var.get()
        paypwd=paypwd_var.get()
        pranum=pranum_var.get()
        if username and pwd and paypwd:
            col=[username,pwd,paypwd]
            writcol(col)
        
            lishi=lishitest()
            lishi.timeset(username,pwd)
            if pranum:
                lishi.giter(paypwd,pranum)
            else:
                lishi.giter(paypwd)
        
        else:
            tkinter.messagebox.askokcancel("提示","除投资金额外所有项不可为空，如果有误将导致无法登录或抢秒时交易密码错误。")
 
    
    b1=Button(root,text="开始抢秒",command=click_on,bg="red",width=15,fg="blue").pack()
    root.mainloop()

if __name__=='__main__':
    main_go()

