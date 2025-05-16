#-*-coding: utf-8 -*-

#import os
import datetime
import configparser
#import numpy as np
import pandas as pd
from collections import Counter

class LeanReportExcel:
    def __init__(self,ini_path,raw_data):
        self.ini_path_temp=ini_path
        self.raw_data_temp=raw_data
        self.config=configparser.ConfigParser()
        self.config.read(self.ini_path_temp)
        self.year=self.config.get('info', 'year')
        self.department=self.config.get('info', 'department')
        self.propose_goal=self.config.get('info', 'propose_goal')
        self.save_manpower_goal=self.config.get('info', 'save_manpower_goal')
        self.org_data=pd.read_excel(self.raw_data_temp)
    
    #获取实际每月提案数量
    def propose_actual(self):
        #对应年度，对应部门，正在进行中的提案
        Implement_data=self.org_data.loc[(self.department[0:4]==self.org_data['提案部門'].str[0:4]) & (int(self.year)==self.org_data['提案日期'].map(lambda x: x.year).fillna(0).astype('Int32')) & (self.org_data['提案狀態']=="Implement")]
        #对应年度，对应部门，完成的提案
        Close_data=self.org_data.loc[(self.department[0:4]==self.org_data['提案部門'].str[0:4]) & (int(self.year)==self.org_data['提案日期'].map(lambda x: x.year).fillna(0).astype('Int32')) & (self.org_data['提案狀態']=="Close")]
        #对应年度，对应部门，执行中Reject提案
        Reject_data=self.org_data.loc[(self.department[0:4]==self.org_data['提案部門'].str[0:4]) & (int(self.year)==self.org_data['提案日期'].map(lambda x: x.year).fillna(0).astype('Int32')) & (self.org_data['提案狀態']=="Reject") & (self.org_data['預計開始日期'].map(lambda x: x.year).fillna(0).astype('Int32')>2010)]
        #将3种情况各月数据相加，得到每月实际提案件数
        propose_actual_dic={}
        implement_dic=Implement_data['提案日期'].map(lambda x: x.month).value_counts().to_dict()
        close_dic=Close_data['提案日期'].map(lambda x: x.month).value_counts().to_dict()
        reject_dic=Reject_data['提案日期'].map(lambda x: x.month).value_counts().to_dict()
        X,Y,Z=Counter(implement_dic),Counter(close_dic),Counter(reject_dic)
        propose_actual_dic=dict(X+Y+Z)
        #若某月为空则设定为0
        if len(propose_actual_dic) < datetime.datetime.now().month:
            propose_actual_dic[datetime.datetime.now().month]=0
        return(propose_actual_dic)
    
    #获取实际每月节省人力数
    def save_manpower_actual(self):
        #对应年度，对应部门，实际节省人力的提案
        save_manpower_data=self.org_data.loc[(self.department[0:4]==self.org_data['被提案部門'].str[0:4]) & (int(self.year)==self.org_data['完成時間'].map(lambda x: x.year).fillna(0).astype('Int32')) & (self.org_data['實際節省人力/月'].fillna(0).astype('Int32')>0)]
        #对应年度，月份列表
        save_manpower_month=save_manpower_data['完成時間'].map(lambda x: x.month).values
        #对应年度，省人列表
        save_manpower=save_manpower_data['實際節省人力/月'].fillna(0).astype('Int32').values
        #将对应列表转换为字典输出
        save_manpower_dic={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}
        for index in range(len(save_manpower_month)):
            save_manpower_dic[save_manpower_month[index]]+=save_manpower[index]
        return(save_manpower_dic)

    #获取implement提案，待TE签核
    def get_te_implement_data(self,excel_path):
        #获取implement提案
        Implement_data=self.org_data.loc[(self.department[0:4]==self.org_data['被提案部門'].str[0:4]) & (self.org_data['提案狀態']=="Implement") & (self.org_data['簽核步驟']<2.1) ]
        implement_table=Implement_data[['名稱','改善主題','核准者','指定執行負責人','預估節省人力/月','預計完成日期']]
        #写入Excel
        writer = pd.ExcelWriter(excel_path)
        implement_table.to_excel(writer, 'implement')
        writer.save()
        return(implement_table)
        
    #获取implement提案，待IE和Leader签核
    def get_ie_implement_data(self,excel_path):
        #获取implement提案
        Implement_data=self.org_data.loc[(self.department[0:4]==self.org_data['被提案部門'].str[0:4]) & (self.org_data['提案狀態']=="Implement") & (self.org_data['簽核步驟']>=2.1) & (self.org_data['簽核步驟']<2.32)]
        implement_table=Implement_data[['名稱','改善主題','核准者','指定執行負責人','預估節省人力/月','預計完成日期']]
        #写入Excel
        writer = pd.ExcelWriter(excel_path)
        implement_table.to_excel(writer, 'implement')
        writer.save()
        return(implement_table)

    #获取implement提案，待Boss签核
    def get_boss_implement_data(self,excel_path):
        #获取implement提案
        Implement_data=self.org_data.loc[(self.department[0:4]==self.org_data['被提案部門'].str[0:4]) & (self.org_data['提案狀態']=="Implement") & (self.org_data['簽核步驟']>=2.32)]
        implement_table=Implement_data[['名稱','改善主題','核准者','指定執行負責人','預估節省人力/月','預計完成日期']]
        #写入Excel
        writer = pd.ExcelWriter(excel_path)
        implement_table.to_excel(writer, 'implement')
        writer.save()
        return(implement_table)

    #获取Issue提案
    def get_issue_data(self,excel_path):
        #获取Issue提案
        Issue_data=self.org_data.loc[(self.department[0:4]==self.org_data['被提案部門'].str[0:4]) & (self.org_data['提案狀態']=="Issue")]
        issue_table=Issue_data[['名稱','改善主題','核准者','指定執行負責人','預估節省人力/月','預計完成日期']]
        #写入Excel
        writer = pd.ExcelWriter(excel_path)
        issue_table.to_excel(writer, 'issue')
        writer.save()
        return(issue_table)

     #获取实际每月提案数量
    
    #获取所有执行阶段的提案
    def get_implement_stage_data(self,excel_path):
        #对应部门，正在进行中的提案
        Implement_data=self.org_data.loc[(self.department[0:4]==self.org_data['提案部門'].str[0:4]) & (self.org_data['提案狀態']=="Implement")]
        #对应部门，完成的提案
        Close_data=self.org_data.loc[(self.department[0:4]==self.org_data['提案部門'].str[0:4]) & (self.org_data['提案狀態']=="Close")]
        #对应部门，执行中Reject提案
        Reject_data=self.org_data.loc[(self.department[0:4]==self.org_data['提案部門'].str[0:4]) & (self.org_data['提案狀態']=="Reject") & (self.org_data['預計開始日期'].map(lambda x: x.year).fillna(0).astype('Int32')>2010)]
        #将3种情况相加
        frames = [Implement_data, Close_data, Reject_data]
        result = pd.concat(frames)
        #排序
        result.sort_values("名稱",inplace=True,ascending=False)
        #写入Excel
        writer = pd.ExcelWriter(excel_path)
        result.to_excel(writer, 'implement_stage_data')
        writer.save()
        return(result)

    #获取所有执行阶段的提案
    def get_closed_data(self,excel_path):
        #对应部门，完成的提案
        Close_data=self.org_data.loc[(self.department[0:4]==self.org_data['被提案部門'].str[0:4]) & (self.org_data['提案狀態']=="Close")]
        #对应部门，执行中Reject提案
        Reject_data=self.org_data.loc[(self.department[0:4]==self.org_data['被提案部門'].str[0:4]) & (self.org_data['提案狀態']=="Reject") & (self.org_data['預計開始日期'].map(lambda x: x.year).fillna(0).astype('Int32')>2010)]
        #将3种情况相加
        frames = [Close_data, Reject_data]
        result = pd.concat(frames)
        #排序
        result.sort_values("名稱",inplace=True,ascending=False)
        #写入Excel
        writer = pd.ExcelWriter(excel_path)
        result.to_excel(writer, 'implement_stage_data')
        writer.save()
        return(result)

if __name__ == "__main__":
    Lean_Report=LeanReportExcel(ini_path=r"C:\Users\Charles\Desktop\Lean_Report_Auto\config.ini",raw_data=r"C:\Users\Charles\Desktop\Lean_Report_Auto\活頁簿1.xlsx")
    print(Lean_Report.propose_actual())
    print(Lean_Report.save_manpower_actual())
    Lean_Report.get_te_implement_data(r'C:\Users\Charles\Desktop\Lean_Report_Auto\implement_te.xlsx')
    Lean_Report.get_ie_implement_data(r'C:\Users\Charles\Desktop\Lean_Report_Auto\implement_ie.xlsx')
    Lean_Report.get_boss_implement_data(r'C:\Users\Charles\Desktop\Lean_Report_Auto\implement_boss.xlsx')
    Lean_Report.get_issue_data(r'C:\Users\Charles\Desktop\Lean_Report_Auto\issue.xlsx')
    Lean_Report.get_implement_stage_data(r'C:\Users\Charles\Desktop\Lean_Report_Auto\implement_all.xlsx')
    Lean_Report.get_closed_data(r'C:\Users\Charles\Desktop\Lean_Report_Auto\closed.xlsx')