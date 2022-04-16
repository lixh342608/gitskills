#coding=utf-8


from command.Base import *
import pyautogui
import time





if __name__=="__main__":
    hwnd=Hwnd()
    my_hwnds=hwnd.get_hwnd()
    for key in my_hwnds.keys():
        print(my_hwnds.get(key))
        hwndbase=myBase(int(key))
        print(hwndbase.parent_size)
        #hwndbase.get_scene()
        #while True:
            #hwndbase.getpic_click("wuyi1.PNG","aswuyi.PNG")
            #hwndbase.getpic_click("wuyidh1.PNG","aswuyi.PNG",check_tag=False,confidence=0.8)
        #hwndbase.positioning("jianye",90,80)
        #hwndbase.shiyongwupin("baozi1.PNG")
        for i in range(10):
            hwndbase.huangdang("donghaiwan")
            print("jieshu1ci")
