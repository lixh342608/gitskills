#coding=utf-8
'''
Created on 2017年6月12日

@author: Administrator
'''
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
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
        self.driver.get('https://jr.yatang.cn/Financial/welfare')
        
        self.driver.maximize_window()
        self.wait=waittime(self.driver,10)
        
    def persi_ele(self,by_vale,byse='xpath',col=1000):
        y_col=0
        while y_col<=col:
            ele=self.wait.get_ele(byse,by_vale)
            if ele==0:
                y_col+=1
                continue
            else:
                if ele.is_displayed():
                    return ele
                else:
                    print("控件[%s]不可见！" % by_vale)
                    y_col+=1
                    continue
        else:
            return None        
        
        
    def lishinum(self):
        pr_ele=self.persi_ele('wf_move_box','class',0)
        if not pr_ele:
            return '0'
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
    def set_xpath(self,lishinumer):        
        self.numer_xpath='//*[@id="amountt_%s"]' % lishinumer
        self.check_xpath='//*[@id="incheck_%s"]' % lishinumer
        self.ppay_xpath='//*[@id="ppay_%s"]' % lishinumer
        self.commit_xpath='//*[@id="button_%s"]' % lishinumer
        self.withdra_class='aj_withdrawalCash_%s' % lishinumer
        self.time_class='lefttime_%s' % lishinumer
            
    def login(self,username,pwd):
        self.driver.get('https://jr.yatang.cn/NewLogin/index/referer/')
        self.driver.switch_to.frame(0)
        self.persi_ele('//*[@id="js-username"]').send_keys(username)
        
        self.persi_ele('//*[@id="js-password"]').send_keys(pwd)
        
        
        self.persi_ele('//*[@id="js-login"]').click()
        
        sleep(2)
        login_ele=self.wait.get_ele('xpath','//*[@id="top"]/div[1]/div/div[2]/a[2]')
            
        if login_ele.text=='免费注册':
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
        
        check_ele=self.persi_ele('/html/body/div[5]/div/div/div/div[1]/div[1]/b')
        print(check_ele.text)

    def timeset(self,username,pwd):
        lishinumer=self.lishinum()
        if lishinumer=='0':
            tkinter.messagebox.showinfo('报告', '没有可投秒标！')
            try:
                sys.exit(0)
            except:
                tkinter.messagebox.showinfo('报告', '程序准备退出！')
            finally:
                return 2
        self.set_xpath(lishinumer)
        
        while True:
            now=time.strftime('%Y-%m-%d',time.localtime(time.time()))
            if now!="2017-07-10":
                try:
                    sys.exit(0)
                except:
                    tkinter.messagebox.showinfo('报告', '程序已失效！')
                finally:
                    return 1
            self.driver.refresh()
            login_ele=self.wait.get_ele('xpath','//*[@id="top"]/div[1]/div/div[2]/a[2]')
            
            if login_ele.text=='免费注册':
                self.login(username,pwd)
                self.driver.get('https://jr.yatang.cn/Financial/welfare')
            ti_text=self.wait.get_ele('class',self.time_class).text
            ti_list=ti_text.split(':')
            ti_sum=int(ti_list[0])*3600+int(ti_list[1])*60+int(ti_list[2])
            #ti_sum=int(ti_list[2])
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
 
    
    b1=Button(root,text="开始抢秒",command=click_on,bg="red",width=15,fg="blue").pack()
    root.mainloop()

if __name__=='__main__':
    main_go()

