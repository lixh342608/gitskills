#coding=utf-8

from .Base import *
import pyautogui
import os,time
pyautogui.PAUSE=1

class scene_yd(myBase):
    def __init__(self,hwndkey):
        super(scene_yd, self).__init__(hwndkey)
        self.luxian_dic={
            "changancheng_jiangnanyewai":{
                "source_add":"长安城",
                "target_add":"江南野外",
                "pic_name":"changancheng",
                "check_name":"changancheng1",
                "yidongproint":[520,20],
                "yidongfx":[300,300]
            },
            "jiangnanyewai_jianyecheng": {
                "source_add": "江南野外",
                "target_add": "建邺城",
                "pic_name": "jiangnanyewai",
                "check_name": "jiangnanyewai1",
                "yidongproint": [137, 55],
                "yidongfx": [300, 70]
            },
            "jianyecheng_donghaiwan": {
                "source_add": "建邺城",
                "target_add": "东海湾",
                "pic_name": "jianye",
                "check_name": "jianye1",
                "yidongproint": [266, 30],
                "dingdian_canzhao": True
            },
            "donghaiwan_aolaiguo": {
                "source_add": "东海湾",
                "target_add": "傲来国",
                "pic_name": "donghaiwan",
                "check_name": "donghaiwan1",
                "yidongproint": [51, 20],
                "is_yizhan": True
            },
        }
    def changjingforyizhan(self,target_add):
        print("进入驿站操作*******")
        while target_add not in self.get_scene():
            print("还没到目的地，继续努力")
            while not self.get_pic_centerforaytogui("yizhan61", confidence=0.8):
                print("没有找到驿站对话图片，开始点击传送人")
                self.clear_scene()
                for k in range(6):
                    pic_name="yizhan%s" % k
                    grids = self.get_pic_centerforaytogui(pic_name,confidence=0.8)
                    if grids:
                        print("%s找到传送人位置" % pic_name)
                        self.dhclick(grids)
                        if not self.get_pic_centerforaytogui("yizhan61", confidence=0.8):
                            self.dhclick(grids,scenal=True)
                        break
                    else:
                        print("没找到%s" % pic_name)
            self.getpic_click("yizhan71",checkfile="yizhan61",confidence=0.9,check_tag=False)

    def changjingfordingdian(self,target_add,check_name):
        while target_add not in self.get_scene():
            self.getpic_click(check_name)
    def changjingforfx(self,target_add,proint):
        px, py = proint
        while target_add not in self.get_scene():
            self.clear_scene()
            self.yidongfx(px, py)
            time.sleep(1)
    def kuachengyundong(self,kuacheng_name):
        kuacheng_dic=self.luxian_dic.get(kuacheng_name)
        if not kuacheng_dic:
            print("没有路线为%s的线跑，请核查.")
            return
        source_add=kuacheng_dic.get("source_add")
        target_add = kuacheng_dic.get("target_add")
        pic_name = kuacheng_dic.get("pic_name")
        check_name = kuacheng_dic.get("check_name")
        yidongproint = kuacheng_dic.get("yidongproint")
        is_yizhan=kuacheng_dic.get("is_yizhan")
        scene=self.get_scene()
        if source_add not in scene:
            print("当前场景不是%s" % source_add)
            return
        tag=scene.split(source_add)[-1]
        while True:
            new_tag=self.get_scene().split(source_add)[-1]
            if new_tag == tag:
                if not self.get_pic_centerforaytogui(check_name,is_npc=True):
                    px,py=yidongproint
                    self.positioning(pic_name, px, py)
                else:
                    break
            else:
                tag=new_tag
                time.sleep(2)
        if is_yizhan:
            self.changjingforyizhan(target_add)
        elif kuacheng_dic.get("dingdian_canzhao") != None:
            self.changjingfordingdian(target_add,check_name)
        else:
            proint=kuacheng_dic.get("yidongfx")
            if proint == None:
                print("请设置一个有效的入场方式.")
                return
            else:
                self.changjingforfx(target_add,proint)
        return True