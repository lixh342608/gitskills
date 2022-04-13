#coding=utf-8

import win32gui
import pyautogui
import ctypes
import random
import PIL,os,time
from pathlib import Path
from pymouse import PyMouse

class Hwnd():
    def get_hwnd_dic(self, hwnd, hwnd_title):
        if "梦幻西游 ONLINE" in win32gui.GetWindowText(hwnd):
            hwnd_title[f"{hwnd}"] = win32gui.GetWindowText(hwnd)

    def get_hwnd(self):
        '''
        :return: {hwnd:title}
        '''
        hwnd_title = {}
        win32gui.EnumWindows(self.get_hwnd_dic, hwnd_title)
        return hwnd_title
class myBase():
    def __init__(self,hwnd):
        self.hwnd=hwnd
        self.get_parent_size()
        currfiletpath = Path(os.path.abspath(__file__))
        self.currtpath=currfiletpath.parent
        self.mous=PyMouse()
    def grt_num_center(self,num1,num2):
        center_num=abs(num1-num2)//2
        if num1 > num2:
            return num2+center_num
        else:
            return num1+center_num

    def get_parent_size(self):
        print(self.hwnd)
        win32gui.SetForegroundWindow(self.hwnd)
        #time.sleep(2)
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        #left, top, right, bottom = self.get_window_rect()
        self.parent_size = (left, top, right, bottom)
        self.dows_center=(self.grt_num_center(left,right),self.grt_num_center(top,bottom))

    def get_window_rect(self):
        try:
            f = ctypes.windll.dwmapi.DwmGetWindowAttribute
        except WindowsError:
            f = None
        if f:
            rect = ctypes.wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            f(ctypes.wintypes.HWND(self.hwnd),
              ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
              ctypes.byref(rect),
              ctypes.sizeof(rect)
              )
            return rect.left, rect.top, rect.right, rect.bottom
    def get_pic_center(self,picfile,confidence=0.6,prees=True):
        """
        根据基准图片获取操作对象位置
        :param picfile: 基准图片
        :param canel: 误差值
        :return: 对像坐标
        """
        picdir=picfile.split(".")[0].strip("123456789")+"pic"
        picpath=os.path.join(self.currtpath,"pic",picdir,picfile)
        if prees:
            pyautogui.press("F9")
            pyautogui.hotkey("alt","h")
        time.sleep(1)
        grids=pyautogui.locateCenterOnScreen(picpath,confidence=confidence,region=self.parent_size,grayscale=True)
        #gridsx=random.choice(range(grids.x-canel,grids.x+canel))
        #gridsy = random.choice(range(grids.y - canel, grids.y + canel))
        return grids
    def dhclick(self,grids,scenal=False):
        gridx = grids.x-7
        gridy = grids.y-7
        if scenal:
            gridx=self.grt_num_center(gridx,self.dows_center[0])
            gridy = self.grt_num_center(gridy, self.dows_center[1])
        #pyautogui.moveTo(gridx,gridy-3)
        print(gridx,gridy-3)
        self.mous.move(int(gridx),int(gridy-8))
        time.sleep(1)
        pyautogui.click()
        #self.mous.click(int(gridx),int(gridy-3),1)
        time.sleep(2)
    def getpic_click(self,picfile,checkfile=None,check_tag=True,prees_tag=True,confidence=0.6,trys=10):
        if checkfile:
            try_num=0
            while try_num <= trys:
                try:
                    grids=self.get_pic_center(picfile,confidence=confidence,prees=prees_tag)
                    self.dhclick(grids)
                except Exception as e:
                    print(e)
                if (self.get_pic_center(checkfile,prees=prees_tag) and check_tag) or (not self.get_pic_center(checkfile,prees=prees_tag) and not check_tag):
                    break
                else:
                    try_num+=1
                    if grids:
                        self.dhclick(grids,scenal=True)
                        time.sleep(2)
                    else:
                        pyautogui.moveTo(self.dows_center)

        else:
            grids = self.get_pic_center(picfile)
            self.dhclick(grids)

