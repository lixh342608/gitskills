#coding=utf-8
'''
Created on 2016年10月14日

@author: pc
'''
from pymouse import PyMouse
import pyautogui
import difflib
import time
print(pyautogui.size())
while True:
    img=pyautogui.position()
    print(img)
    print(img.x,img.y)
    time.sleep(1)




