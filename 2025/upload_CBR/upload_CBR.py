import pywinauto # pywinauto 是一个用于 自动化 Windows GUI 应用程序 的 Python 库，通过模拟用户操作（如点击、输入、窗口控制等），实现对桌面程序的自动化交互。
import pandas as pd
import time
from pywinauto.application import Application
from tkinter import messagebox
import tkinter as tk
import traceback
import psutil
from io import StringIO
import sys
import _ctypes  # 引入 COMError 所需类型

# ------------------- 配置区域（需根据实际环境修改）-------------------
EXCEL_FILE_PATH = "CBR上传list_20250429.xlsm"
PKID_COLUMN_NAME = "PKID"
INFO_LOG_PATH = "info.txt"
ERROR_LOG_PATH = "error.txt"
# ---------------------------------------------------

# 将EXCEL中的“PKID”列读出，并返回为列表
def read_pkid_from_excel():
    df = pd.read_excel(EXCEL_FILE_PATH)
    if PKID_COLUMN_NAME not in df.columns:
        raise ValueError(f"Excel 中未找到列名：{PKID_COLUMN_NAME}")
    return df[PKID_COLUMN_NAME].tolist()

# 查找指定进程名称的PID
def get_process_id_by_name(process_name):
    for proc in psutil.process_iter(['name', 'pid']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None

# 将信息写入日志文件
def write_info_to_file(message):
    with open(INFO_LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 信息: {message}\n")

# 将错误信息写入日志文件
def write_error_to_file(error_message):
    with open(ERROR_LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 错误:\n{error_message}\n{'=' * 80}\n")

def auto_submit_pkid(pkid_list):
    # Microsoft.MDOS.SmartClient.UI.exe 是微软数字运营服务（Microsoft Digital Operations Services, MDOS）智能客户端的用户界面程序。它的正常用途主要面向微软授权翻新商 (Microsoft Authorized Refurbisher, MAR)，用于管理和激活翻新设备上的 Windows 操作系统许可证。
    # 1. 获取数字产品密钥 (DPK)：授权翻新商通过 MDOS 智能客户端从微软获取用于激活 Windows 操作系统的数字产品密钥。
    # 2. 管理密钥库存：帮助翻新商跟踪和管理他们拥有的数字产品密钥。
    # 3. 注入产品密钥：在翻新计算机上安装 Windows 操作系统后，使用该工具将数字产品密钥注入到系统中，以完成激活过程。这通常是为了让最终用户在购买翻新设备后无需手动输入产品密钥。
    # 4. 生成和提交报告：用于创建和向微软提交计算机构建报告 (Computer Build Reports, CBR)，这是翻新流程的一部分。
    app_name = 'Microsoft.MDOS.SmartClient.UI.exe'
    pid = get_process_id_by_name(app_name)
    write_info_to_file(f"尝试连接进程：{app_name}（PID: {pid if pid else '未找到'}）")
    try:
        #创建了一个 Application 类的实例，并指定使用 "uia"（即 UI Automation）作为后端。pywinauto 支持多种后端，"uia" 适用于现代 Windows 应用（如 WPF、UWP），而 "win32" 适用于传统 Win32 应用。
        app = Application(backend='uia').connect(process=pid)
        write_info_to_file("成功连接到 MDOS 应用")
    except pywinauto.findwindows.ElementNotFoundError as e:
        write_error_to_file(traceback.format_exc())
        return

    try:
        # 定位主窗口
        main_window = app.window(title_re="Main Panel")
        # 等待窗口可见，最多等待5秒，最小化则不可见
        main_window.wait('visible', timeout=5)
        if not main_window.exists():
            # 如果主窗口不存在，则尝试透过类名查找，每个窗口在创建时都会被赋予一个类名
            main_window = app.window(class_name_re="Window.*")
            main_window.wait('visible', timeout=5)
        write_info_to_file("获取主窗口成功")

        time.sleep(2)  # 增加延迟
        
        #标准输出重定向用途：临时将输出内容捕获到内存中，而不是显示在终端或控制台
        old_stdout = sys.stdout # 保存当前标准输出
        result = StringIO() # 创建一个 StringIO 对象，用于捕获输出
        sys.stdout = result # 重定向标准输出到 StringIO 对象

        try:
            #打印目标窗口的控件层级结构，包括控件类型、标题、auto_id 等关键属性。
            main_window.print_control_identifiers()
        except _ctypes.COMError as com_err:
            write_error_to_file(f"打印控件标识符时 COM 错误: {str(com_err)}")
        finally:
            sys.stdout = old_stdout # 恢复标准输出
            output = result.getvalue() # 获取 StringIO 对象中的内容
            print(output)
            write_info_to_file("控件树结构信息：\n" + output)

    except Exception as e:
        write_error_to_file(traceback.format_exc())
        return

    # 定位 KeysOperationNavigationView 窗口
    radio_indicator_floor = main_window.child_window(title="Please wait, Refreshing the dashboard.", auto_id="busyShellIndicator", control_type="ProgressBar")  #请耐心等待..数据加载中
    Keys_NavigationView_floor = radio_indicator_floor.window(class_name="KeysOperationNavigationView")

    # 定位CBR按钮并点击
    CBR_button = Keys_NavigationView_floor.child_window(title="CBR by Keys", auto_id="CBRBYKeysoption", control_type="Button")
    if CBR_button.exists():
        CBR_button.click_input()
        write_info_to_file("点击 CBR by Keys 按钮成功")
    else:
        write_error_to_file("未找到 CBR by Keys 按钮控件")
    time.sleep(1)

    # 各组件层级
    cbr_pane_floor = radio_indicator_floor.window(class_name="ScrollViewer")
    cbr_byKEYView_floor = cbr_pane_floor.window(class_name="CBRByKeyView")
    cbr_indicator_floor = cbr_byKEYView_floor.child_window(title="请耐心等待..数据加载中",
                                                           auto_id="busyIndicatorCBRByKeys", control_type="ProgressBar")

    gridView_floor = cbr_indicator_floor.child_window(title="GridViewCBRByKey", auto_id="gridViewCBRKey", control_type="DataGrid")
    part_GridView_floor = gridView_floor.child_window(auto_id="PART_GridViewVirtualizingPanel", control_type="Custom")
    dataitem_floor = part_GridView_floor.child_window(title="Microsoft.MDOS.SmartClient.UI.KeyOpsModule.Models.ProductKeyInfo", auto_id="Row_0", control_type="DataItem")
    cell_0_0_floor = dataitem_floor.child_window(title="Item: Microsoft.MDOS.SmartClient.UI.KeyOpsModule.Models.ProductKeyInfo, Column Display Index: 0", auto_id="Cell_0_0", control_type="Custom")


    confirm_message_box_floor = radio_indicator_floor.child_window(title="确认CBR密钥",
                                                                   auto_id="operationStatusMessageBox",
                                                             control_type="Custom")

    # 点击搜索文本
    cbr_search_button = cbr_indicator_floor.child_window(title="搜索", control_type="Text")
    cbr_search_button.click_input()
    write_info_to_file("点击搜索成功")

    #开始上传PKID
    for pkid in pkid_list:
        write_info_to_file(f"开始处理 PKID：{pkid}")
        try:
            # 输入 PKID
            input_box = cbr_indicator_floor.child_window(title="txtMSFTProductKeyID", auto_id="txtMSFTProductKeyID", control_type="Edit")
            input_box.set_text(pkid)
            write_info_to_file(f"输入 PKID：{pkid}")

            # 点击搜索按钮
            search_button = cbr_indicator_floor.child_window(title="Search Key", control_type="Button")
            search_button.click_input()
            write_info_to_file("点击搜索按钮，等待搜索结果")
            time.sleep(2)

            # 检查是否已提交
            submitted_text = cbr_indicator_floor.child_window(title="未找到数据", auto_id="NoDataText", control_type="Text")
            if submitted_text.exists():
                write_info_to_file(f"PKID {pkid} 已提交（提示：未找到数据）")
            else:
                # 勾选复选框
                checkbox = cell_0_0_floor.child_window(title="select data item", auto_id="CellElement_0_0", control_type="CheckBox")
                checkbox.click_input()
                write_info_to_file("勾选搜索结果复选框")

                # 点击提交按钮
                submit_button = cbr_indicator_floor.child_window(title="btnSubmitCBRByKey", auto_id="btnSubmitCBRByKey", control_type="Button")
                submit_button.click_input()
                write_info_to_file("点击提交按钮，等待确认")
                time.sleep(1)

                # 确认提交
                confirm_message_box_floor.wait('visible', timeout=5)
                confirm_button = confirm_message_box_floor.child_window(title="Confirm", auto_id="btnCONFIRM", control_type="Button")
                confirm_button.click_input()
                write_info_to_file("确认提交操作完成")
                time.sleep(1)

            write_info_to_file(f"PKID {pkid} 处理完成")

        except Exception as e:
            write_error_to_file(f"处理 PKID {pkid} 时出错：{str(e)}\n{traceback.format_exc()}")

def start_process():
    write_info_to_file("------------------- 程序启动 -------------------")
    try:
        pkid_list = read_pkid_from_excel()
        write_info_to_file(f"成功读取 Excel 文件，获取 {len(pkid_list)} 个 PKID")
        auto_submit_pkid(pkid_list)
        write_info_to_file("所有 PKID 提交完成，程序正常结束")
    except Exception as e:
        write_error_to_file(f"程序主流程出错：{str(e)}\n{traceback.format_exc()}")
    finally:
        write_info_to_file("------------------- 程序结束 -------------------\n")

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Auto Upload CBR")
    #geometry是Tkinter库中用于设置窗口尺寸的核心方法
    root.geometry("350x100")
    # 设置1行2列的网格布局，参数 weight=1：设置列的权重比例，当窗口大小改变时：
    # 值为0（默认）表示列不扩展
    # 相同权重的列会平分额外空间
    # 不同权重按比例分配空间
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    # tk.Button：创建一个按钮控件
    # root：指定按钮的父容器为根窗口
    # text="开始"：设置按钮显示文本为"开始"
    # command=start_process：绑定点击事件到start_process函数
    confirm_button = tk.Button(root, text="开始", command=start_process)
    # row=0, column=0：将按钮放置在网格布局的第0行第0列
    # padx=20：设置左右内边距各为20像素
    # pady=25：设置上下内边距各为25像素
    # sticky="nsew"：控件拉伸方向（n=上, s=下, e=右, w=左），使按钮填满所在网格区域
    confirm_button.grid(row=0, column=0, padx=20, pady=25, sticky="nsew")
    # 创建一个退出按钮，点击时关闭窗口
    exit_button = tk.Button(root, text="退出", command=root.destroy)
    exit_button.grid(row=0, column=1, padx=20, pady=25, sticky="nsew")

    root.mainloop()