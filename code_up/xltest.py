#coding=utf-8
'''
Created on 2016年10月14日

@author: pc
'''
from pymouse import PyMouse
def single_click(m,x,y,but=1,n=1):
    for i in range(1):
        m.press(x,y,button=but)
        #m.release(x,y,button=but)


import pyautogui

pyautogui.moveTo((200,200))

pyautogui.hotkey("alt","c")

    
if __name__=="__main__":
    #m=PyMouse()
    #m.move(30,230)
    #m.click(30,230,1,1)
    pass
