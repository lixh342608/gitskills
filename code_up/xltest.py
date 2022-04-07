#coding=utf-8
'''
Created on 2016年10月14日

@author: pc
'''
import xlrd,xlwt
from xlutils.copy import copy

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#读取excel第一个工作表一行数值（row_num)+int(cal)）
def xl_red(row_num,cal,xlfile=u"Y:/研发部/更新日志.xls",ind=0):
    exl=xlrd.open_workbook(xlfile)
    ex_sheet=exl.sheet_by_index(ind)
    
    cell=ex_sheet.row_values(int(row_num)+int(cal))
    
    return cell 
#写入excel第一个工作表某行第五列值为changed，行数（row=int(row)+int(cal)）,保存OK返回1，无法保存返回0
def xl_write(row,cal,col=5,changed=u"已更新",xlfile=u"Y:/研发部/更新日志.xls",ind=0):
    #返回一个单元格对像（row=rowIndex,col=colIndex）
    def _getOutCell(outSheet, colIndex=5, rowIndex=2):
        """ HACK: Extract the internal xlwt cell representation. """
        row = outSheet._Worksheet__rows.get(rowIndex)
        if not row: return None
        cell = row._Row__cells.get(colIndex)
        return cell
    row=int(row)+int(cal)
    
    exl=xlrd.open_workbook(u"Y:/研发部/更新日志.xls",formatting_info=True)
    r_sheet=exl.sheet_by_index(ind)
    w_exl=copy(exl)
    w_sheet=w_exl.get_sheet(ind)
    previousCell = _getOutCell(w_sheet)
    w_sheet.write(row,col,changed)
    newcell=_getOutCell(w_sheet, col, row)
    newcell.xf_idx = previousCell.xf_idx
    try:
        w_exl.save(xlfile)
        return 1
    except Exception as e:
        return 0

    
if __name__=="__main__":
    textlist=xl_red(2)
    print textlist
    xl_write(5,5)