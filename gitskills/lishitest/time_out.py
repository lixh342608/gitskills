#coding=utf-8
'''
Created on 2016年3月1日

@author: admin
'''
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
        except TimeoutException as e:
            print("定位元素超时!")
            return 0
        except NoSuchElementException as e:
            print("没有找到元素!")
            return 0
        except ElementNotVisibleException as e:
            print("元素不可见！")
            return 0
        except Exception as e:
            print("程序出现错误!")
            return 0
        
        
if __name__=="__main__":
    from selenium import webdriver
    
    driver=webdriver.Chrome()
    driver.get("http://www.baidu.com")
    driver.maximize_window()
    wait=waittime(driver,30)
    ele=wait.get_ele('xpath','//*[@id="ss"]')
    if ele==0:
        driver.quit()
    else:
        ele.send_keys("cheese")
