#coding=utf-8
'''
Created on 2017年6月16日

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
import urllib.request
import urllib.parse
import json,requests
#使用requests实现查询第一页期限一个月，待投金额大于X，利率最高的标
def reque_num(main_num):
    url='https://jr.yatang.cn/Financial/getAssetList'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'}
    data={}
    data['aprrange']='0'
    data['selectdate']='2'
    data['repaystyle']='0'
    data['goto_page']=''
    data['page_href']='/Financial/getAssetList?&p=1'
    resq=requests.post(url,data,headers)
    t_text=json.loads(resq.text)['list']
    t_text=[i for i in t_text if i['showday']=='1个月' and i['remain'] > main_num]
    apr=0
    for j in t_text:
        if float(j['apr'])>apr:
            apr=float(j['apr'])
            apr_num=j['id']
    
    return apr_num
#使用urllib实现查询第一页期限一个月，待投金额大于X，利率最高的标   
'''def select_num(main_num):
    url='https://jr.yatang.cn/Financial/getAssetList'
    
    data={}
    data['aprrange']='0'
    data['selectdate']='2'
    data['repaystyle']='0'
    data['goto_page']=''
    data['page_href']='/Financial/getAssetList?&p=1'
    
    data=urllib.parse.urlencode(data).encode('utf-8')
    req=urllib.request.Request(url,data)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36')
    resp=urllib.request.urlopen(req)
    t_text=json.loads(resp.read().decode('utf-8'))['list']


    t_text=[i for i in t_text if i['showday']=='1个月' and i['remain'] > main_num]
    apr=0
    for j in t_text:
        if float(j['apr'])>apr:
            apr=float(j['apr'])
            apr_num=j['id']
    
    return apr_num'''
class q_mon:
    def __init__(self,username,pwd,pay_pwd):
        self.username=username
        self.pwd=pwd
        self.paypwd=pay_pwd
        self.driver=webdriver.Chrome('C:/chromedriver')
        self.driver.get('https://jr.yatang.cn/Financial/asset')
        
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
    def login(self):
        self.driver.get('https://jr.yatang.cn/NewLogin/index/referer/')
        self.persi_ele('//*[@id="username"]').send_keys(self.username)
        
        self.persi_ele('//*[@id="password"]').send_keys(self.pwd)
        
        yzm=img_set(self.driver)
        self.persi_ele('//*[@id="sendnumber"]').send_keys(yzm)
        
        self.persi_ele('//*[@id="button"]').click()
        
        sleep(2)
        if self.driver.title!='雅堂金融—专注于家具产业领域供应链金融服务平台！':
            self.login()
            
    def q_mont(self,main_num):
        login_ele=self.wait.get_ele('xpath','//*[@id="top"]/div[1]/div/div[2]/a[2]')
        if login_ele.text=='免费注册':
            self.login()
        apr_num=reque_num(main_num)
        url='https://jr.yatang.cn/Invest/ViewBorrow/ibid/%s' % apr_num
        self.driver.get(url)
        self.persi_ele('//*[@id="amountt"]').send_keys(main_num)
if __name__=='__main__':
    qiang=q_mon('月光宝盒','ri123654','aaa111')
    qiang.q_mont(5000)
    




