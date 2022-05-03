#coding=utf-8

import win32gui
import pyautogui
import random
import os,time,re
import aircv
from pathlib import Path
from pymouse import PyMouse
from PIL import Image, ImageGrab
from aip import AipOcr
from skimage import io
from paddleocr import PaddleOCR
import difflib

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
        self.ditu_size={"jianye":(287,142),"donghaiwan":(119,119),"changancheng":(548,277),"jiangnanyewai":(159,119),"aolaiguo":(222,150),"huaguoshan":(159,119),"beijuluzhou":(226,169),"changshoujiaowai":(191,167)}
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
    def get_pic_centerforaytogui(self,picfile,confidence=0.7,is_npc=False):
        """
        根据基准图片获取操作对象位置
        :param picfile: 基准图片
        :param canel: 误差值
        :return: 对像坐标
        """
        if is_npc:
            self.clear_scene()
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
        print(picfile,picpath)
        bbox=pyautogui.locateOnScreen(picpath,confidence=confidence,region=self.parent_size,grayscale=True)
        return bbox
    def get_allpic(self,picfile,confidence=0.6,index=None):
        """
        查找所有相似图片，返回bbox
        """
        picpath = self.get_pic_fullpath(picfile)
        btm=pyautogui.locateAllOnScreen(picpath,confidence=confidence,region=self.parent_size,grayscale=True)
        if index != None:
            return list(btm)[index]
        return list(btm)
    def get_interval(self,basic,length):
        pt=length/3
        end=basic+pt*2
        start=basic
        return range(int(start),int(end))

    def dhclick(self,grids,scenal=False):
        gridx = grids.x
        gridy = grids.y
        if scenal:
            if abs(self.dows_center[0] - gridx) < 100:
                gridx = gridx + 100
            else:
                gridx=self.get_num_center(gridx,self.dows_center[0])
            gridy = self.get_num_center(gridy, self.dows_center[1])
        pyautogui.moveTo(gridx-5,gridy-5)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
    def getpic_click(self,picfile,checkfile=None,confidence=0.7,is_npc=False,check_tag=True):
        if checkfile:
            if check_tag:
                while not self.get_pic_centerforaytogui(checkfile):
                    grids=self.get_pic_centerforaytogui(picfile,confidence=confidence,is_npc=is_npc)
                    if grids:
                        self.dhclick(grids)
                        if not self.get_pic_centerforaytogui(checkfile):
                            self.dhclick(grids,scenal=True)
            else:
                while self.get_pic_centerforaytogui(checkfile):
                    pyautogui.moveTo(self.dows_center)
                    grids = self.get_pic_centerforaytogui(picfile, confidence=confidence,is_npc=is_npc)
                    if grids:
                        self.dhclick(grids)
        else:
            grids=self.get_pic_centerforaytogui(picfile,confidence=confidence,is_npc=is_npc)
            if grids:
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
    def diff_ratio(self,diff1,diff2):
        if not isinstance(diff1,str) or not isinstance(diff2,str):
            print("非字符串数据不能比较相似度")
            return 0
        res = difflib.SequenceMatcher(None,diff1,diff2)
        return res.quick_ratio()
    # 百度OCR接口
    def get_pic_text(self,picfile):
        result=self.duqu_yemian(picfile)
        return result
    # 获取当前声景
    def get_scene(self):
        tmpfilename=self.get_filename("scene")
        left,top=self.parent_size[:2]
        scene_size=(left,top+80,left+130,top+130)
        img=ImageGrab.grab(scene_size)
        img.save(tmpfilename)
        time.sleep(1)
        result = self.padocr.ocr(tmpfilename, cls=True)
        print(result)
        scene_text = [line[-1][0] for line in result]
        texts=scene_text[-1]
        scene="".join(re.findall(r'[\u4e00-\u9fa5]',texts))
        zuobiao=re.findall(r"\d+",texts.split(scene)[-1][1:-1])
        if len(zuobiao)==1:
            zuobiao=[zuobiao[0][:-1],zuobiao[0][-1]]
        print("当前场景信息：%s %s" % (scene,zuobiao))
        return [scene,zuobiao]
    def xiaozhun_weizhi(self,grid):
        while True:
            print("位置校准：%s" % grid)
            _,zb=self.get_scene()
            if len(zb)!=2:
                continue
            if (int(grid[0]) - int(zb[0])) > 10:
                px = 100
            elif (int(grid[0]) - int(zb[0])) < -10:
                px = -100
            else:
                px=0
            if (int(grid[1]) - int(zb[1])) > 10:
                py = -100
            elif (int(grid[1]) - int(zb[1])) < -10:
                py = 100
            else:
                py=0
            if px==py==0:
                break
            print("校准值：%s %s" % (px,py))
            self.yidongfx(px,py)
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
            picdir=pocname.strip("0123456789")+"pic"
            picpath=os.path.join(self.currtpath,"pic",picdir,pocname+".png")
        return picpath
    def get_pic_foraircv(self, picfile, confidence=0.6):
        picpath=self.get_pic_fullpath(picfile)
        print(picpath)
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
        return self.bbox_pic(bbox,snapshot_pic)
    def bbox_pic(self,bbox,source_image=None):
        if source_image == None:
            source_image=self.get_snapshot()
        #im_box=(bbox.left,bbox.top,bbox.left+bbox.width,bbox.top+bbox.height)
        im1=Image.open(source_image)
        im2=im1.crop(bbox)
        temfile = self.get_filename("renwutmp")
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
        bbox=self.suoxiaosource(rec[0])+self.suoxiaosource(rec[-1],lv=0.01,is_add=False)
        xt,yt=self.get_pixel_rate(scene_name,bbox)
        minix=bbox[0]
        maxy=bbox[-1]
        grids=(minix+int(x*xt),maxy-int(y*yt))
        pyautogui.moveTo(grids)
        time.sleep(1)
        print(pyautogui.position())
        pyautogui.click()
        time.sleep(1)
        pyautogui.press("tab")

    def positioningforzb(self, scene_name, x, y):
        pyautogui.press("tab")
        time.sleep(2)
        rec, _ = self.get_pic_foraircv(scene_name)
        bbox = self.suoxiaosource(rec[0]) + self.suoxiaosource(rec[-1], lv=0.01, is_add=False)
        xt, yt = self.get_pixel_rate(scene_name, bbox)
        minix = bbox[0]
        maxy = bbox[-1]
        grids = (minix + int(x * xt), maxy - int(y * yt))
        pyautogui.moveTo(grids)
        time.sleep(1)
        print(pyautogui.position())
        pyautogui.click()
        time.sleep(1)
        pyautogui.press("tab")
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












