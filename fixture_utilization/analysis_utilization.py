#SN
#綫體（同一個儀器，count最多的綫體名）
#站別（同一個儀器，count最多的站別名）
#平均時間（時間排序，逐一遞減，剔除最大和最小的20%的數據，中間數值取平均）
#上抛數量（同一個儀器，count所有上抛數據）
#稼動率（最大的時間-最小的時間）/24hour

import os
import re
import csv
import pandas as pd
import numpy as np

log_csv=r'D:\Fixture_Log\0312.csv'
utilization_csv=r'D:\Fixture_Log\0312_utilization.csv'

if os.path.exists(utilization_csv):
	os.remove(utilization_csv)
log_data=[]
data=pd.read_csv(log_csv)
#获取所有仪器的SN
SN=pd.Series(data['sn'].values).unique()

for index in SN:
	#获取sn
	sn=index
	#获取每个sn的table
	sn_data=data.loc[data['sn']==index]
	#获取count最多的线体名
	line=sn_data.loc[:,'line'].value_counts().idxmax()
	#获取count最多的站别名
	station=sn_data.loc[:,'station'].value_counts().idxmax()
	#获取测试次数
	quantities=len(sn_data)
	#获取上抛时间数组（先将时间转换为str，再转换为时间格式，最后再转换为数组）
	upload_time=pd.to_datetime(sn_data['time'].apply(str)).values
	#获取上抛时间间隔，单位为纳秒，1秒=1,000,000,000纳秒
	test_time_array=[]
	for i in range(len(upload_time)-1):
		test_time=upload_time[i+1]-upload_time[i]
		test_time_array.append(test_time)
	#获取时间间隔的平均数
	average=np.mean(test_time_array)
	#获取时间间隔的中位数
	median=np.median(test_time_array)
	#获取使用时长（最后一个上抛时间减去第一个上抛时间）
	total_time=upload_time[len(upload_time)-1]-upload_time[0]
	# try:
	# 	print((upload_time[len(upload_time)-1]-upload_time[0]))
	# except IndexError:
	# 	pass
	log_data.append([sn,line,station,quantities,average,median,total_time])

headers=['sn','line','station','quantities','average','median','total_time']
write_csv=open(utilization_csv,'w',newline='')
writer_csv=csv.writer(write_csv)
writer_csv.writerow(headers)
writer_csv.writerows(log_data)
write_csv.close()