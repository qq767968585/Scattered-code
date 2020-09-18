import os
import natsort
import xlrd
import xlwt

def day_pass(fileName1):
	file_open="D:/个人文件夹-宁菠/检验统计日报表/"+fileName1
	data1 = xlrd.open_workbook(file_open)
	table1 = data1.sheets()[0]
	colx1=6
	list_day1=table1.col_values(colx1, start_rowx=3, end_rowx=None)
	sum_val1=0
	for i in list_day1:
		if i:
			sum_val1=sum_val1+float(i)
	# colx2=7
    # list_day2=table1.col_values(colx2, start_rowx=3, end_rowx=None)
	# sum_val2=0
	# for j in list_day2:
	# 	sum_val2=sum_val2+float(j)
	return round(sum_val1)

# def day_nopass(fileName2):
# 	data2 = xlrd.open_workbook("D:\\个人文件夹-宁菠\\检验统计日报表\\"+fileName2)
# 	table2 = data2.sheets()[0]
# 	colx2=7
# 	list_day2=table2.col_values(colx2, start_rowx=3, end_rowx=None)
# 	sum_val2=0
# 	for i in list_day2:
# 		sum_val2=sum_val2+float(i)
# 	return round(sum_val2)

filePath = r'D:\个人文件夹-宁菠\检验统计日报表'
list_file =natsort.natsorted(os.listdir(filePath))
myWorkbook = xlwt.Workbook(encoding = 'utf-8')
mySheet = myWorkbook.add_sheet('sheet1')
for i in range(len(list_file)):
	mySheet.write(i, 0, day_pass(list_file[i]))
	# mySheet.write(i, 0, day_nopass(list_file[i]))
	# print(list_file[i])
myWorkbook.save(r'D:\个人文件夹-宁菠\日报表总计python\sum.xls')
