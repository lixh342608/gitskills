#coding=utf-8
'''
Created on 2017年6月16日

@author: Administrator
'''
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import pickle,threading
from time_out import waittime
from tkinter import *
from img_set import img_set
import tkinter.messagebox
import requests,platform,time,sys,os

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
    #print(main_num)
    time.sleep(1.5)
    url='https://jr.yatang.cn/Financial/getAssetList'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'}

    data={}
    data['aprrange']='0'
    data['selectdate']='2'
    data['repaystyle']='0'
    data['goto_page']=''
    data['page_href']='/Financial/getAssetList?&p=1'
    resq=requests.post(url,data=data,headers=headers,cookies=cookie_dict)
    t_text=resq.json()['list']
    print(t_text)
    #t_text=json.loads(resq.text)['list']
    t_text=[i for i in t_text if i['showday']=='1个月' and i['remain'] >= main_num and float(i['apr']) >= 5.0]# and i['borrow_type'] != '10']
    print(t_text)
    rema=0
    apr_num=0
    for j in t_text:
        if int(j['remain'])>rema:
            rema=int(j['remain'])
            apr_num=j['id']
    
    return apr_num   

class q_mon(threading.Thread):
    def __init__(self,eve,msg_var,commit_bt,miao_bt,stop_bt):
        super(q_mon,self).__init__()
        self.eve=eve
        self.msg_var=msg_var
        self.commit_bt=commit_bt
        self.miao_bt=miao_bt
        self.stop_bt=stop_bt
        self.nopar=[]
        self.yuecol=loadcol()
        self.username=self.yuecol[0]#用户名
        self.pwd=self.yuecol[1]#用户密码
        self.paypwd=self.yuecol[2]#支付密码
        self.par_num=int(self.yuecol[3])#红包倍数
        self.parsex_list=self.yuecol[4].split(',')#红包面值'''

        self.driver=webdriver.Chrome('C:/chromedriver')
        self.driver.get('https://jr.yatang.cn/Financial/asset')
        
        self.driver.maximize_window()
        self.wait=waittime(self.driver,20)
        self.login()
    def run(self):
        self.eve.wait()
        self.q_mont()
         
    def login(self):
        self.driver.get('https://jr.yatang.cn/NewLogin/index/referer/')
        self.driver.switch_to.frame(0)
        self.wait.visibility('xpath', '//*[@id="js-username"]').send_keys(self.username)

        self.wait.visibility('xpath', '//*[@id="js-password"]').send_keys(self.pwd)
        select=self.wait.visibility('id','_cache_time')
        Select(select).select_by_value('7200')

        self.wait.clickable('xpath', '//*[@id="js-login"]').click()

        time.sleep(2)
        '''login_ele = self.wait.get_ele('xpath', '//*[@id="root"]/div/div[1]/div/div[1]/div/div[2]/ul/li[1]/a[2]')

        if login_ele and login_ele.text=='免费注册':
            self.login()
        else:'''
        self.msg_var.set('登陆成功')
        cookie_list=self.driver.get_cookies()
        #if os.path.exists('cookie.yt'):
            #os.remove('cookie.yt')
        global cookie_dict
        cookie_dict={}
        for cookie in cookie_list:
            if 'name' in cookie and 'value' in cookie:
                cookie_dict[cookie['name']]=cookie['value']


    def q_mont(self):

        if not self.eve.is_set():
            self.msg_var.set("已结束任务！")
            self.chnge_bt()
            self.driver.quit()
            sys.exit(1)
        #检测登录
        '''self.msg_var.set("检测登录状态...")
        login_ele=self.wait.get_ele('xpath','//*[@id="root"]/div/div[1]/div/div[1]/div/div[2]/ul/li[1]/a[2]')
        if login_ele and login_ele.text=='免费注册':
            self.msg_var.set("正在准备登录...")
            self.login()'''
        self.msg_var.set("正在寻找月标...")
        #循环直到找到为止
        apr_num=0
        while int(apr_num)==0:
                
            if not self.eve.is_set():
                self.msg_var.set("已结束任务！")
                self.chnge_bt()
                self.driver.quit()
                sys.exit(1)
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
        if self.driver.current_url != url:
            img_set(self.driver)
            strcommand='tesseract.exe '+"f:/image_code.png "+'f:/inputs -l num'
            print(strcommand)
            os.system(strcommand)
            with open('f:/inputs.txt','r',encoding='UTF-8') as f:

                print(f.readline())
            time.sleep(5)
        try:
            mynum=self.wait.visibility('xpath','//*[@id="amountt"]')
            hbxs_ele=self.wait.visibility('class','hbje_xs')
        except Exception:
            self.q_mont()

        if mynum:
            if hbxs_ele:
                #print(mynum.get_attribute('value'),hbxs_ele.text.split('\n'))
                if mynum.get_attribute('value')==str(main_num) and hbxs_ele.text.split('\n')[0]==str(parsex):
                    self.msg_var.set("红包已准备完毕")
                    self.biaochu()
                else:
                    if self.select_hb(main_num,parsex):
                        self.biaochu()
            else:
                balance_ele=self.wait.visibility('class','right_box1')
                balance=re.findall('\d.+\d',balance_ele.text)[0].replace(',','').split('.')[0]
                if int(balance)<main_num:
                    self.msg_var.set("帐户可投资金不足，退出投标！")
                    self.chnge_bt()
                    self.driver.quit()
                    sys.exit(1)
                else:
                    self.msg_var.set("项目可投资金不足，重新抢标！")

        else:
            self.msg_var.set("项目可能已结束，重新抢标！")




        self.q_mont()


    def select_hb(self,main_num,parsex):
        mynum=self.wait.visibility('xpath','//*[@id="amountt"]')
        hbxs_ele=self.wait.visibility('class','hbje_xs')

        mynum.clear()
        mynum.send_keys(main_num)
        #查找红包选框
        hbxs_ele.click()
        #找到红包盒子
        ele_box=self.wait.visibility('class','hb_xl_box')
            #找到盒子中所有红包
        hb_list=self.driver.find_elements_by_class_name('hb_check_list')

        for hb in hb_list:
            hb_li=hb.text.replace('元','').split('\n')

            #如果红包等于预期红包且投资金额等于预期投资金额则选中该红包
            if int(hb_li[0])==parsex and int(hb_li[1])==main_num:
                hb.find_element_by_class_name('hbcheck_1').click()
            else:
                continue

        if mynum.get_attribute('value')==str(main_num) and hbxs_ele.text=='%d元' % parsex:
            self.msg_var.set("红包已准备完毕")

            return True
        else:
            tkinter.messagebox.showinfo('报告', '没有找到%d元面值红包，怪不得宝宝了' % parsex)
            self.nopar.append(parsex)
            if len(self.nopar)==len(self.parsex_list):
                tkinter.messagebox.showinfo('报告', '没有找到%d元面值红包，即将退出抢标' % parsex)
                self.chnge_bt()
                self.driver.quit()
                sys.exit(1)
            else:
                return False



    def biaochu(self):
        self.wait.clickable('xpath','//*[@id="incheck"]').click()
        pay_ele=self.wait.visibility('xpath','//*[@id="ppay"]')
        if pay_ele!=None:
        
            pay_ele.send_keys(self.paypwd)
            self.wait.clickable('xpath','//*[@id="button"]').click()
            ti_mm=5
            while ti_mm>=0:
                self.msg_var.set('投标已进入队列，\n等待15秒（%d）' % ti_mm)
                time.sleep(1)
                ti_mm-=1
            
    def chnge_bt(self):
        self.commit_bt['state']=NORMAL
        self.stop_bt['state']=DISABLED
        self.miao_bt['state']=NORMAL


class lishitest(threading.Thread):
    def __init__(self,eve,msg_var,commit_bt,miao_bt,stop_bt,miao_num=None):
        super(lishitest, self).__init__()
        self.eve=eve
        self.msg_var=msg_var
        self.commit_bt=commit_bt
        self.miao_bt=miao_bt
        self.stop_bt=stop_bt
        self.miao_num=miao_num
        self.yuecol=loadcol()
        self.username=self.yuecol[0]#用户名
        self.pwd=self.yuecol[1]#用户密码
        self.paypwd=self.yuecol[2]#支付密码
        self.driver = webdriver.Chrome('C:/chromedriver')
        #self.driver.get('https://jr.yatang.cn/NewLogin/index/referer/')
        self.check_zt=False
        self.driver.maximize_window()
        self.wait = waittime(self.driver, 20)
        self.login()
    def run(self):
        self.eve.wait()
        self.miao_main()
    def miao_main(self):
        pac = self.timeset()
        if pac==0:
            self.msg_var.set("正在投资准备...")
            self.giter()
        else:
            self.driver.quit()

    def lishinum(self):
        pr_ele = self.wait.presence('class', 'wf_move_box')
        if not pr_ele:
            return '0'
        ele_list = pr_ele.find_elements_by_class_name('wf_list_box')
        ele_list = filter(lambda x: x.get_attribute('iborrowid') != '0', ele_list)
        lishinumer = 0
        ele_praser = 0
        for i in ele_list:
            ele = i.find_element_by_class_name('wf_xq_lv')
            ele_pra = int(re.sub('\W', '', ele.text))
            if ele_pra > ele_praser:
                ele_praser = ele_pra
                lishinumer = i.get_attribute('iborrowid')
        return lishinumer

    def set_xpath(self, lishinumer):
        self.numer_xpath = '//*[@id="amountt_%s"]' % lishinumer
        self.check_xpath = '//*[@id="incheck_%s"]' % lishinumer
        self.ppay_xpath = '//*[@id="ppay_%s"]' % lishinumer
        self.commit_xpath = '//*[@id="button_%s"]' % lishinumer
        self.withdra_class = 'aj_withdrawalCash_%s' % lishinumer
        self.time_class = 'lefttime_%s' % lishinumer

    def login(self):
        self.driver.get('https://jr.yatang.cn/NewLogin/index/referer/')
        self.driver.switch_to.frame(0)
        self.wait.visibility('xpath', '//*[@id="js-username"]').send_keys(self.username)

        self.wait.visibility('xpath', '//*[@id="js-password"]').send_keys(self.pwd)
        select=self.wait.visibility('id','_cache_time')
        Select(select).select_by_value('7200')

        self.wait.clickable('xpath', '//*[@id="js-login"]').click()

        time.sleep(2)
        login_ele = self.wait.get_ele('xpath', '//*[@id="top"]/div[1]/div/div[2]/a[2]')
        print(login_ele)

        if login_ele!=0 and login_ele.text == '免费注册':
            self.login()
        else:
            self.driver.get('https://jr.yatang.cn/Financial/welfare')
    def wrrtenum(self, numer):
        if numer == None:
            dra_text = self.wait.presence('class', self.withdra_class).text

            numer = int(float(dra_text.strip('￥').replace(',', '')))

        self.wait.visibility('xpath', self.numer_xpath).send_keys(numer)

    def giter(self):
        self.wrrtenum(self.miao_num)
        ele = self.wait.clickable('xpath', self.check_xpath)
        ele.click()

        self.miaochu()

    def miaochu(self):
        pay_ele = self.wait.visibility('xpath', self.ppay_xpath)
        pay_ele.send_keys(self.paypwd)
        commit_ele = self.wait.clickable('xpath', self.commit_xpath)
        commit_ele.click()
        self.msg_var.set('投资已进入队列，正在获取投资结果...')
        check_ele = self.wait.visibility('xpath','/html/body/div[5]/div/div/div/div[1]/div[1]/b')
        self.msg_var.set(check_ele.text)
    def tsleep(self,ti_sum,timer):
        while timer>0:
            try:
                check_text=self.driver.find_element_by_xpath(self.check_xpath)
                if check_text.is_displayed():

                    self.check_zt=True
                    break
                else:
                    self.msg_var.set('距离投秒时间还有%d秒，\n%d秒后刷新...' % (ti_sum,timer))
                    time.sleep(0.95)
                    timer-=1
            except Exception as e:
                print(e)


    def timeset(self):
        lishinumer = self.lishinum()
        if lishinumer == '0':
            self.msg_var.set('没有可投秒标！')
            tkinter.messagebox.showinfo('报告', '没有可投秒标！')
            try:
                sys.exit(0)
            except:
                self.msg_var.set('程序准备退出！')
                tkinter.messagebox.showinfo('报告', '程序准备退出！')
            finally:
                self.chnge_bt()
                self.msg_var.set('设置投资信息...')
                return 2
        self.set_xpath(lishinumer)

        while True:
            if not self.eve.is_set():
                self.msg_var.set("已结束任务！")
                self.chnge_bt()
                self.driver.quit()
                sys.exit(1)
            if self.check_zt==True:
                break
            self.driver.refresh()

            ti_text = self.wait.get_ele('class', self.time_class).text
            ti_list = ti_text.split(':')
            if '天' in ti_list[0]:
                hour_list=ti_list[0].split('天')
                ti_list[0]=int(hour_list[0])*24+int(hour_list[1])
                #print(hour_list,ti_list[0])
            ti_sum = int(ti_list[0]) * 3600 + int(ti_list[1]) * 60 + int(ti_list[2])
            #ti_sum=int(ti_list[2])
            if ti_sum > 600:
                self.tsleep(ti_sum,300)
                continue
            elif ti_sum > 300:
                self.tsleep(ti_sum,150)
                continue
            elif ti_sum > 200:
                self.tsleep(ti_sum,90)
                continue
            elif ti_sum > 50:
                self.tsleep(ti_sum,28)
                continue
            elif ti_sum > 10:
                self.tsleep(ti_sum,5)
                continue
            elif ti_sum > 5:
                self.tsleep(ti_sum,ti_sum - 3)
                continue
            else:
                break
        return 0
    def chnge_bt(self):
        self.commit_bt['state']=NORMAL
        self.stop_bt['state']=DISABLED
        self.miao_bt['state']=NORMAL
class yuebiao_gui:
    def __init__(self):
        #self.plat='Z6NRQGUFOYCRJGFWindows-7-6.1.7601-SP1'#dell
        self.plat='WIN-20170212KKHWindows-7-6.1.7601-SP1'#本机
        #self.plat='DESKTOP-JMLPBFMWindows-10-10.0.15063'#zzyt
        #self.plat='HY-201708142306Windows-7-6.1.7601-SP1'#上海雅堂


            
        self.root=Tk()
        self.root.wm_attributes("-topmost", 1)
        self.root.title('你值得拥有')
        width_n=self.root.winfo_screenwidth()/2-200
        height_n=self.root.winfo_screenheight()/2-200
        self.root.geometry('400x500+%d+%d' % (int(width_n),int(height_n)))


    
    
    def main_go(self):
        
        col_list=loadcol()
        if col_list==0:
            col_list=["","","","",""]

        def yue_click_on():
            if platform.node()+platform.platform()!=self.plat:
                tkinter.messagebox.showerror('运行出错','此程序不可在此计算机上运行！')
                return
            
            username=username_var.get()
            pwd=pwd_var.get()
            paypwd=paypwd_var.get()
            pranum=pranum_var.get()
            hbset=hb_var.get()
            if username and pwd and paypwd and pranum and hbset:
                stop_bt['state']=NORMAL
                commit_bt['state']=DISABLED
                miao_bt['state'] = DISABLED
                yue_col=[username,pwd,paypwd,pranum,hbset]
                writcol(yue_col)
                pack_var.set('正在初始化...')
                self.eve=threading.Event()
                self.tasker=q_mon(self.eve,pack_var,commit_bt,miao_bt,stop_bt)
                self.tasker.setDaemon(True)
                self.tasker.start()
                time.sleep(2)
                self.eve.set()
            else:
                tkinter.messagebox.askokcancel("提示","缺少有用设置信息，请检查！")
        def miao_click_on():
            if platform.node()+platform.platform()!=self.plat:
                tkinter.messagebox.showerror('运行出错','此程序不可在此计算机上运行！')
                return
            username=username_var.get()
            pwd=pwd_var.get()
            paypwd=paypwd_var.get()
            miao_num=miao_var.get()
            if username and pwd and paypwd:
                stop_bt['state']=NORMAL
                commit_bt['state']=DISABLED
                miao_bt['state'] = DISABLED
                yue_col=[username,pwd,paypwd,'','']
                writcol(yue_col)
                if not miao_num:
                    miao_num=None
                pack_var.set('正在初始化...')
                self.eve=threading.Event()
                self.tasker=lishitest(self.eve,pack_var,commit_bt,miao_bt,stop_bt,miao_num)
                self.tasker.setDaemon(True)
                self.tasker.start()
                time.sleep(2)
                self.eve.set()


        def stop_tb():
            self.eve.clear()
            stop_bt['state'] = DISABLED
            commit_bt['state']=NORMAL
            miao_bt['state'] = NORMAL
        
        Label(self.root,width=7).grid(row=0,column=0)
        Label(self.root).grid(row=1,column=0)
        Label(self.root).grid(row=3,column=0)
        Label(self.root).grid(row=5,column=0)
        Label(self.root).grid(row=7,column=0)
        Label(self.root,text='红包面值可设置多个，使用英文逗号（,）隔开。\n红包设置只在投资月标时生效！',bd=5).grid(row=9,column=1,columnspan=3)
        Label(self.root,text='投秒资金只在投资秒标时生效！').grid(row=11,column=1,columnspan=3)
        Label(self.root,text="雅堂帐户:",bd=5).grid(row=0,column=1)
        Label(self.root,text="帐户密码:",bd=5).grid(row=2,column=1)
        Label(self.root,text="交易密码:",bd=5).grid(row=4,column=1)
        Label(self.root,text="使用红包倍数:",bd=5).grid(row=6,column=1)
        Label(self.root,text="当前动作:",bd=5,font="华康少女字体,16").grid(row=14,column=1,rowspan=2)
        Label(self.root,text="使用红包面值:",bd=5).grid(row=8,column=1)
        Label(self.root, text="投秒资金:", bd=5).grid(row=10, column=1)
        
        hb_var=StringVar()
        Entry(self.root,textvariable=hb_var,bd=5).grid(row=8,column=2,columnspan=2)
        hb_var.set(col_list[4])
        
        
        pack_var=StringVar()
        Label(self.root,bd=5,textvariable=pack_var,font=16,fg='green').grid(row=14,column=2,rowspan=2,columnspan=2)
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

        miao_var=StringVar()
        Entry(self.root,textvariable=miao_var,bd=5).grid(row=10,column=2,columnspan=2)
        miao_var.set('')
        
        
        commit_bt=Button(self.root,text="我要抢标",command=yue_click_on,bg="green",width=10,fg="blue",bd=5)
        commit_bt.grid(row=12,column=2)
        stop_bt=Button(self.root,text="停止抢标",command=stop_tb,bg="red",width=10,fg="blue",bd=5,state=DISABLED)
        stop_bt.grid(row=12,column=1)
        miao_bt = Button(self.root, text="我要抢秒", command=miao_click_on, bg="green", width=10, fg="blue", bd=5)
        miao_bt.grid(row=12, column=3)
        self.root.mainloop()
if __name__=='__main__':
    #apr=reque_num(4000)
    #print(apr)
    yue=yuebiao_gui()
    yue.main_go()

    




