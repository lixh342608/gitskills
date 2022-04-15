#coding=utf-8


from command.Base import *
import pyautogui
import time





if __name__=="__main__":
    hwnd=Hwnd()
    my_hwnds=hwnd.get_hwnd()
    for key in my_hwnds.keys():
        hwndbase=myBase(int(key))
        #hwndbase.get_scene()
        #hwndbase.getpic_click("wuyi1.PNG","aswuyi.PNG")
        #hwndbase.getpic_click("wuyidh1.PNG","aswuyi.PNG",check_tag=False,confidence=0.8)
        hwndbase.positioning("jianye",211,100)
