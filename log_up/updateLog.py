#coding=utf-8
'''
Created on 2016年10月13日

@author: pc
'''
from xlrd import open_workbook
from xlutils.copy import copy
import pickle

def _getOutCell(outSheet, colIndex, rowIndex):
        """ HACK: Extract the internal xlwt cell representation. """
        row = outSheet._Worksheet__rows.get(rowIndex)
        if not row: return None
        cell = row._Row__cells.get(colIndex)
        return cell
def _write_value(outsheet,colIndex, rowIndex,value):
    
    outsheet.write(rowIndex,colIndex,value)
    pv_cell=_getOutCell(outsheet, colIndex, rowIndex-1)
    new_cell=_getOutCell(outsheet, colIndex, rowIndex)
    new_cell.xf_idx = pv_cell.xf_idx
    
def read_cell(xlfile=u"C:/test/更新日志.xls"):
    rb = open_workbook(xlfile,formatting_info=True)
    rs = rb.sheet_by_index(0)
    rows=rs.nrows
    cal=1
    cell_value = rs.cell(rows-cal,0).value
    while not cell_value:
        cal+=1
        cell_value = rs.cell(rows-cal,0).value
        
        
    return cell_value,rb
def read_row(rowindex,cal=2,xlfile=u"C:/test/更新日志.xls"):
    rb = open_workbook(xlfile,formatting_info=True)
    rs = rb.sheet_by_index(0)
    row_cell=rs.row_values(int(rowindex)+int(cal))
    return row_cell
    
def write_log(textlist,cal=2):
    cell_value,rb=read_cell()
    wb = copy(rb)
    #通过get_sheet()获取的sheet有write()方法
    ws = wb.get_sheet(0)
    rows=int(textlist[0])+int(cal)
    col=0 
    for value in textlist:
        try:
            _write_value(ws,col, rows,int(value))
        except:
            _write_value(ws,col, rows,value)
        
        col+=1
    while col<8:
        _write_value(ws,col, rows,"")
        col+=1
           
    wb.save(u"C:/test/更新日志.xls")
#读取配置文件
def loadcol(dump_file="collocation.pic"):
    try:
        with open(dump_file,"r") as f:
            col=pickle.load(f)   
            return col     
    except IOError:
        return ""
#生成配置文件 
def writcol(col,dump_file="collocation.pic"):
    with open(dump_file,"w") as f:
        pickle.dump(col, f)
if __name__=="__main__":
    #textlist=["9",u"余额支付","/mapi/mapi/Lib/cartModule.class.php",815,u"维冒号"]
    #write_log(textlist)
    row_cell=read_row()
    print row_cell