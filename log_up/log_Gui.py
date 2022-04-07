#coding=utf-8
'''
Created on 2016年11月12日

@author: pc
'''
from Tkinter import *
import tkMessageBox,os
from updateLog import *
from tkFileDialog import askopenfilename


class log_gui:
    #初始化TKINTER对象显示形状
    def __init__(self):
        self.root=Tk()  
        self.root.title("预设参数")
        width_n=self.root.winfo_screenwidth()/2-180
        height_n=self.root.winfo_screenheight()/2-250
        
        self.root.geometry('330x430+%s+%s' % (width_n,height_n))
        self.exl_path=loadcol("excel_path.pic")
        #print self.exl_path      
    #初始化控件
    def add_info(self):
        def back_value(up_var):
            if self.exl_path != "":
                try:
                    cellvalue,rb=read_cell(self.exl_path)
                    up_var.set(int(cellvalue)+1)
                    head_var.set("")
                    self.e2.delete(1.0,END)
                    SVN_V_var.set("")
                    emp_name_var.set("")
                except ValueError:
                    tkMessageBox.showinfo("提示：","文件最后一条数据更新码不是有效数据，请检查目标文件。")
                    up_var.set("")
            else:
                up_var.set("")
        def change_on():
            if b2_text_var.get()==u"去修改（当前为新增模式）":
                b2_text_var.set("去新增（当前为修改模式）")
                b1_text_var.set("保      存")
                b2["bg"]="blue"
                b1["bg"]="blue"
                e5["state"]=NORMAL
                b3["state"]=NORMAL
                b3["bg"]="blue"
                cellvalue,rb=read_cell(self.exl_path)
                set_value(cellvalue)
            else:
                b2_text_var.set("去修改（当前为新增模式）")
                b1_text_var.set("写      入")
                b2["bg"]="red"
                b1["bg"]="red"
                e5["state"]=DISABLED
                b3["state"]=DISABLED
                b3["bg"]="white"
                back_value(up_ver_var)
        def click_on():
            filelist=[]
            filelist.append(up_ver_var.get())
            filelist.append(head_var.get())
            filelist.append(self.e2.get("0.0",END).replace("\n","\r\n"))
            filelist.append(SVN_V_var.get())
            filelist.append(emp_name_var.get())
            #print filelist
            for filename in filelist:
                if filename.strip()=="":
                    tkMessageBox.showinfo("提示：","以上所有项不可为空！")
                    break
            else:
                try:
                #print "开始写入"
                    write_log(filelist)
                    if b1_text_var.get()==u"写      入":
                        tkMessageBox.showinfo("提示：","写入成功！")
                        back_value(up_ver_var)
                    else:
                        tkMessageBox.showinfo("提示：","保存成功！")
                except Exception as e:
                    tkMessageBox.showerror("提示：",e)
                
        def set_value(cellvalue):
            try:
                row_cell=read_row(cellvalue,xlfile=self.exl_path)
                up_ver_var.set(int(row_cell[0]))
            except:
                up_ver_var.set("")
            head_var.set(row_cell[1])
            self.e2.delete(1.0,END)
            self.e2.insert(INSERT,row_cell[2])
            try:
                SVN_V_var.set(int(row_cell[3]))
            except:
                SVN_V_var.set(row_cell[3])
            emp_name_var.set(row_cell[4])
        def select_value():
            cellvalue=up_ver_var.get()
            set_value(cellvalue)
        def select_file():
            e6["state"]=NORMAL
            try:
                path_dir=os.path.split(self.exl_path)[0]
            except:
                path_dir="C:\Users\pc\Desktop"
            self.exl_path =u"%s" % askopenfilename(initialdir = path_dir,filetypes=[("old_excel","*.xls"),("new_excel","*.xlsx")])
            if self.exl_path:
                excel_file_var.set(self.exl_path)
            back_value(up_ver_var)
            writcol(self.exl_path,"excel_path.pic")
            e6["state"]=DISABLED        
        #功能描述
        lab1=Label(self.root,text="请在下方输入功能或BUG描述").grid(row=2,column=0,columnspan=3)
    
        head_var=StringVar()
    
        e1=Entry(self.root,textvariable=head_var,width=35).grid(row=3,column=1,columnspan=2)
    
        head_var.set("")
        
        #文件列表
        lab2=Label(self.root,text="请在下方输入需要更新的文件（一个文件一行）。").grid(row=4,column=0,columnspan=3)
    
        
    
        self.e2=Text(self.root,width=35,height=10,font = ("Arial, 10"))
        self.e2.grid(row=5,column=1,columnspan=2)
    

        
        #SVN版本号
        lab3=Label(self.root,text="请在下方输入SVN版本号").grid(row=6,column=0,columnspan=3)
    
        SVN_V_var=StringVar()
    
        e3=Entry(self.root,textvariable=SVN_V_var,width=35).grid(row=7,column=1,columnspan=2)
    
        SVN_V_var.set("")
        
        #设置开发人
        lab4=Label(self.root,text="请在下方输入开发人员姓名").grid(row=8,column=0,columnspan=3)
    
        emp_name_var=StringVar()
    
        e4=Entry(self.root,textvariable=emp_name_var,width=35).grid(row=9,column=1,columnspan=2)
    
        emp_name_var.set("")
        
        up_ver_var=StringVar()
        e5=Entry(self.root,textvariable=up_ver_var,state=DISABLED)
        e5.grid(row=1,column=1)
        back_value(up_ver_var)
        excel_file_var=StringVar()
        e6=Entry(self.root,textvariable=excel_file_var,state=DISABLED)
        e6.grid(row=11,column=1)
        
        
        if self.exl_path:
            excel_file_var.set(self.exl_path)
        else:
            tkMessageBox.showerror("提示：","找不到配置文件，请先选择需要操作的excel文件。")
            excel_file_var.set("")
        
        Label(self.root,text="更新码").grid(row=1,column=0)
        Label(self.root,text="功能描述").grid(row=3,column=0)
        Label(self.root,text="文件列表").grid(row=5,column=0)
        Label(self.root,text="SVN版本号").grid(row=7,column=0)
        remote=Label(self.root,text="开发者").grid(row=9,column=0)
        b1_text_var=StringVar()
        b1=Button(self.root,textvariable=b1_text_var,command=click_on,bg="red",width=10,fg="white")
        b1_text_var.set("写      入")
        b1.grid(row=12,column=1)
        b2_text_var=StringVar()
        b2=Button(self.root,textvariable=b2_text_var,command=change_on,bg="red",width=44,fg="white")
        b2_text_var.set("去修改（当前为新增模式）")
        b2.grid(row=0,column=0,columnspan=5)
        b3=Button(self.root,text="GO=>>",command=select_value,bg="white",fg="white",state=DISABLED)
        b3.grid(row=1,column=2)
        b4=Button(self.root,text="目标文件",command=select_file,bg="yellow",fg="blue").grid(row=11,column=2)
        self.root.mainloop()
        
        
if __name__=="__main__":
    gui_log=log_gui()
    gui_log.add_info()