#coding=utf-8
'''
Created on 2017年6月16日

@author: Administrator
'''
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import pickle
from time_out import waittime
from tkinter import *
import tkinter.messagebox
import json,requests
#使用requests实现查询第一页期限一个月，待投金额大于X，利率最高的标
def reque_num(main_num):
    sleep(1.5)
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
    apr_num=0
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
    def __init__(self,username,pwd,pay_pwd,par_num,par_sex):
        self.username=username
        self.pwd=pwd
        self.paypwd=pay_pwd
        self.par_num=par_num
        self.par_sex=par_sex
        self.driver=webdriver.Chrome('C:/chromedriver')
        self.driver.get('https://jr.yatang.cn/Financial/asset')
        
        self.driver.maximize_window()
        self.wait=waittime(self.driver,10)
    def persi_ele(self,by_vale,byse='xpath',col=1000):
        y_col=0
        while y_col<=col:
            ele=self.wait.get_ele(byse,by_vale)
            if ele==0:
                continue
            else:
                if ele.is_displayed():
                    return ele
                else:
                    print("控件[%s]不可见！" % by_vale)
                    y_col+=1
                    if y_col==col:
                        return None
         
    def login(self):
        self.driver.get('https://jr.yatang.cn/NewLogin/index/referer/')
        self.driver.switch_to.frame(0)
        self.persi_ele('//*[@id="js-username"]').send_keys(self.username)
        
        self.persi_ele('//*[@id="js-password"]').send_keys(self.pwd)
        
        
        self.persi_ele('//*[@id="js-login"]').click()
        
        sleep(2)
        if self.driver.title=='雅堂金融—专注于家具产业领域供应链金融服务平台！':
            pass
            
        else:
            self.login()
            
    def q_mont(self):
        main_num=int(self.par_num)*int(self.par_sex)
        login_ele=self.wait.get_ele('xpath','//*[@id="top"]/div[1]/div/div[2]/a[2]')
        if login_ele.text=='免费注册':
            self.login()
        apr_num=reque_num(main_num)
        while int(apr_num)==0:
            print('没有可投资项目，重新刷新列表中！')
            apr_num=reque_num(main_num)
        
        url='https://jr.yatang.cn/Invest/ViewBorrow/ibid/%s' % apr_num
        self.driver.get(url)
        self.persi_ele('//*[@id="amountt"]').send_keys(main_num)
        hbxs_ele=self.persi_ele('hbje_xs','class',11)
        if hbxs_ele:
            hbxs_ele.click()
            
            ele_box=self.persi_ele('hb_xl_box','class')
            try:
                ele_box.find_element_by_class_name('hb_check_list').click()
               

                yq_hb=self.par_sex+'00元'
                print(yq_hb)
                if hbxs_ele.text==yq_hb:
                    #if tkinter.messagebox.askokcancel('提示', '是否继续'):
                            
                    print(hbxs_ele.text)
                    #self.biaochu()
                    sleep(10)
                    self.q_mont()
                
                else:
                    self.q_mont()
                
            except:
                print('没有找到可用红包，重新投资！')
                self.q_mont()
        else:
            print('没有找到可用红包，重新投资！')
            self.q_mont()
        

    def biaochu(self):
        self.persi_ele('//*[@id="incheck"]').click()
        self.persi_ele('//*[@id="ppay"]').send_keys(self.paypwd)
        self.persi_ele('//*[@id="button"]').click()
if __name__=='__main__':
    qiang=q_mon('月光宝盒','ri123654','aaa111','8000','2')
    qiang.q_mont()
    




