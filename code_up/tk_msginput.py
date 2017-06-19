#coding=utf-8
'''
Created on 2015年12月25日

@author: admin
'''

from Tkinter import *
import tkMessageBox
from xltest import xl_red
import pickle
from updata_gui import *
#读取配置文件
def loadcol():
    try:
        with open("collocation.pic","r") as f:
            col=pickle.load(f)   
            return col     
    except IOError:
        return 0
#生成配置文件 
def writcol(col):
    with open("collocation.pic","w") as f:
        pickle.dump(col, f)
class tk_Msginput:
    #初始化TKINTER对像形状
    def __init__(self):
        self.root=Tk()
    
        self.root.title("预设参数")
    
        
        width_n=self.root.winfo_screenwidth()/2-200
        height_n=self.root.winfo_screenheight()/2-250
        self.pack=0
        self.textlist=[]
        self.row_list=[]
        self.root.geometry('350x550+%s+%s' % (width_n,height_n))
        self.col=loadcol()
    #如果读取配置文件返回值为0，则弹出提示，并初始化配置信息为“”
    def colback(self):
        if self.col==0:
            tkMessageBox.showinfo("提示：","没有找到可用配置文件，请手动设置相关参数！")
            self.col=dict.fromkeys(("motecom","pwd","localpath","motepath","moteuser","cal"),"")
            
    #初始化控件
    def tk_input(self):
        self.colback()
        #设置文件路径
        lab1=Label(self.root,text="请在下方输入远程主机信息（格式：root@192.168.1.5:22）").grid(row=0,column=0,columnspan=3)
    
        motecom_var=StringVar()
    
        e1=Entry(self.root,textvariable=motecom_var).grid(row=1,column=1)
    
        motecom_var.set(self.col["motecom"])
        
        #设置新数据库地址
        lab2=Label(self.root,text="请在下方输入远程主机密码").grid(row=2,column=0,columnspan=3)
    
        pwd_var=StringVar()
    
        e2=Entry(self.root,textvariable=pwd_var,show="*").grid(row=3,column=1)
    
        pwd_var.set(self.col["pwd"])
        
        #设置新域名
        lab3=Label(self.root,text="请在下方输入源文件地址").grid(row=4,column=0,columnspan=3)
    
        localpath_var=StringVar()
    
        e3=Entry(self.root,textvariable=localpath_var).grid(row=5,column=1)
    
        localpath_var.set(self.col["localpath"])
        
        #设置远程主机IP
        lab4=Label(self.root,text="请在下方输入远程目录地址").grid(row=6,column=0,columnspan=3)
    
        motepath_var=StringVar()
    
        e4=Entry(self.root,textvariable=motepath_var).grid(row=7,column=1)
    
        motepath_var.set(self.col["motepath"])
        
        #设置远程主机端口
        lab5=Label(self.root,text="请选择上传文件列表").grid(row=10,column=0,columnspan=3)
    
        update_var=StringVar()
    
        e5=Entry(self.root,textvariable=update_var).grid(row=11,column=1)
    
        update_var.set("")
        
        #设置远程主机用户名
        lab6=Label(self.root,text="请在下方输入程序执行角色（格式：user:group）").grid(row=8,column=0,columnspan=3)
    
        moteuser_var=StringVar()
    
        e6=Entry(self.root,textvariable=moteuser_var).grid(row=9,column=1)
    
        moteuser_var.set(self.col["moteuser"])
        cal_var=StringVar()
        e7=Entry(self.root,textvariable=cal_var).grid(row=14,column=1)
        try: 
            if self.col["cal"]:
                cal_var.set(self.col["cal"])
            else:
                cal_var.set(2)    
        except:
            cal_var.set(2)
        Label(self.root,text="主机信息").grid(row=1,column=0)
        Label(self.root,text="连接密码").grid(row=3,column=0)
        Label(self.root,text="源文件地址").grid(row=5,column=0)
        remote=Label(self.root,text="远程地址").grid(row=7,column=0)
        Label(self.root,text="更新序号").grid(row=11,column=0)
        Label(self.root,text="用户身份").grid(row=9,column=0)
        Label(self.root,text="请确认更新信息后点击右上角红色按钮进行更新操作").grid(row=12,column=0,columnspan=3)
        #text=Text(self.root,width=45,height=15,font = ("Arial, 10"))
        #text.grid(row=13,column=0,columnspan=3)
        Label(self.root,text="校准值").grid(row=14,column=0)
        #定义按钮动作（继续动作）
        def click_on():
            
            self.col["motecom"]=motecom_var.get()
            self.col["pwd"]=pwd_var.get()
            self.col["localpath"]=localpath_var.get()
            self.col["motepath"]=motepath_var.get()
            #self.col["update_num"]=update_var.get()
            self.col["moteuser"]=moteuser_var.get()
            self.col["cal"]=cal_var.get()
            for item in self.col.values():
                if item:
                    pass
                else:
                    tkMessageBox.showinfo("提示：","以上所有项不可为空！")
                    break
            else:
                writcol(self.col)
                self.pack=1
                self.root.destroy()
        #定义按钮动作（获取版本号信息）
        def select_on():
            self.row_list=update_var.get().split(",")
            #print row_list
            cal=cal_var.get()
            text=""
            try:
                for row_num in self.row_list:
                    #print row_num
                    if row_num:
                        cell=xl_red(int(row_num),int(cal))
                        item=["更新代号： ","  更新功能：  ","文件列表：  ","  SVN版本号：  ","  开发人员：  "]
                        num=0
                        for stri in item:
                            text+=(stri+"*"+str(cell[num])+"*")
                            num+=1
                            if num==2:
                                filelist=cell[num].split("\n")
                                for file in filelist:
                                    if file:
                                        self.textlist.append(file)
                                           
        
                        if int(row_num)==cell[0]:
                            text+=("更新码核对正确，请点击右上角按钮进行更新!\n"+"*"*30+"我是分割线"+"*"*30+"\n")
                            
                        else:
                            text+=("更新码核对不正确，请重新调整更新码校准值！\n")
                #print textlist
                tkMessageBox.showinfo("请核对以下信息：",text)        
                    
            except:
                tkMessageBox.showinfo("提示：","请正确输入更新码")
                
        b1=Button(self.root,text="参数设置完成再点我",command=click_on,bg="red",width=15,fg="blue").grid(row=1,column=2)
        b2=Button(self.root,text="查看更新信息",command=select_on).grid(row=11,column=2)
        self.root.mainloop()
        return self.pack,self.textlist,self.row_list
if __name__=="__main__":
    #定义更新主函数
    def main():
        act=tk_Msginput()
        pack,textlist,row_list=act.tk_input()
        if pack==0:
            pass
        else:
            col=loadcol()
            #print col
            put=updata_list(col,textlist,row_list)
            pack=put.update_File()
            if pack==1:
                main()
    try:
        main()
    except Exception as e:
        tkMessageBox.showinfo("错误提示：",e)