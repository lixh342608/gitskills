#coding=utf-8

import win32gui
import pyautogui
import random
import os,time
from pathlib import Path
from pymouse import PyMouse
from PIL import Image, ImageGrab
from aip import AipOcr
from skimage import io
import easyocr
from cnstd import CnStd
from cnocr import CnOcr
Image.MAX_IMAGE_PIXELS = None
pyautogui.PAUSE=1
os.environ['TESSDATA_PREFIX'] = 'C:/Program Files (x86)/Tesseract-OCR/tessdata'
os.environ["CUDA_VISIBLE_DEVICES"] = "True"
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
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
        self.tmpfilename = os.path.join(self.currtpath, "temp/tmp.png")
        # 调用百度的识别文字
        APP_ID = '25963522'
        API_KEY = 'RIOFdoDKGXfhHr2uLYVmUG8w'
        SECRET_KEY = 'vnWA7s1WfWsrPwEvkgkiVI7MMxNTjFvw'
        self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    def grt_num_center(self,num1,num2):
        center_num=abs(num1-num2)//2
        if num1 > num2:
            return num2+center_num
        else:
            return num1+center_num

    def get_parent_size(self):
        print(self.hwnd)
        win32gui.SetForegroundWindow(self.hwnd)
        time.sleep(2)
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        #left, top, right, bottom = self.get_window_rect()
        self.windowleft=left
        self.windowtop = top
        self.windowright = right-470
        self.windowbottom = bottom-80
        self.parent_size = (left, top, self.windowright, self.windowbottom)
        self.dows_center=(self.grt_num_center(left,right),self.grt_num_center(top,bottom))
    def clear_scene(self):
        self.mous.move(self.dows_center[0],self.dows_center[1])
        time.sleep(1)
        pyautogui.click()
        time.sleep(2)
        #self.mous.click(self.dows_center[0],self.dows_center[1],1,1)
        pyautogui.press("F9")
        pyautogui.hotkey("alt", "h")
        time.sleep(1)
    def get_pic_center(self,picfile,confidence=0.6):
        """
        根据基准图片获取操作对象位置
        :param picfile: 基准图片
        :param canel: 误差值
        :return: 对像坐标
        """
        picdir=picfile.split(".")[0].strip("123456789")+"pic"
        picpath=os.path.join(self.currtpath,"pic",picdir,picfile)
        grids=pyautogui.locateCenterOnScreen(picpath,confidence=confidence,region=self.parent_size,grayscale=True)
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
        #self.mous.click(int(gridx),int(gridy-8),1,1)
        time.sleep(2)
    def getpic_click(self,picfile,checkfile=None,check_tag=True,confidence=0.6,trys=10):
        if checkfile:
            try_num=0
            while try_num <= trys:
                try:
                    self.clear_scene()
                    grids=self.get_pic_center(picfile,confidence=confidence)
                    self.dhclick(grids)
                except Exception as e:
                    print(e)
                if (self.get_pic_center(checkfile) and check_tag) or (not self.get_pic_center(checkfile) and not check_tag):
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
    def calsimilar(self,imagef1,imagef2):
        """
        图片相似度对比
        :param imagef1:
        :param imagef2:
        :return:
        """
        image1=Image.open(imagef1)
        image2 = Image.open(imagef2)
        image1 = image1.convert("L")
        image2 = image2.resize((image1.width,image1.height),Image.ANTIALIAS).convert("L")
        gray1=list(image1.getdata())
        gray2 = list(image2.getdata())
        if gray1 == gray2:
            return 100
        same=0
        for sm in range(len(gray1)):
            if gray1[sm] == gray2[sm]:
                same+=1
        return same*100/len(gray1)
    # 百度OCR接口
    def get_pic_text(self,picfile):
        with open(picfile, 'rb') as fp:
            bimg = fp.read()
            msg = self.client.basicGeneral(bimg)
            return msg
    # 获取当前声景
    def get_scene(self):
        pyautogui.screenshot(imageFilename=self.tmpfilename,region=self.parent_size)
        img=io.imread(self.tmpfilename,as_gray=False)
        print(img.shape)
        rows,cols,_= img.shape
        new = img[rows // 15:rows // 7, 0:cols // 6]
        io.imsave(self.tmpfilename,new)
        #io.show()
        self.get_pic_text(self.tmpfilename)
    # 通过百度接品获取定位
    def get_pointpic_bybaidu(self):
        px,py=self.mous.position()
        print(px,py)
        bbox=(px-70,py-80,px+100,py+50)
        im=ImageGrab.grab(bbox)
        im.save(self.tmpfilename)
        msg=self.get_pic_text(self.tmpfilename)
        text_list=msg.get("words_result")
        for text in text_list:
            texts=text.get("words")
            point=texts.split(",")
            if len(point) == 2:
                break
        else:
            point=self.get_pointpic_bybaidu()
        return point
    def get_pointpic_byeasyocr(self):
        px,py=self.mous.position()
        print(px,py)
        bbox=(px-70,py-80,px+100,py+50)
        im=ImageGrab.grab(bbox)
        im.save(self.tmpfilename)
        time.sleep(1)
        std = CnStd()
        cn_ocr = CnOcr()
        box_info_dic = std.detect(self.tmpfilename)
        box_info_list=box_info_dic.get('detected_texts')
        for box_info in box_info_list:
            print(box_info)
            cropped_img = box_info['cropped_img']  # 检测出的文本框
            ocr_res = cn_ocr.ocr_for_single_line(cropped_img)
            print(ocr_res)

        return ocr_res
    def positioning(self,scene_name,x,y):
        if scene_name == "jianye":
            picname="jianye1.png"
        else:
            return None
        pyautogui.press("tab")
        time.sleep(2)
        grids=self.get_pic_center(picname,confidence=0.6)
        print(grids)
        if grids == None:
            pyautogui.press("tab")
            time.sleep(2)
            grids = self.get_pic_center(picname,confidence=0.6)
        while self.get_pic_center("checkdt1.png",confidence=0.9):
            pyautogui.moveTo(self.dows_center)
            #self.mous.move(self.dows_center)
            quanbu_grid = self.get_pic_center("quanbu1.png", confidence=0.8)
            if quanbu_grid:
                print(1111111111111111)
                quanbu_grid=(quanbu_grid.x+18,quanbu_grid.y-9,)
                pyautogui.moveTo(quanbu_grid,duration=2)
                #self.mous.move(int(quanbu_grid.x) + 10, int(quanbu_grid.y - 10))
                time.sleep(1)
                pyautogui.click()
        self.mous.move(int(grids.x),int(grids.y))
        time.sleep(1)
        while True:
            px,py=self.get_pointpic_byeasyocr()
            print(px,py)
            break

