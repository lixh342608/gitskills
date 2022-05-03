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
            "aolaiguo_huaguoshan": {
                "source_add": "傲来国",
                "target_add": "花果山",
                "pic_name": "aolaiguo",
                "check_name": "aolaiguo1",
                "yidongproint": [208, 137],
                "yidongfx": [300, -200]
            },
            "huaguoshan_beijuluzhou": {
                "source_add": "花果山",
                "target_add": "北俱芦洲",
                "pic_name": "huaguoshan",
                "check_name": "huaguoshantudi0",
                "yidongproint": [26, 103],
                "is_yizhan": True,
                "is_check": True
            },
            "beijuluzhou_changshoujiaowai": {
                "source_add": "北俱芦洲",
                "target_add": "长寿郊外",
                "pic_name": "beijuluzhou",
                "check_name": "beijuluzhoudidungui0",
                "yidongproint": [196, 10],
                "is_yizhan": True,
                "is_check": True
            },
            "beijuluzhou_huaguoshan": {
                "source_add": "北俱芦洲",
                "target_add": "花果山",
                "pic_name": "beijuluzhou",
                "check_name": "beijuluzhoutudi0",
                "yidongproint": [190, 105],
                "is_yizhan": True,
                "is_check": True
            },
            "beijuluzhou_changancheng": {
                "source_add": "北俱芦洲",
                "target_add": "长安城",
                "pic_name": "beijuluzhou",
                "check_name": "beijuluzhouyizhan0",
                "yidongproint": [45, 119],
                "is_yizhan": True,
                "is_check": True
            },
            "changshoujiaowai_beijuluzhou": {
                "source_add": "长寿郊外",
                "target_add": "北俱芦洲",
                "pic_name": "changshoujiaowai",
                "check_name": "changshoujiaowaiyizhan0",
                "yidongproint": [60, 66],
                "is_yizhan": True
            },
            "changshoujiaowai_changshoucun": {
                "source_add": "长寿郊外",
                "target_add": "长寿村",
                "pic_name": "changshoujiaowai",
                "check_name": "changshoujiaowai1",
                "yidongproint": [150, 160],
                "yidongfx": [50, -200]
            },

        }
    def changjingforyizhan(self,target_add,grid,checkyz):
        print("进入驿站操作*******")
        checkyz=checkyz.strip("0123456789")
        while self.diff_ratio(target_add,self.get_scene()[0]) < 0.6:
            #self.xiaozhun_weizhi(grid)
            print("还没到目的地，继续努力")
            while not self.get_pic_centerforaytogui("yizhan61", confidence=0.8):
                print("没有找到驿站对话图片，开始点击传送人")
                self.clear_scene()
                for k in range(8):
                    pic_name="%s%s" % (checkyz,k)
                    print(pic_name)
                    pic_path=self.get_pic_fullpath(pic_name)
                    if not os.path.exists(pic_path):
                        self.xiaozhun_weizhi(grid)
                        break
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
        while self.diff_ratio(target_add,self.get_scene()[0]) < 0.6:
            self.getpic_click(check_name)
    def changjingforfx(self,target_add,proint):
        px, py = proint
        while self.diff_ratio(target_add,self.get_scene()[0]) < 0.9:
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
        is_check = kuacheng_dic.get("is_check")
        if self.diff_ratio(source_add,self.get_scene()[0]) < 0.6:
            print("当前场景不是%s" % source_add)
            return
        tag=self.get_scene()[-1]
        while True:
            new_tag=self.get_scene()[-1]
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
            if is_check:
                checkyz=check_name
            else:
                checkyz="%syizhan" % pic_name
            self.changjingforyizhan(target_add,yidongproint,checkyz)
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