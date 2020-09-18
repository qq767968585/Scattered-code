import os
import natsort
import xlrd
import re
# import sys



def lookFor(fileName, val):
    file_open="D:/个人文件夹-宁菠/检验统计日报表/"+fileName
    data = xlrd.open_workbook(file_open)
    table = data.sheets()[0]
    colx = 0
    list = table.col_values(colx, start_rowx=3, end_rowx=None)
    flag = ""
    for i in range(len(list)):
        if re.search(val, list[i]):
            flag = fileName
    return flag

# path=r"D:\个人文件夹-宁菠\日报表总计python"
# sys.path.append("path")
x = input("Input company's name your search:")
filePath = "D:/个人文件夹-宁菠/检验统计日报表"
list_file = natsort.natsorted(os.listdir(filePath))
for i in range(len(list_file)):
    str=lookFor(list_file[i], x)
    if str:
        print(str)
