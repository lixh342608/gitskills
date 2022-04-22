#coding=utf-8
'''
Created on 2016年10月14日

@author: pc
'''
from pymouse import PyMouse



    
if __name__=="__main__":
    m=PyMouse()
    #m.move(30,230)
    #m.click(30,230,1)
    m.click(30, 230, 1,100000000)

