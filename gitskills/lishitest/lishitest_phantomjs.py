#coding=utf-8
'''
Created on 2017年6月12日

@author: Administrator
'''
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import pickle,threading,queue
from time_out import waittime
from tkinter import *
import tkinter.messagebox


#que=queue.Queue()

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

class lishitest(threading.Thread):
    def __init__(self,que,msg_var,tdriver,ele_path):
        super(lishitest,self).__init__()
        self.que=que
        self.msg_var=msg_var
        self.tdriver=tdriver
        self.ele_path=ele_path
    def run(self):
        while True:
            task_msg=self.que.get()
            if isinstance(task_msg, str) and task_msg=='start':
                self.col=loadcol()
                self.start_br()
                
                self.start_click()
                
            elif isinstance(task_msg, str) and task_msg=='quit':
                pass
            else:
                pass
            
    def start_br(self):
        self.msg_var.set('正在启动浏览器...')
        self.driver=webdriver.PhantomJS()
        #self.driver=webdriver.Chrome('C:/chromedriver')
        self.driver.get('https://jr.yatang.cn/Financial/welfare')
        self.driver.maximize_window()
        self.wait=waittime(self.driver,10)
        self.msg_var.set('启动浏览器成功，正在检测登录状态...')
    def refash_t(self,ti_sum,wait_t):
        self.msg_var.set('浏览器将在倒计时%s刷新。' % self.fomat_t(ti_sum-wait_t))
        sleep(wait_t)
        
    def timeset(self):   
        while True:
            self.tdriver.refresh()
            self.driver.refresh()
            login_ele=self.wait.get_ele('xpath','//*[@id="top"]/div[1]/div/div[2]/a[2]')
            if login_ele.text=='免费注册':
                self.msg_var.set('检测登录状态失败，准备登录...')
                self.login()
                self.driver.get('https://jr.yatang.cn/Financial/welfare')
            ti_text=self.tr_time()
            ti_list=ti_text.split(':')
            print(ti_text,ti_list)
            ti_sum=int(ti_list[0])*3600+int(ti_list[1])*60+int(ti_list[2])
            
            #self.pack_var.set('距离投秒时间还有%d秒,等待刷新。' % ti_sum)
            if ti_sum>600:
                self.refash_t(ti_sum, 60)
                
                continue
            elif ti_sum>300:
                self.refash_t(ti_sum, 60)
                continue
            elif ti_sum>200:
                self.refash_t(ti_sum,60)
                continue
            elif ti_sum>50:
                self.refash_t(ti_sum,30)
                continue
            elif ti_sum>10:
                self.refash_t(ti_sum,5)
                continue
            elif ti_sum>5:
                self.refash_t(ti_sum,ti_sum-2)
                continue
            else:
                break
    def tr_time(self):
        ti_text=self.driver.find_element_by_class_name(self.ele_path['time_class']).text
        return ti_text
    def login(self):
        self.driver.get('https://jr.yatang.cn/NewLogin/index/referer/')
        self.driver.switch_to.frame(0)
        self.persi_ele('//*[@id="js-username"]').send_keys(self.col[0])
        
        self.persi_ele('//*[@id="js-password"]').send_keys(self.col[1])
        
        
        self.persi_ele('//*[@id="js-login"]').click()
        
        sleep(2)
        login_ele=self.wait.get_ele('xpath','//*[@id="top"]/div[1]/div/div[2]/a[2]')
        if login_ele and login_ele.text=='免费注册':
            self.login()
        else:
            self.msg_var.set('登陆成功')

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
    def wrrtenum(self,numer):
        if numer==None:
            dra_text=self.persi_ele(self.ele_path['withdra_class'], 'class').text
            
            numer=int(float(dra_text.strip('￥').replace(',','')))
                
            
        self.persi_ele(self.ele_path['numer_xpath']).send_keys(numer)
    def giter(self,pay_pwd,numer=None):
        self.wrrtenum(numer)
        ele=self.persi_ele(self.ele_path['check_xpath'])
        ele.click()
        self.miaochu(pay_pwd)
    def miaochu(self,pay_pwd):
        self.msg_var.set('正在抢投...')
        pay_ele=self.persi_ele(self.ele_path['ppay_xpath'])
        pay_ele.send_keys(pay_pwd)
        commit_ele=self.persi_ele(self.ele_path['commit_xpath'])
        commit_ele.click()
        
        sleep(10)
        try:
            check_ele=self.persi_ele('/html/body/div[5]/div/div/div/div[1]/div[1]/b')
            if '恭喜' in check_ele.text:
                self.msg_var.set('恭喜，已成功投资秒标！')
            else:
                self.msg_var.set('抱谦，可能是电脑或网络原因导致投秒未成功，下次再接再励！')
        except:
            self.msg_var.set('抱谦，可能是电脑或网络原因导致投秒未成功，下次再接再励！')


    def start_click(self):
        
        self.timeset()
        if self.col[3]:
            self.giter(self.col[2],self.col[3])
        else:
            self.giter(self.col[2])
    def fomat_t(self,timer):
        t_list=[]
        fomat_list=[3600,60,1]
        for t in fomat_list:
            if timer//t>=10:
                t_list.append(str(timer//t))
            else:
                t_list.append('0'+str(timer//t))
            timer=timer%t
        return ":".join(t_list)
class lishi_gui:
    def __init__(self):

        self.driver=webdriver.PhantomJS()
        self.driver.get('https://jr.yatang.cn/Financial/welfare')
        self.set_xpath()
        self.root=Tk()
        width_n=self.root.winfo_screenwidth()/2-200
        height_n=self.root.winfo_screenheight()/2-150
        self.root.geometry('350x300+%d+%d' % (int(width_n),int(height_n)))
    def lishinum(self):
        pr_ele=self.driver.find_element_by_class_name('wf_move_box')
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
        self.ele_path={}
        self.ele_path['numer_xpath']='//*[@id="amountt_%s"]' % lishinumer
        self.ele_path['check_xpath']='//*[@id="incheck_%s"]' % lishinumer
        self.ele_path['ppay_xpath']='//*[@id="ppay_%s"]' % lishinumer
        self.ele_path['commit_xpath']='//*[@id="button_%s"]' % lishinumer
        self.ele_path['withdra_class']='aj_withdrawalCash_%s' % lishinumer
        self.ele_path['time_class']='lefttime_%s' % lishinumer
    def tr_time(self):
        ti_text=self.driver.find_element_by_class_name(self.ele_path['time_class']).text
        return ti_text

    
    def trickit(self):
        try:
            tr_time=self.tr_time()
        except:
            sleep(3)
            tr_time=self.tr_time()
        self.time_lab.config(text=tr_time)
        self.root.update()
        self.time_lab.after(1000,self.trickit)
    def main_go(self):
        
        col_list=loadcol()
        if col_list==0:
            col_list=["","","",""]

        def click_on():
            commit_bt['state']=DISABLED
            username=username_var.get()
            pwd=pwd_var.get()
            paypwd=paypwd_var.get()
            pranum=pranum_var.get()
            if username and pwd and paypwd:
                col=[username,pwd,paypwd,pranum]
                writcol(col)
                self.pack_var.set('正在初始化...')
                self.que=queue.Queue()
                self.tasker=lishitest(self.que,self.pack_var,self.driver,self.ele_path)
                self.tasker.start()
                self.que.put('start')
            else:
                tkinter.messagebox.askokcancel("提示","除投资金额外所有项不可为空，如果有误将导致无法登录或抢秒时交易密码错误。")
     
    
        
        Label(self.root,width=7).grid(row=0,column=0)
        Label(self.root).grid(row=1,column=0)
        Label(self.root).grid(row=3,column=0)
        Label(self.root).grid(row=5,column=0)
        Label(self.root).grid(row=7,column=0)
        Label(self.root).grid(row=9,column=0)
        
        Label(self.root,text="雅堂帐户:",bd=5).grid(row=0,column=1)
        Label(self.root,text="帐户密码:",bd=5).grid(row=2,column=1)
        Label(self.root,text="交易密码:",bd=5).grid(row=4,column=1)
        Label(self.root,text="投资金额:",bd=5).grid(row=6,column=1)
        Label(self.root,text="当前动作:",bd=5).grid(row=9,column=1)
        Label(self.root,text="倒计时:",bd=5).grid(row=10,column=1)
        self.time_lab=Label(self.root,text="准备中",bd=5)

        self.time_lab.grid(row=10,column=2)
        self.time_lab.after(1000,self.trickit)
        
        self.pack_var=StringVar()
        Label(self.root,bd=5,textvariable=self.pack_var).grid(row=9,column=2,columnspan=3)
        self.pack_var.set('设置投资信息...')
        
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
        pranum_var.set("")    
        
        
        commit_bt=Button(self.root,text="开始抢秒",command=click_on,bg="red",width=15,fg="blue",bd=5)
        commit_bt.grid(row=8,column=2,columnspan=2)
            
        self.root.mainloop()

if __name__=='__main__':
    lishi=lishi_gui()
    lishi.main_go()

