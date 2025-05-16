import datetime
import configparser
import pandas as pd

from collections import Counter
from pptx import Presentation
from pptx.util import Pt
from pptx.util import Inches
from pptx.dml.color import RGBColor

from lean_report_excel import LeanReportExcel
from lean_report_pptx import slider_goal
from lean_report_pptx import slider_implement
from lean_report_pptx import slider_project
from lean_report_pptx import slider_reward

if __name__ == "__main__":
    #获取初始化数据
    Lean_Report=LeanReportExcel(ini_path=r"C:\Users\Charles\Desktop\Lean_Report_Auto\config.ini",raw_data=r"C:\Users\Charles\Desktop\Lean_Report_Auto\活頁簿1.xlsx")
    #筛选正在进行中的提案
    Lean_Report.get_te_implement_data(r'C:\Users\Charles\Desktop\Lean_Report_Auto\implement_te.xlsx')
    Lean_Report.get_ie_implement_data(r'C:\Users\Charles\Desktop\Lean_Report_Auto\implement_ie.xlsx')
    Lean_Report.get_boss_implement_data(r'C:\Users\Charles\Desktop\Lean_Report_Auto\implement_boss.xlsx')
    #筛选Issue提案
    Lean_Report.get_issue_data(r'C:\Users\Charles\Desktop\Lean_Report_Auto\issue.xlsx')
    #筛选所有进入执行阶段的提案
    Lean_Report.get_implement_stage_data(r'C:\Users\Charles\Desktop\Lean_Report_Auto\implement_all.xlsx')
    #筛选所有Closed提案
    Lean_Report.get_closed_data(r'C:\Users\Charles\Desktop\Lean_Report_Auto\closed.xlsx')
    #获取每月实际提案件数
    propose_actual=Lean_Report.propose_actual()
    #获取实际节省人力件数
    save_manpower_actual=Lean_Report.save_manpower_actual()
    #获取ini档案信息
    config=configparser.ConfigParser()
    config.read(r"C:\Users\Charles\Desktop\Lean_Report_Auto\config.ini")
    propose_goal=config.get('info', 'propose_goal')
    save_manpower_goal=config.get('info', 'save_manpower_goal')
    #加载模板
    prs=Presentation(r'C:\Users\Charles\Desktop\Lean_Report_Auto\Lean Report Template.pptx')
    #制作第一页
    prs=slider_goal(prs,propose_goal,save_manpower_goal,propose_actual,save_manpower_actual)
    #制作第二页
    implement_te_data=pd.read_excel(r"C:\Users\Charles\Desktop\Lean_Report_Auto\implement_te.xlsx")
    prs=slider_implement(prs,implement_te_data,"待TE签核")
    #制作第三页
    implement_ie_data=pd.read_excel(r"C:\Users\Charles\Desktop\Lean_Report_Auto\implement_ie.xlsx")
    prs=slider_implement(prs,implement_ie_data,"待IE签核")
    #制作第四页
    project_data=pd.read_excel(r"C:\Users\Charles\Desktop\Lean_Report_Auto\專案改善進度.xlsx")
    prs=slider_project(prs,project_data)
    #制作第五页
    prs=slider_reward(prs)
    #获取当前日期
    today=datetime.date.today()
    #保存pptx
    prs.save(r'C:\Users\Charles\Desktop\Lean_Report_Auto\Lean Report %s.pptx' % (str(today)))