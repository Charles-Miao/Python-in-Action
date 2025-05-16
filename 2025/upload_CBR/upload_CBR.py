import pywinauto
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

def read_pkid_from_excel():
    df = pd.read_excel(EXCEL_FILE_PATH)
    if PKID_COLUMN_NAME not in df.columns:
        raise ValueError(f"Excel 中未找到列名：{PKID_COLUMN_NAME}")
    return df[PKID_COLUMN_NAME].tolist()

def get_process_id_by_name(process_name):
    for proc in psutil.process_iter(['name', 'pid']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None

def write_info_to_file(message):
    with open(INFO_LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 信息: {message}\n")

def write_error_to_file(error_message):
    with open(ERROR_LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 错误:\n{error_message}\n{'=' * 80}\n")

def auto_submit_pkid(pkid_list):
    app_name = 'Microsoft.MDOS.SmartClient.UI.exe'
    pid = get_process_id_by_name(app_name)
    write_info_to_file(f"尝试连接进程：{app_name}（PID: {pid if pid else '未找到'}）")

    try:
        app = Application(backend='uia').connect(process=pid)
        write_info_to_file("成功连接到 MDOS 应用")
    except pywinauto.findwindows.ElementNotFoundError as e:
        write_error_to_file(traceback.format_exc())
        return

    try:
        main_window = app.window(title_re="Main Panel")
        main_window.wait('visible', timeout=5)
        if not main_window.exists():
            main_window = app.window(class_name_re="Window.*")
            main_window.wait('visible', timeout=5)
        write_info_to_file("获取主窗口成功")

        time.sleep(2)  # 增加延迟

        old_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result

        try:
            main_window.print_control_identifiers()
        except _ctypes.COMError as com_err:
            write_error_to_file(f"打印控件标识符时 COM 错误: {str(com_err)}")
        finally:
            sys.stdout = old_stdout
            output = result.getvalue()
            print(output)
            write_info_to_file("控件树结构信息：\n" + output)

    except Exception as e:
        write_error_to_file(traceback.format_exc())
        return


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
    root.geometry("350x100")

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)

    confirm_button = tk.Button(root, text="开始", command=start_process)
    confirm_button.grid(row=0, column=0, padx=20, pady=25, sticky="nsew")

    exit_button = tk.Button(root, text="退出", command=root.destroy)
    exit_button.grid(row=0, column=1, padx=20, pady=25, sticky="nsew")

    root.mainloop()