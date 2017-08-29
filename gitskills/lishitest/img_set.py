#coding=utf-8
'''
Created on 2017年6月15日

@author: Administrator
'''
'''import platform
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart  
from email.utils import parseaddr, formataddr
from email.mime.base import MIMEBase
import smtplib,os

xinxi=platform.node()+platform.platform()

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
class sendmeil:
    def __init__(self):
        #self._file=_file
        #self.filename=os.path.split(self._file)[1]
        #self.ext=os.path.splitext(self._file)[1].replace('.','')
        self.from_addr = "li_xianghuay@163.com"
        self.password = "ri123654"#"mxzgoepapvimcahj"
        self.to_addr = "zijinshanmao@163.com"
        self.smtp_server = "smtp.163.com"
        
        self.add_att=[]
    def add_from(self,fileph):
        filename=os.path.split(fileph)[1]
        #ext=os.path.splitext(fileph)[1].replace('.','')
        att = MIMEBase('application', 'octet-stream')  
        att.set_payload(open(fileph, 'rb').read())  
        att.add_header('Content-Disposition', 'attachment', filename=('gbk','',filename) )  
        encoders.encode_base64(att)  
  
        self.add_att.append(att)
    def msg_set(self,codstr):
        msg = MIMEMultipart('alternative')  
        msg['From'] = _format_addr('月半弯 <%s>' % self.from_addr)
        msg['To'] = _format_addr('管理员 <%s>' % self.to_addr)
        msg['Subject'] = Header('来自花儿的问候……', 'utf-8').encode()
        msg.attach(MIMEText(codstr, 'plain', 'utf-8'))    
        for att in self.add_att:
            msg.attach(att)
        
        return msg
    def sendmile(self):
        codstr=platform.node()+platform.platform()
        msg=self.msg_set(codstr)
        server = smtplib.SMTP(self.smtp_server, 25)
        #server.set_debuglevel(1)
        server.login(self.from_addr, self.password)
        try:
            server.sendmail(self.from_addr, [self.to_addr],msg.as_string())
            server.quit()
            return True
        except Exception as e:
            server.quit()
            print(e)
            return False  

if __name__=='__main__':
    mm=sendmeil()
    mm.sendmile()'''
    
    
    

from PIL import Image,ImageEnhance
import pytesseract,re,requests,json
from selenium import webdriver
from selenium.webdriver.support.select import Select
from time import sleep
from time_out import waittime
def img_set(driver,wait):
    driver.save_screenshot('f://aa.png')  #截取当前网页，该网页有我们需要的验证码
    imgelement = wait.visibility('name','validate')  #定位验证码
    location = imgelement.location  #获取验证码x,y轴坐标
    size=imgelement.size  #获取验证码的长宽
    rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) #写成我们需要截取的位置坐标
    i=Image.open("f://aa.png") #打开截图
    frame4=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
    imgry = frame4.convert('L')#图像加强，二值化
    sharpness =ImageEnhance.Contrast(imgry)
    sharp_img = sharpness.enhance(2.0)
    sharp_img.save("f:/image_code.jpg")
    text=pytesseract.image_to_string(sharp_img) #使用image_to_string识别验证码
    text = re.sub("\W", "", text)
    return text
def login(driver,username,pwd):
    driver.get('https://jr.yatang.cn/NewLogin/index/referer/')
    wait=waittime(driver,20)
    wait.visibility('css', '#username').send_keys(username)

    wait.visibility('css', '#password').send_keys(pwd)
    yzm=img_set(driver,wait)
    wait.visibility('name', 'sendnumber').send_keys(yzm)
    select = wait.visibility('id', 'cookietime')
    Select(select).select_by_value('7200')
    wait.clickable('css', '#button').click()
    sleep(1)
    if '登录' in driver.title:
        login(driver,username,pwd)
    return driver
    '''login_ele=driver.find_element_by_xpath('//*[@id="top"]/div[1]/div/div[2]/a[2]')
    if login_ele and login_ele.text=='免费注册':
        login()
    else:
        print('登陆成功')'''
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

if __name__=='__main__':
    driver=webdriver.Chrome('C:/chromedriver')
    driver.maximize_window()
    driver.get('https://jr.yatang.cn/NewLogin/index/referer/')
    login(driver,'月光宝盒','ri123654')
    sleep(5)
    '''apr_num=reque_num(50)
    url='https://jr.yatang.cn/Invest/ViewBorrow/ibid/%s' % apr_num
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="amountt"]').send_keys(50)
    driver.find_element_by_xpath('//*[@id="incheck"]').click()
    sleep(5)
    driver.find_element_by_xpath('//*[@id="ppay"]').send_keys('aaa111')
    yzm=img_set(driver)
    print('验证码是：%s' % yzm)
    frame4=Image.open('f:/aa.jpg')
    imgry = frame4.convert('L')#图像加强，二值化
    sharpness =ImageEnhance.Contrast(imgry)
    sharp_img = sharpness.enhance(2.0)
    sharp_img.save("f:/image_code.jpg")
    
    text=pytesseract.image_to_string(sharp_img) #使用image_to_string识别验证码
    #text=re.sub("\W", "", text)
    print(text)'''