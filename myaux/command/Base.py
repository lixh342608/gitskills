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
from paddleocr import PaddleOCR

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
        self.ditu_size={"jianye":(287,142),"donghaiwan":(117,117)}
        self.yunbiao_par=["牛魔王","观音姐姐","镇元大仙","孙婆婆","地藏王"]
        self.padocr = PaddleOCR(use_angle_cls=True, lang="ch")
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
        print("zhiqian")
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
        self.mous.move(random.choice(range(self.dows_center[0]-10,self.dows_center[0]+10)),random.choice(range(self.dows_center[1]-10,self.dows_center[1]+10)))
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
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
        picpath=self.get_pic_fullpath(picfile)
        grids=pyautogui.locateCenterOnScreen(picpath,confidence=confidence,region=self.parent_size,grayscale=True)
        return grids
    def get_pic_bbox(self,picfile,confidence=0.6):
        """
        根据基准图片获取操作对象位置
        :param picfile: 基准图片
        :param canel: 误差值
        :return: 对像box
        """
        picpath=self.get_pic_fullpath(picfile)
        bbox=pyautogui.locateOnScreen(picpath,confidence=confidence,region=self.parent_size,grayscale=True)
        return bbox
    def get_allpic(self,picfile,confidence=0.6):
        """
        查找所有相似图片，返回bbox
        """
        picpath = self.get_pic_fullpath(picfile)
        btm=pyautogui.locateAllOnScreen(picpath,confidence=confidence)
        return list(btm)

    def dhclick(self,bbox,scenal=False,pfx=None):
        gridx = self.get_num_center(bbox.left,bbox.left+bbox.width)
        gridy = self.get_num_center(bbox.top,bbox.top+bbox.height)
        if scenal:
            if abs(self.dows_center[0] - gridx) < 100:
                gridx = gridx + 100
            else:
                gridx=self.get_num_center(gridx,self.dows_center[0])
            gridy = self.get_num_center(gridy, self.dows_center[1])
        else:
            gridx = random.choice(range(bbox.left,bbox.left+bbox.width))
            gridy = random.choice(range(bbox.top,bbox.top+bbox.height))
        if pfx == "left":
            gridx-=10
        elif pfx == "right":
            gridx+=10
        elif pfx == "top":
            gridy -= 10
        elif pfx == "bom":
            gridy += 10
        else:
            gridx -= 5
        print("scenal:%s %s ===>> (%s,%s)" % (scenal,bbox,gridx,gridy))
        pyautogui.moveTo(gridx,gridy)
        #print(gridx,gridy)
        #self.mous.move(int(gridx),int(gridy))
        time.sleep(1)
        pyautogui.click()
        #self.mous.click(int(gridx),int(gridy-8),1,1)
        time.sleep(1)
    def getpic_click(self,picfile,checkfile=None,confidence=0.5,pfx=None):
        if checkfile:
            while not self.get_pic_centerforaytogui(checkfile):
                self.clear_scene()
                bbox=self.get_pic_bbox(picfile,confidence=confidence)
                if bbox:
                    self.dhclick(bbox,pfx=pfx)
                if not self.get_pic_centerforaytogui(checkfile):
                    self.dhclick(bbox,scenal=True, pfx=pfx)

        else:
            bbox=self.get_pic_bbox(picfile)
            self.dhclick(bbox,pfx=pfx)
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
        result=self.duqu_yemian(picfile)
        return str(result)
        #with open(picfile, 'rb') as fp:
            #bimg = fp.read()
            #msg = self.client.basicGeneral(bimg)
            #return msg
    # 获取当前声景
    def get_scene(self):
        tmpfilename=self.get_filename("scene")
        pyautogui.screenshot(imageFilename=tmpfilename,region=self.parent_size)
        img=io.imread(tmpfilename,as_gray=False)
        print(img.shape)
        rows,cols,_= img.shape
        new = img[rows // 15:rows // 7, 0:cols // 6]
        io.imsave(tmpfilename,new)
        #io.show()
        return self.get_pic_text(tmpfilename)
    # 通过百度接品获取定位
    def get_pointpic_bybaidu(self):
        tmpfilename = self.get_filename("pointpic")
        px,py=self.mous.position()
        print(px,py)
        bbox=(px-70,py-80,px+100,py+50)
        im=ImageGrab.grab(bbox)
        im.save(tmpfilename)
        msg=self.get_pic_text(tmpfilename)
        text_list=msg.get("words_result")
        for text in text_list:
            texts=text.get("words")
            point=texts.split(",")
            if len(point) == 2:
                break
        else:
            point=self.get_pointpic_bybaidu()
        return point
    # aircv方式获取指定图片坐标
    def get_pic_fullpath(self,pocname):
        myfile=Path(pocname)
        if myfile.is_file():
            picpath=pocname
        else:
            picdir=pocname.strip("123456789")+"pic"
            picpath=os.path.join(self.currtpath,"pic",picdir,pocname+".png")
        return picpath
    def get_pic_foraircv(self, picfile, confidence=0.6):
        picpath=self.get_pic_fullpath(picfile)
        snapshot_pic=self.get_snapshot()
        bmp = aircv.imread(snapshot_pic)
        tim = aircv.imread(picpath)
        result=aircv.find_template(bmp, tim,threshold=confidence)
        if result:
            print(result.get("confidence"))
            rec=result.get('rectangle')
            return rec,snapshot_pic
            #return self.suoxiaosource(rec[0])+self.suoxiaosource(rec[-1],lv=0.015,is_add=False)
        else:
            return None
    # 截取屏幕上类似图片
    def shear_pic(self,picfile):
        rec,snapshot_pic=self.get_pic_foraircv(picfile)
        bbox=rec[0]+rec[-1]
        im1=Image.open(snapshot_pic)
        im2=im1.crop(bbox)
        temfile=self.get_filename("renwutmp")
        im2.save(temfile)
        return temfile
    # 场景与PC的缩方比例
    def get_pixel_rate(self,sec,bbox):
        max_grid=self.ditu_size.get(sec)
        x1,y1,x2,y2=bbox
        xt=(x2-x1)/max_grid[0]
        yt=(y2-y1)/max_grid[1]
        return (xt,yt)
    def get_pic_center(self,picfile,confidence=0.6):
        rec,_=self.get_pic_foraircv(picfile,confidence=confidence)
        bbox = self.suoxiaosource(rec[0]) + self.suoxiaosource(rec[-1], lv=0.015, is_add=False)
        if bbox:
            return (self.get_num_center(bbox[0],bbox[2]),self.get_num_center(bbox[1],bbox[3]))
    # 按比例缩小图片坐标
    def suoxiaosource(self,bbox,lv=0.005,is_add=True):
        if is_add:
            lv=lv+1
        else:
            lv=1-lv
        return (bbox[0]*lv,bbox[1]*lv)
    # 去往场景内某一坐标
    def positioning(self,scene_name,x,y):
        pyautogui.press("tab")
        time.sleep(2)
        rec,_=self.get_pic_foraircv(scene_name)
        bbox=self.suoxiaosource(rec[0])+self.suoxiaosource(rec[-1],lv=0.015,is_add=False)
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
    # 使用物品
    def shiyongwupin(self,wupinpic):
        while not self.get_pic_centerforaytogui(wupinpic,confidence=0.8):
            print("没找到")
            pyautogui.hotkey("alt","e")
        grids=self.get_pic_centerforaytogui(wupinpic,confidence=0.8)
        pyautogui.moveTo(grids)
        pyautogui.click(button="right")
    def yidongfx(self,fx=100,fy=100):
        """
        方向移动
        """
        dx=self.dows_center[0]
        dy=self.dows_center[1]
        print(self.dows_center)
        px = dx+fx
        py = dy+fy
        print(px,py)
        pyautogui.moveTo(px,py)
        pyautogui.click()
        time.sleep(2)
    def is_zhantouz(self):
        """判断是否战斗状态"""
        if self.get_pic_centerforaytogui("zhandou1",confidence=0.8):
            return True
        return False
    def zhandoucz(self):
        """
        战斗时的操作
        """
        while self.is_zhantouz():
            pyautogui.hotkey("alt", "q")
            pyautogui.hotkey("alt", "q")
            pyautogui.hotkey("alt", "a")
            pyautogui.hotkey("alt", "a")
            time.sleep(10)
    def huangdang(self,scene_name):
        """
        场景内转悠
        """
        px=random.choice(range(10,100))
        py=random.choice(range(10,100))
        self.positioning(scene_name,px,py)
        for i in range(5):
            if self.is_zhantouz():
                self.zhandoucz()
            else:
                time.sleep(5)
    def duqu_yemian(self,picfile):
        print(picfile)
        temp_file=self.shear_pic(picfile)
        print(temp_file)
        # Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
        # 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
        result = self.padocr.ocr(temp_file, cls=True)
        result = [line[-1][0] for line in result]
        return result
    # 打开任务栏
    def open_renwulan(self):
        while not self.get_pic_centerforaytogui("renwu1") and not self.is_zhantouz():
            pyautogui.hotkey("alt", "q")












