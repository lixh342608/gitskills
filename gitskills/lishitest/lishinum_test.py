#coding=utf-8
'''
Created on 2017年6月18日

@author: Administrator
'''
from tkinter import *


import tkinter.messagebox

root=Tk()
width_n=root.winfo_screenwidth()/2-200
height_n=root.winfo_screenheight()/2-150
root.geometry('350x300+%d+%d' % (int(width_n),int(height_n)))

lab1=Label(root,text="请输入雅堂帐户用户名:").pack()
username_var=StringVar()
Entry(root,textvariable=username_var).pack()
username_var.set("")

lab2=Label(root,text="请输入雅堂帐户密码:").pack()
pwd_var=StringVar()
Entry(root,textvariable=pwd_var,show='*').pack()
pwd_var.set("")
lab3=Label(root,text="请输入雅堂帐户交易密码:").pack()
paypwd_var=StringVar()
Entry(root,textvariable=paypwd_var).pack()
paypwd_var.set("")

lab4=Label(root,text="请输入投资金额（置 空将默认为最大金额）:").pack()
pranum_var=StringVar()
Entry(root,textvariable=pranum_var).pack()
pranum_var.set("")
def click_on():
    username=username_var.get()
    pwd=pwd_var.get()
    paypwd=paypwd_var.get()
    pranum=pranum_var.get()
    if username and pwd and paypwd:
        
        lishi=lishitest()
        lishi.timeset(username,pwd)
        if pranum:
            lishi.giter(paypwd,pranum)
        else:
            lishi.giter(paypwd)
        
    else:
        tkinter.messagebox.askokcancel("提示","除投资金额外所有项不可为空，如果有误将导致无法登录或抢秒时交易密码错误。")
        
    
b1=Button(root,text="开始抢秒",command=click_on,bg="red",width=15,fg="blue").pack()
root.mainloop()



   
    