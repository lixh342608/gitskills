#coding=utf-8

import random,os
import tkinter.messagebox
from tkinter import *
def ask_pk():
    pk=random.choice(range(1,14))

    for i in range(3):
        try:
            #ask = hb_var.get()
            ask=int(input("请输入："))
        except Exception as e:
            print("你操作有误，退出游戏.")
            os._exit(3)
        if ask > pk:
            print("太大了")
        elif ask < pk:
            print("太小了")
        else:
            print("you win %s %s" % (pk,ask))
            break
    else:
        print("geme over must %s but you give %s." % (pk,ask))

if __name__ == "__main__":
    ask_pk()