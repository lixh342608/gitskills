#coding=utf-8
'''
Created on 2017年6月12日

@author: Administrator
'''
from selenium import webdriver
from selenium.webdriver.support.select import Select
from time import sleep
from time_out import waittime
from tkinter import *
import tkinter.messagebox

'''def writcol(col):
    with open("collocation.pic","wb") as f:
        pickle.dump(col, f)
def loadcol():
    try:
        with open("collocation.pic","rb") as f:
            col=pickle.load(f)   
            return col     
    except IOError:
        return 0'''


class lishitest:
    def __init__(self,username,paypwd,passwd="ri123654"):
        self.username=username
        self.paypwd=paypwd
        self.pwd=passwd
        
        self.driver=webdriver.Chrome('C:/chromedriver')

        
        self.driver.maximize_window()
        self.wait=waittime(self.driver,20)
        self.login()
        self.driver.get('https://jr.yatang.cn/GradRedPacket')
    def login(self):
        self.driver.get('https://jr.yatang.cn/NewLogin/index/referer/')
        self.driver.switch_to.frame(0)
        self.wait.visibility('xpath', '//*[@id="js-username"]').send_keys(self.username)

        self.wait.visibility('xpath', '//*[@id="js-password"]').send_keys(self.pwd)
        select=self.wait.visibility('id','_cache_time')
        Select(select).select_by_value('7200')

        self.wait.clickable('xpath', '//*[@id="js-login"]').click()
        sleep(2)


        if self.driver.title=='雅堂金融':
            print('登陆成功')

        else:
            self.login()
        


        
            


    '''def giter(self,pay_pwd,numer=None):
        self.wrrtenum(numer)
        ele=self.wait.clickable('xpath',self.check_xpath)
        ele.click()
        self.miaochu(pay_pwd)
    def miaochu(self,pay_pwd):
        pay_ele=self.wait.visibility('xpath',self.ppay_xpath)
        pay_ele.send_keys(pay_pwd)
        commit_ele=self.wait.clickable('xpath',self.commit_xpath)
        commit_ele.click()
        
        check_ele=self.persi_ele('/html/body/div[5]/div/div/div/div[1]/div[1]/b')
        print(check_ele.text)'''

    def timeset(self):

        
        while True:

            self.driver.refresh()
            sleep(1)

            ti_text=self.wait.get_ele('css','body > div.project-move-on > div.grad-container > div > div > div.count-down > div > span').text


            ti_list=ti_text.split('天')
            days=int(ti_list[0])
            ti_list=ti_list[1].strip().split(':')
            print(ti_list)
            ti_sum=(days*24+int(ti_list[0]))*3600+int(ti_list[1])*60+int(ti_list[2])
            print('距离投秒时间还有%d秒' % ti_sum)
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
        self.wait.visibility('css','body > div.project-move-on > div.grad-container > div > div > div.count-input-container > input.count-btn')
'''def main_go():
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
 
    
    b1=Button(root,text="开始抢秒",command=click_on,bg="red",width=15,fg="blue").pack()
    root.mainloop()'''

if __name__=='__main__':
    hb=lishitest("夜夜难眠","aa123..")
    hb.timeset()

