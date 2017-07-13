#coding=utf-8
'''
Created on 2017年6月16日

@author: Administrator
'''
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import pickle,threading
from time_out import waittime
from tkinter import *
import tkinter.messagebox
import json,requests,platform,time,sys

def writcol(col):
    with open("yuelocation.pic","wb") as f:
        pickle.dump(col, f)
def loadcol():
    try:
        with open("yuelocation.pic","rb") as f:
            col=pickle.load(f)   
            return col     
    except IOError:
        return 0

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
    
    t_text=[i for i in t_text if i['showday']=='1个月' and i['remain'] > main_num]# and i['borrow_type'] != '10']
    #for i in t_text:
        #print(i)
    apr=0
    apr_num=0
    for j in t_text:
        if float(j['apr'])>apr:
            apr=float(j['apr'])
            apr_num=j['id']
    
    return apr_num   

class q_mon(threading.Thread):
    def __init__(self,eve,msg_var,commit_bt):
        super(q_mon,self).__init__()
        self.eve=eve
        self.msg_var=msg_var
        self.commit_bt=commit_bt
        self.nopar=[]
        self.yuecol=loadcol()
        self.username=self.yuecol[0]#用户名
        self.pwd=self.yuecol[1]#用户密码
        self.paypwd=self.yuecol[2]#支付密码
        self.par_num=int(self.yuecol[3])#红包倍数
        self.parsex_list=self.yuecol[4].split(',')#红包面值'''
        #self.driver=webdriver.PhantomJS()
        self.driver=webdriver.Chrome('C:/chromedriver')
        self.driver.get('https://jr.yatang.cn/Financial/asset')
        
        self.driver.maximize_window()
        self.wait=waittime(self.driver,30)
    def run(self):
        self.eve.wait()
        self.q_mont()
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
         
    def login(self):
        self.driver.get('https://jr.yatang.cn/NewLogin/index/referer/')
        self.driver.switch_to.frame(0)
        self.persi_ele('//*[@id="js-username"]').send_keys(self.username)
        
        self.persi_ele('//*[@id="js-password"]').send_keys(self.pwd)
        
        
        self.persi_ele('//*[@id="js-login"]').click()
        sleep(2)
        login_ele=self.wait.get_ele('xpath','//*[@id="top"]/div[1]/div/div[2]/a[2]')
        if login_ele and login_ele.text=='免费注册':
            self.login()
        else:
            self.msg_var.set('登陆成功')

            
    def q_mont(self):

        if not self.eve.is_set():
            self.msg_var.set("抢标已暂停")
            self.chnge_bt()
            self.driver.quit()
            self.eve.wait()
        #检测登录
        self.msg_var.set("检测登录状态...")
        login_ele=self.wait.get_ele('xpath','//*[@id="top"]/div[1]/div/div[2]/a[2]')
        if login_ele.text=='免费注册':
            self.msg_var.set("正在准备登录...")
            self.login()
        self.msg_var.set("正在寻找月标...")
        #循环直到找到为止
        apr_num=0
        while int(apr_num)==0:
            now=time.strftime('%Y-%m-%d',time.localtime(time.time()))
            if now!="2017-07-12":
                try:
                    sys.exit(0)
                except:
                    tkinter.messagebox.showinfo('报告', '程序已失效！')
                finally:
                    self.eve.clear()
                
            if not self.eve.is_set():
                self.msg_var.set("抢标已暂停")
                self.chnge_bt()
                self.driver.quit()
                self.eve.wait()
            self.msg_var.set("宝宝努力抢标中...")
            for pars in self.parsex_list:
                parsex=int(pars)
                if pars not in self.nopar:
                    main_num=self.par_num*parsex
                    apr_num=reque_num(main_num)
                else:
                    continue
                if apr_num!=0:
                    break
            else:
                continue        
            break
                    
                    


        self.msg_var.set("抢标成功，\n准备投标中...")
        url='https://jr.yatang.cn/Invest/ViewBorrow/ibid/%s' % apr_num
        self.driver.get(url)
        mynum=self.persi_ele('//*[@id="amountt"]',col=0)
        if mynum:
            mynum.send_keys(main_num) 
            self.msg_var.set("选择红包中...")
        else:
            self.msg_var.set("标被人抢先一步！")
            self.q_mont()
        #查找红包选框
        hbxs_ele=self.persi_ele('hbje_xs','class',3)
        if hbxs_ele:
            hbxs_ele.click()
            #找到红包盒子
            ele_box=self.persi_ele('hb_xl_box','class') 
            try:
                #找到盒子中所有红包
                hb_list=self.driver.find_elements_by_class_name('hb_check_list')
            
                for hb in hb_list:
                    hb_li=hb.text.replace('元','').split('\n')
                    #如果红包等于预期红包且投资金额等于预期投资金额则选中该红包
                    if int(hb_li[0])==parsex and int(hb_li[1])==main_num:
                        hb.find_element_by_class_name('hbcheck_1').click()
                    else:
                        continue
                    if hbxs_ele.text=='%d元' % parsex:
                        self.msg_var.set("红包已准备完毕")
                       
                        self.biaochu()
                        break
                          
                                    
                else:
                    tkinter.messagebox.showinfo('报告', '没有找到%d元面值红包，怪不得宝宝了' % parsex)
                    
                    self.nopar.append(parsex)
                    if len(self.nopar)>=len(self.parsex_list):
                        tkinter.messagebox.showinfo('报告', '主人应该没有%d倍红包了' % self.par_num)
                        self.msg_var.set("抢标已暂停")
                        self.chnge_bt()
                        self.driver.quit()
                        self.eve.wait()
                        
                    
                self.q_mont()
                
                
            except:
                self.msg_var.set('没有找到可用红包，重新投资！')
                self.q_mont()
        else:
            self.msg_var.set('没有找到可用红包，重新投资！')
            self.q_mont()
        

    def biaochu(self):
        self.persi_ele('//*[@id="incheck"]').click()
        pay_ele=self.persi_ele('//*[@id="ppay"]',col=10)
        if pay_ele!=None:
        
            pay_ele.send_keys(self.paypwd)
            self.persi_ele('//*[@id="button"]').click()
            ti_mm=15
            while ti_mm>=0:
                self.msg_var.set('投标已进入队列，\n等待15秒（%d）' % ti_mm)
                sleep(1)
                ti_mm-=1
            
    def chnge_bt(self):
        self.commit_bt['state']=NORMAL
        self.commit_bt["text"]="继续投资"        
class yuebiao_gui:
    def __init__(self):
        self.plat='Z6NRQGUFOYCRJGFWindows-7-6.1.7601-SP1'

            
        self.root=Tk()
        self.root.title('你值得拥有')
        width_n=self.root.winfo_screenwidth()/2-200
        height_n=self.root.winfo_screenheight()/2-200
        self.root.geometry('400x400+%d+%d' % (int(width_n),int(height_n)))


    
    
    def main_go(self):
        
        col_list=loadcol()
        if col_list==0:
            col_list=["","","","",""]

        def click_on():
            if platform.node()+platform.platform()!=self.plat:self.root.destroy()
            
            
            username=username_var.get()
            pwd=pwd_var.get()
            paypwd=paypwd_var.get()
            pranum=pranum_var.get()
            hbset=hb_var.get()
            if username and pwd and paypwd and pranum and hbset:
                stop_bt['state']=NORMAL
                commit_bt['state']=DISABLED
                yue_col=[username,pwd,paypwd,pranum,hbset]
                writcol(yue_col)
                pack_var.set('正在初始化...')
                self.eve=threading.Event()
                self.tasker=q_mon(self.eve,pack_var,commit_bt)
                self.tasker.setDaemon(True)
                self.tasker.start()
                sleep(2)
                self.eve.set()
            else:
                tkinter.messagebox.askokcancel("提示","所有项不可为空!")
     
        def stop_tb():
            self.eve.clear()
            commit_bt['state']=NORMAL
                    
        
        Label(self.root,width=7).grid(row=0,column=0)
        Label(self.root).grid(row=1,column=0)
        Label(self.root).grid(row=3,column=0)
        Label(self.root).grid(row=5,column=0)
        Label(self.root).grid(row=7,column=0)
        Label(self.root,text='红包面值可设置多个，使用英文逗号（,）隔开。',bd=5).grid(row=9,column=1,columnspan=3)
        Label(self.root).grid(row=11,column=0)
        Label(self.root,text="雅堂帐户:",bd=5).grid(row=0,column=1)
        Label(self.root,text="帐户密码:",bd=5).grid(row=2,column=1)
        Label(self.root,text="交易密码:",bd=5).grid(row=4,column=1)
        Label(self.root,text="使用红包倍数:",bd=5).grid(row=6,column=1)
        Label(self.root,text="当前动作:",bd=5,font="华康少女字体,16").grid(row=12,column=1,rowspan=2)
        Label(self.root,text="使用红包面值:",bd=5).grid(row=8,column=1)
        
        hb_var=StringVar()
        Entry(self.root,textvariable=hb_var,bd=5).grid(row=8,column=2)
        hb_var.set(col_list[4])
        
        
        pack_var=StringVar()
        Label(self.root,bd=5,textvariable=pack_var,font=16,fg='green').grid(row=12,column=2,rowspan=2,columnspan=2)
        pack_var.set('设置投资信息...')
        
        username_var=StringVar()
        Entry(self.root,textvariable=username_var,bd=5).grid(row=0,column=2,columnspan=2)
        username_var.set(col_list[0])
        
        pwd_var=StringVar()
        Entry(self.root,textvariable=pwd_var,show='*',bd=5).grid(row=2,column=2,columnspan=2)
        pwd_var.set(col_list[1])
        
        paypwd_var=StringVar()
        Entry(self.root,textvariable=paypwd_var,bd=5).grid(row=4,column=2,columnspan=2)
        paypwd_var.set(col_list[2])
    
        pranum_var=StringVar()
        Entry(self.root,textvariable=pranum_var,bd=5).grid(row=6,column=2,columnspan=2)
        pranum_var.set(col_list[3])    
        
        
        commit_bt=Button(self.root,text="开始抢标",command=click_on,bg="green",width=15,fg="blue",bd=5)
        commit_bt.grid(row=10,column=2,columnspan=2)
        stop_bt=Button(self.root,text="停止抢标",command=stop_tb,bg="red",width=15,fg="blue",bd=5,state=DISABLED)
        stop_bt.grid(row=10,column=1)            
        self.root.mainloop()
if __name__=='__main__':
    #apr=reque_num(4000)
    #print(apr)
    yue=yuebiao_gui()
    yue.main_go()

    




