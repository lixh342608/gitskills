#coding=utf-8
'''
Created on 2016年3月1日

@author: admin
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException,WebDriverException,ElementNotVisibleException
"""关于本类get_ele函数：元素定位方式错误、定位出错或超时给出错误信息返回0，
正常返回定位到的对象（element）。"""

class waittime:
    def __init__(self,driver,timeout=30):
        self.driver=driver
        self.wait=WebDriverWait(self.driver,timeout)
    def get_ele(self,fashion,value):
        #条件识别定位方法
        if fashion.lower()=="id":#ID方法定位元素
            funtion=lambda x:x.find_element_by_id(value)
            
        elif fashion.lower()=="name":#NAME方法定位元素
            funtion=lambda x:x.find_element_by_name(value)
        elif fashion.lower()=="xpath":#XPATH方法定位元素
            funtion=lambda x:x.find_element_by_xpath(value)
        elif fashion.lower()=="class":#class_name方法定位元素
            funtion=lambda x:x.find_element_by_class_name(value)
        elif fashion.lower()=="css":#css_selector方法定位元素
            funtion=lambda x:x.find_element_by_css_selector(value)
        elif fashion.lower()=="tag":#tag_name方法定位元素
            funtion=lambda x:x.find_element_by_tag_name(value)
        elif fashion.lower()=="link":#link_text方法定位元素
            funtion=lambda x:x.find_element_by_link_text(value)
        elif fashion.lower()=="partial":#partial_link_text方法定位元素(匹配链接的部分文字)
            funtion=lambda x:x.find_element_by_partial_link_text(value)
        else:
            print("定位方式无效,执行关闭浏览器窗口！")
            return 0
        try:
            element=self.wait.until(funtion)
            return element
        except TimeoutException:
            print("定位元素超时!信息：%s" % value)
            return 0
        except NoSuchElementException:
            print("没有找到元素!信息：%s" % value)
            return 0
        except ElementNotVisibleException:
            print("元素不可见！信息：%s" % value)
            return 0
        except Exception:
            print("程序出现错误!信息：%s" % value)
            return 0
    def change_fashion(self,fashion):
        if fashion.lower()=="id":#ID方法定位元素
            return By.ID
            
        elif fashion.lower()=="name":#NAME方法定位元素
            return By.NAME
        elif fashion.lower()=="xpath":#XPATH方法定位元素
            return By.XPATH
        elif fashion.lower()=="class":#class_name方法定位元素
            return By.CLASS_NAME
        elif fashion.lower()=="css":#css_selector方法定位元素
            return By.CSS_SELECTOR
        elif fashion.lower()=="tag":#tag_name方法定位元素
            return By.TAG_NAME
        elif fashion.lower()=="link":#link_text方法定位元素
            return By.LINK_TEXT
        elif fashion.lower()=="partial":#partial_link_text方法定位元素(匹配链接的部分文字)
            return By.PARTIAL_LINK_TEXT
        else:
            print("定位方式无效！")
            return 0
    #有效时间内控件是可见，可见返回元素，不可见提示超时信息
    def visibility(self,fashion,value):
        try:
            BY=self.change_fashion(fashion)
            ele=self.wait.until(EC.visibility_of(self.driver.find_element(by=BY,value=value)))
            return ele
        except TimeoutException:
            print('定位元素超时',value)
            return None
        except NoSuchElementException:
            print('没有找到指定元素',value)
            return None
    #有效时间内定位到控件，返回元素，超时提示超时信息    
    def presence(self,fashion,value):
        try:
            BY=self.change_fashion(fashion)
            ele=self.wait.until(EC.presence_of_element_located((BY,value)))
            return ele
        except TimeoutException:
            print('定位元素超时',value)
            return None
        except NoSuchElementException:
            print('没有找到指定元素',value)
            return None
    #有效时间内定位到元素并且为可点击状态，并返回元素，否则提示超时信息
    def clickable(self,fashion,value):
        try:
            BY=self.change_fashion(fashion)
            ele=self.wait.until(EC.element_to_be_clickable((BY,value)))
            return ele
        except TimeoutException:
            print('定位元素超时',value)
            return None
        except NoSuchElementException:
            print('没有找到指定元素',value)
            return None

if __name__=="__main__":

    
    driver=webdriver.Chrome('C:/chromedriver')
    driver.get('https://www.baidu.com/')
    driver.maximize_window()
    #driver.switch_to.frame(0)
    wait=WebDriverWait(driver,10)
    ele=wait.until(EC.presence_of_element_located((By.ID,'aw')))
    ele.send_keys('月光宝盒')
    print(ele)
    '''wait=waittime(driver,30)
    wait.get_ele('xpath','//*[@id="js-username"]').send_keys('月光宝盒')
    if ele==0:
        driver.quit()
    else:
        ele.send_keys("cheese")'''
