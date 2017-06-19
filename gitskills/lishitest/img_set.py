#coding=utf-8
'''
Created on 2017年6月15日

@author: Administrator
'''
from PIL import Image
import pytesseract,re
from selenium import webdriver
from asyncio.tasks import sleep

def img_set(driver):
    driver.save_screenshot('f://aa.png')  #截取当前网页，该网页有我们需要的验证码
    imgelement = driver.find_element_by_xpath('//*[@id="form1"]/div[4]/div/img')  #定位验证码
    location = imgelement.location  #获取验证码x,y轴坐标
    size=imgelement.size  #获取验证码的长宽
    rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) #写成我们需要截取的位置坐标
    i=Image.open("f://aa.png") #打开截图
    frame4=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域

    text=pytesseract.image_to_string(frame4) #使用image_to_string识别验证码
    text=re.sub("\W", "", text)
    return text
