# ------------------------------
# Written by: Charles Miao
# Company: Wistron Corporation
# Date: 2024-10-25
# version:Python3.9
# 修改记录：
# 2024-11-01：舍弃异常log；重构filt函数，将重复代码提取为copy_log_file函数
# 2024-11-04：舍弃offline测试的log（log中需要包含"update mes info"信息）
# 2024-11-05：重构copy_log_file函数，优化处理时间，原始方案筛选1.8W份log大约使用了75min，优化后只用了15min
# 2024-11-09：剔除Failing test due to：SFC和Exception
# ------------------------------
import os
import time
import re
from multiprocessing import Pool
import shutil

# 原始函数:
# def copy_log_file(entry, target_folder):
#     # 获取源文件绝对路径
#     source_file = os.path.dirname(entry) + "\\" + os.path.split(entry)[-1]
#     # 获取目标文件绝对路径
#     source_split = re.split(r'[\\]', source_file.strip())
#     target_file = target_folder + "\\" + source_split[-1]
#     # 拷贝条件：
#     # 1.文件格式需要为log
#     # 2.log命名需要以时间开头
#     # 3.log中需要同时包含"RUN SUMMARY"和"update mes info"
#     # 4.SN命名规则：P开头21位；N开头14位
#     file_format = re.split(r'[._]', source_split[-1].strip())[-1]
#     date_time = re.split(r'[._]', source_split[-1].strip())[0]
#     SN = re.split(r'[._]', source_split[-1].strip())[-2]
#     date_time_pattern = r"\d{20}"
#     SN_pattern = r'^(P.{20}|N.{13})$'
#     if file_format == "log" and re.match(date_time_pattern, date_time) and re.match(SN_pattern, SN):
#         read_log = open(source_file, mode='r', encoding='UTF-8')
#         content = read_log.readlines()
#         run_summary_found = False
#         update_mes_info_found = False
#         for index in range(len(content)):
#             if "RUN SUMMARY" in content[index]:
#                 run_summary_found = True
#             elif "update mes info" in content[index]:
#                 update_mes_info_found = True
#             if run_summary_found and update_mes_info_found:
#                 try:
#                     os.system('copy "%s" "%s" /y' % (source_file, target_file))
#                 except Exception as e:
#                     print(f"while copying {source_file} to {target_file}: {e}")
#                     return
#         read_log.close()

# 优化方案：
# 1. 路径操作：使用 os.path.abspath 和 os.path.join 来处理路径，更加安全和简洁。
# 2. 减少重复拆分：将 re.split 的结果存储在 parts 中，避免多次调用。
# 3. 文件资源管理：使用 with 语句自动管理文件的打开和关闭。
# 4. 文件复制：使用 shutil.copy2 替代 os.system，更高效和安全。
# 5. 提前退出：使用 any 函数来判断是否存在特定字符串，避免不必要的遍历；使用break提前退出循环
# 6. 字符串操作：直接使用 file_name，避免多次 strip 操作。
# 7. 优化正则表达式的使用： 只在需要时编译正则表达式，如果多次使用，考虑使用re.compile

def copy_log_file(entry, target_folder):
    # 获取源文件绝对路径
    source_file = os.path.abspath(entry)
    # 获取目标文件绝对路径
    target_file = os.path.join(target_folder, os.path.basename(source_file))
    
    # 拷贝条件：
    # 1. 文件格式需要为log
    # 2. log命名需要以时间开头
    # 3. log中需要同时包含"RUN SUMMARY"和"update mes info"
    # 4. SN命名规则：P开头21位；N开头14位
    # 5. Failing test due to：SFC和Exception，此部分log不拷贝
    file_name = os.path.basename(source_file)
    parts = re.split(r'[._]', file_name)
    
    file_format = parts[-1]
    date_time = parts[0]
    SN = parts[-2]

    date_time_pattern = re.compile(r"\d{20}")
    SN_pattern = re.compile(r'^(P.{20}|N.{13})$')
    SFC_pattern = re.compile(r"Failing test due to.*?SFC\w+")
    Exception_pattern = re.compile(r"Failing test due to.*?Exception\s.*")
    
    if file_format == "log" and re.match(date_time_pattern, date_time) and re.match(SN_pattern, SN):
        with open(source_file, mode='r', encoding='UTF-8') as read_log:
            content = read_log.readlines()
        
        run_summary_found = any("RUN SUMMARY" in line for line in content)
        update_mes_info_found = any("update mes info" in line for line in content)
        for index in range(len(content)):
            SFC_match = re.search(SFC_pattern, content[index])
            Exception_match = re.search(Exception_pattern, content[index])
            if SFC_match or Exception_match:
                break
        
        if run_summary_found and update_mes_info_found and not SFC_match and not Exception_match:
            try:
                shutil.copy2(source_file, target_file)
            except Exception as e:
                print(f"while copying {source_file} to {target_file}: {e}")
                return

def filt(source_folder,target_folder,date="all"):
    for files in os.walk(source_folder):
        with os.scandir(files[0]) as entries:
            for entry in entries:
                if os.path.isfile(entry):
                    # 获取文件修改日期
                    info = entry.stat()
                    time_local=time.localtime(info.st_mtime)
                    file_change_date=time.strftime("%Y-%m-%d",time_local)
                    #若为默认值则处理所有日期的文件
                    if date=="all":
                        copy_log_file(entry, target_folder)
                    #若指定日期，则拷贝指定日期的文件
                    elif file_change_date==date:
                        copy_log_file(entry, target_folder)

# 获取CPU核心数
def get_CPU_NumberOfCores():
	conent=os.popen("wmic cpu get NumberOfCores").readlines()
	CPU_NumberOfCores=0
	for index in range(len(conent)):
		if conent[index].strip()=="":
			continue
		elif conent[index].strip()=="NumberOfCores":
			continue
		else:
			CPU_NumberOfCores=CPU_NumberOfCores+int(conent[index].strip())
	return(str(CPU_NumberOfCores))        

if __name__ == "__main__":
    source_folder=r"C:\Users\Administrator\Desktop\EDA\NIO_Log"
    target_folder=r"C:\Users\Administrator\Desktop\EDA\Temp_Log"
    date="all"
	
    core=int(get_CPU_NumberOfCores())
    source_dirs=os.listdir(source_folder)

    p = Pool(core*5)
    for i in range(len(source_dirs)):
        p.apply_async(filt, args=(source_folder+"\\"+source_dirs[i],target_folder,date))
    p.close()
    p.join()
    print('All subprocesses done.')