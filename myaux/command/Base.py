#coding=utf-8

import win32gui
import pyautogui
import random
import os,time
import aircv
from pathlib import Path
from pymouse import PyMouse
from PIL import Image, ImageGrab
from aip import AipOcr
from skimage import io

Image.MAX_IMAGE_PIXELS = None
pyautogui.PAUSE=1
os.environ['TESSDATA_PREFIX'] = 'C:/Program Files (x86)/Tesseract-OCR/tessdata'
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
        self.ditu_size={"jianye":(287,142),"donghaiwan":(117,117)}
        # 调用百度的识别文字
        APP_ID = '25963522'
        API_KEY = 'RIOFdoDKGXfhHr2uLYVmUG8w'
        SECRET_KEY = 'vnWA7s1WfWsrPwEvkgkiVI7MMxNTjFvw'
        self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    def get_num_center(self,num1,num2):
        center_num=abs(num1-num2)//2
        if num1 > num2:
            return num2+center_num
        else:
            return num1+center_num
    def get_filename(self,ptn):
        """
        返回一个临时文件
        :param ptn:
        :return:
        """
        times=time.time()
        timearray=time.localtime(times)
        times=time.strftime("%Y%m%d%H%M%S", timearray)
        return os.path.join(self.currtpath,"temp",ptn+times+".png")
    def get_snapshot(self):
        """
        截取当前屏幕快照，返回临时文件名
        :param ptn:
        :return:
        """
        filename=self.get_filename("snapshot")
        im = ImageGrab.grab()
        im.save(filename)
        return filename
    def get_parent_size(self):
        print(self.hwnd)
        win32gui.SetForegroundWindow(self.hwnd)
        time.sleep(2)
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        #left, top, right, bottom = self.get_window_rect()
        self.windowleft=left
        self.windowtop = top
        self.windowright = right
        self.windowbottom = bottom
        self.parent_size = (left, top, self.windowright, self.windowbottom)
        self.dows_center=(self.get_num_center(left,self.windowright),self.get_num_center(top,self.windowbottom))
    def clear_scene(self):
        self.mous.move(self.dows_center[0],self.dows_center[1])
        time.sleep(1)
        pyautogui.click()
        time.sleep(2)
        #self.mous.click(self.dows_center[0],self.dows_center[1],1,1)
        pyautogui.press("F9")
        pyautogui.hotkey("alt", "h")
        time.sleep(1)
    def get_pic_centerforaytogui(self,picfile,confidence=0.6):
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
        gridx = grids[0]
        gridy = grids[1]
        if scenal:
            gridx=self.get_num_center(gridx,self.dows_center[0])
            gridy = self.get_num_center(gridy, self.dows_center[1])
        #pyautogui.moveTo(gridx,gridy-3)
        print(gridx,gridy-3)
        self.mous.move(int(gridx)-8,int(gridy-8))
        time.sleep(1)
        pyautogui.click()
        #self.mous.click(int(gridx),int(gridy-8),1,1)
        time.sleep(2)
    def getpic_click(self,picfile,checkfile=None,check_tag=True,confidence=0.5,trys=10):
        if checkfile:
            try_num=0
            while try_num <= trys:
                try:
                    self.clear_scene()
                    grids=self.get_pic_centerforaytogui(picfile,confidence=confidence)
                    self.dhclick(grids)
                except Exception as e:
                    print("失败了")
                    print(e)
                if (self.get_pic_centerforaytogui(checkfile) and check_tag) or (not self.get_pic_centerforaytogui(checkfile) and not check_tag):
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

    def get_pic_foraircv(self, picfile, confidence=0.6):
        picdir=picfile.split(".")[0].strip("123456789")+"pic"
        picpath=os.path.join(self.currtpath,"pic",picdir,picfile)
        snapshot_pic=self.get_snapshot()
        bmp = aircv.imread(snapshot_pic)
        tim = aircv.imread(picpath)
        result=aircv.find_template(bmp, tim,threshold=confidence)
        if result:
            print(result.get("confidence"))
            rec=result.get('rectangle')
            return self.suoxiaosource(rec[0])+self.suoxiaosource(rec[-1],lv=0.015,is_add=False)
        else:
            return None
    def get_pixel_rate(self,sec,bbox):
        max_grid=self.ditu_size.get(sec)
        x1,y1,x2,y2=bbox
        xt=(x2-x1)/max_grid[0]
        yt=(y2-y1)/max_grid[1]
        return (xt,yt)
    def get_pic_center(self,picfile,confidence=0.6):
        bbox=self.get_pic_foraircv(picfile,confidence=0.6)
        if bbox:
            return (self.get_num_center(bbox[0],bbox[2]),self.get_num_center(bbox[1],bbox[3]))
    def suoxiaosource(self,bbox,lv=0.005,is_add=True):
        if is_add:
            lv=lv+1
        else:
            lv=1-lv
        return (bbox[0]*lv,bbox[1]*lv)

    def positioning(self,scene_name,x,y):
        picname=scene_name+".PNG"
        pyautogui.press("tab")
        time.sleep(2)
        bbox=self.get_pic_foraircv(picname)
        xt,yt=self.get_pixel_rate(scene_name,bbox)
        minix=bbox[0]
        maxy=bbox[-1]
        grids=(minix+int(x*xt),maxy-int(y*yt))
        print(bbox)
        print(grids)
        pyautogui.moveTo(grids)
        time.sleep(2)
        print(pyautogui.position())
        #while not self.get_pic_centerforaircv("checkdt2.png",confidence=0.5):

        pyautogui.click()
    def shiyongwupin(self,wupinpic):
        while not self.get_pic_centerforaytogui(wupinpic,confidence=0.8):
            pyautogui.hotkey("alt","e")
        grids=self.get_pic_centerforaytogui(wupinpic,confidence=0.8)
        pyautogui.moveTo(grids)
        pyautogui.click(button="right")
    def yidongfx(self,fx=True,fy=True):
        dx=self.dows_center[0]
        dy=self.dows_center[1]
        print(self.dows_center)
        px = dx+100 if fx else dx-100
        py = dy+120 if fy else dy-120
        print(px,py)
        pyautogui.moveTo(px,py)
        pyautogui.click()
        time.sleep(2)
    def is_zhantouz(self):
        if self.get_pic_centerforaytogui("zhandou1.PNG",confidence=0.8):
            return True
        return False
    def zhandoucz(self):
        while self.is_zhantouz():
            pyautogui.hotkey("alt", "q")
            pyautogui.hotkey("alt", "q")
            pyautogui.hotkey("alt", "a")
            pyautogui.hotkey("alt", "a")
            time.sleep(10)
    def huangdang(self,scene_name):
        px=random.choice(range(10,100))
        py=random.choice(range(10,100))
        self.positioning(scene_name,px,py)
        for i in range(5):
            if self.is_zhantouz():
                self.zhandoucz()
            else:
                time.sleep(5)









