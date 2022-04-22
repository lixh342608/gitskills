#coding=utf-8

from .Base import *
import pyautogui
import os
pyautogui.PAUSE=1

class yabiao(myBase):
    def __init__(self,hwndkey):
        super(yabiao, self).__init__(hwndkey)
    def is_yabiao(self):
        biaodi = None
        self.open_renwulan()
        text_list=self.duqu_yemian("renwu1")
        for text in reversed(text_list):
            if "运镖给" in text:
                for npc in self.yunbiao_par:
                    if npc in text:
                        biaodi=npc
                        break
                break
        return biaodi
    def qubiao(self):
        #self.shiyongwupin("biaoqi1")
        #grids=self.get_pic_centerforaytogui("biaoqi2",confidence=0.8)
        #pyautogui.moveTo(grids)
        #pyautogui.click()
        while "长风镖局" not in self.get_scene():
            self.yidongfx(100,-50)
        #print(os.path.exists('J:\gitskills\myaux\command\pic\zhongapic\zhonga1.png'))
        #while self.get_pic_centerforaytogui("zhonga1",confidence=0.7):
        #    self.getpic_click("zhonga1",confidence=0.7)
        self.getpic_click("biaoqi3",checkfile="biaoqi4",confidence=0.7)
        while not self.get_pic_centerforaytogui("biaoqi6"):
            print(666)
            btm = self.get_allpic('biaoqi5',confidence=0.8)
            self.dhclick(btm[-1])
            bbox=btm[-2]
            im_box=(bbox.left,bbox.top,bbox.left+bbox.width,bbox.top+bbox.height)
            print(self.bbox_pic(im_box))
        self.getpic_click("biaoqi7",confidence=0.8,pfx="bom")
        #self.getpic_click("biaoqi5", checkfile="biaoqi6", confidence=0.8)


