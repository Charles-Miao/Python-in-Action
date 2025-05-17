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
import threading
import os

# ------------------- 配置区域（需根据实际环境修改）-------------------
EXCEL_FILE = "CBR上传list"
PKID_COLUMN_NAME = "PKID"
INFO_LOG_PATH = "info.txt"
ERROR_LOG_PATH = "error.txt"
PKID_LIST_PATH = "PKID_list.txt"  # 新增配置项

SHORT_TIMEOUT = 0.5  # 短时间等待
MEDIUM_TIMEOUT = 1.0  # 中等时间等待
LONG_TIMEOUT = 2.0  # 长时间等待
# ---------------------------------------------------

def get_latest_excel_file(pattern):
    """获取符合模式的最新Excel文件"""
    try:
        files = [f for f in os.listdir() if f.startswith(pattern) and f.endswith(".xlsm")]
        if not files:
            raise FileNotFoundError(f"未找到符合模式 '{pattern}' 的Excel文件")
        # 按修改时间排序，取最新文件
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return files[0]
    except Exception as e:
        raise RuntimeError(f"获取Excel文件失败: {str(e)}")

def delete_old_files():
    """删除旧的日志文件和PKID列表文件"""
    files_to_delete = [INFO_LOG_PATH, ERROR_LOG_PATH, PKID_LIST_PATH]
    for file_path in files_to_delete:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"已删除旧文件: {file_path}")
            except Exception as e:
                print(f"删除文件 {file_path} 失败: {str(e)}")


def read_pkid_from_excel():
    try:
        excel_file = get_latest_excel_file(EXCEL_FILE)
        df = pd.read_excel(excel_file)
        if PKID_COLUMN_NAME not in df.columns:
            raise ValueError(f"Excel中未找到列名：{PKID_COLUMN_NAME}")
        write_info_to_file(f"使用文件: {excel_file} 读取数据")
        return df[PKID_COLUMN_NAME].tolist()
    except Exception as e:
        write_error_to_file(f"读取Excel数据失败: {str(e)}\n{traceback.format_exc()}")
        raise


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

def wait_for_control(control, state='visible', timeout=2.0, retry_interval=0.2):
    """等待控件处于指定状态，严格控制总等待时间不超过 timeout"""
    elapsed_time = 0
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if state == 'visible' and control.element_info.visible:
                return True
        except Exception:
            # 仅在控件不存在时抛出异常，其他情况忽略（如属性暂不可用）
            if not control.exists():
                raise
        time.sleep(retry_interval)
        elapsed_time = time.time() - start_time

    write_info_to_file(f"等待控件 {control} 可见超时，等待时间: {elapsed_time:.2f} 秒")
    return False

def auto_submit_pkid(pkid_list):
    app_name = 'Microsoft.MDOS.SmartClient.UI.exe'
    pid = get_process_id_by_name(app_name)
    write_info_to_file(f"尝试连接进程：{app_name}（PID: {pid if pid else '未找到'}）")

    try:
        # 连接MDOS应用
        app = Application(backend='uia').connect(process=pid)
        write_info_to_file("成功连接到 MDOS 应用")

        # 获取主窗口
        main_window = app.window(title_re="Main Panel")
        main_window.wait('visible', timeout=3)

        if not wait_for_control(main_window, 'visible', timeout=3):
            main_window = app.window(class_name_re="Window.*")
            main_window.wait('visible', timeout=3)
        write_info_to_file("获取主窗口成功")

        time.sleep(SHORT_TIMEOUT)  # 增加延迟

    except Exception as e:
        write_error_to_file(traceback.format_exc())
        return

    try:
        radio_indicator_floor = main_window.child_window(title="Please wait, Refreshing the dashboard.",
                                                         auto_id="busyShellIndicator",
                                                         control_type="ProgressBar")  # 请耐心等待..数据加载中
        Keys_NavigationView_floor = radio_indicator_floor.window(class_name="KeysOperationNavigationView")

        # 定位CBR按钮并点击
        CBR_button = Keys_NavigationView_floor.child_window(title="CBR by Keys", auto_id="CBRBYKeysoption",
                                                            control_type="Button")
        if wait_for_control(CBR_button, 'visible', timeout=LONG_TIMEOUT):
            CBR_button.click_input()
            write_info_to_file("点击 CBR by Keys 按钮成功")
        else:
            write_error_to_file("未找到 CBR by Keys 按钮控件")
            return
        time.sleep(SHORT_TIMEOUT)

        # 打印空间树信息
        # old_stdout = sys.stdout
        # result = StringIO()
        # sys.stdout = result

        # main_window.print_control_identifiers()

        # sys.stdout = old_stdout
        # output = result.getvalue()
        # print(output)

        # write_info_to_file("控件树结构信息：\n" + output)

        # 各组件层级
        cbr_pane_floor = radio_indicator_floor.window(class_name="ScrollViewer")
        cbr_byKEYView_floor = cbr_pane_floor.window(class_name="CBRByKeyView")
        cbr_indicator_floor = cbr_byKEYView_floor.child_window(title="请耐心等待..数据加载中",
                                                               auto_id="busyIndicatorCBRByKeys", control_type="ProgressBar")

        gridView_floor = cbr_indicator_floor.child_window(title="GridViewCBRByKey", auto_id="gridViewCBRKey",
                                                          control_type="DataGrid")
        part_GridView_floor = gridView_floor.child_window(auto_id="PART_GridViewVirtualizingPanel",
                                                          control_type="Custom")
        dataitem_floor = part_GridView_floor.child_window(
            title="Microsoft.MDOS.SmartClient.UI.KeyOpsModule.Models.ProductKeyInfo", auto_id="Row_0",
            control_type="DataItem")

        # 点击搜索功能区，确保页面展开
        cbr_search_text = cbr_indicator_floor.child_window(title="搜索", control_type="Text")
        input_box = cbr_indicator_floor.child_window(title="txtMSFTProductKeyID", auto_id="txtMSFTProductKeyID",
                                                     control_type="Edit")
        search_button = cbr_indicator_floor.child_window(title="Search Key", control_type="Button")
        submitted_text = cbr_indicator_floor.child_window(title="未找到数据", auto_id="NoDataText",
                                                          control_type="Text")
        submit_button = cbr_indicator_floor.child_window(title="btnSubmitCBRByKey",
                                                         auto_id="btnSubmitCBRByKey",
                                                         control_type="Button")

        # 开始上传PKID
        with open(PKID_LIST_PATH, 'a', encoding='utf-8') as f:
            f.write('pkid' + '\n')

            for pkid in pkid_list:
                start_time = time.time()  # 记录开始时间
                write_info_to_file(f"开始处理 PKID：{pkid}")
                try:
                    # 尝试等待输入框可见，超时时间设为2秒
                    if not wait_for_control(input_box, 'visible', timeout=MEDIUM_TIMEOUT):
                        write_info_to_file("PKID输入框不可见，尝试展开")
                        # 点击搜索功能区
                        cbr_search_text.click_input()
                        write_info_to_file("点击搜索功能区，等待输入框显示")
                        if not wait_for_control(input_box, 'visible', timeout=MEDIUM_TIMEOUT):
                            write_error_to_file(f"PKID输入框仍不可见，流程结束")
                            return

                    write_info_to_file("PKID输入框可见，准备输入")

                    # 输入PKID
                    input_box.set_text(str(pkid))
                    write_info_to_file(f"输入 PKID：{pkid}")

                    # 点击搜索按钮
                    search_button.click_input()
                    write_info_to_file("点击搜索按钮，等待搜索结果")
                    # time.sleep(SHORT_TIMEOUT)

                    # 检查是否已提交，优化等待时间
                    if wait_for_control(submitted_text, 'visible', timeout=MEDIUM_TIMEOUT):
                        write_info_to_file(f"PKID {pkid} 已提交（提示：未找到数据）")
                        f.write(f"{pkid}\n")  # 写入成功处理的PKID
                        continue  # 继续处理下一个PKID

                    # 判断当前PKID状态是否为bound
                    cell_0_4 = dataitem_floor.child_window(
                        title="Item: Microsoft.MDOS.SmartClient.UI.KeyOpsModule.Models.ProductKeyInfo, Column Display Index: 4",
                        auto_id="Cell_0_4", control_type="Custom")
                    bound_text = cell_0_4.child_window(title="Bound", auto_id="CellElement_0_4",
                                                        control_type="Text")
                    if not wait_for_control(bound_text, 'visible', timeout=MEDIUM_TIMEOUT):
                        write_info_to_file(f"PKID {pkid} 状态不为Bound，跳过提交")
                        f.write(f"{pkid}\n")  # 写入成功处理的PKID
                        continue  # 继续处理下一个PKID

                    # 勾选复选框
                    cell_0_0 = dataitem_floor.child_window(
                        title="Item: Microsoft.MDOS.SmartClient.UI.KeyOpsModule.Models.ProductKeyInfo, Column Display Index: 0",
                        auto_id="Cell_0_0", control_type="Custom")

                    checkbox = cell_0_0.child_window(title="select data item", auto_id="CellElement_0_0",
                                                     control_type="CheckBox")
                    checkbox.click_input()
                    write_info_to_file("勾选搜索结果复选框")

                    # 点击提交按钮
                    submit_button.click_input()
                    write_info_to_file("点击提交按钮，等待确认")

                    # 确认提交
                    confirm_message_box_floor = radio_indicator_floor.child_window(title="确认CBR密钥",
                                                                                   auto_id="operationStatusMessageBox",
                                                                                   control_type="Custom")

                    if wait_for_control(confirm_message_box_floor, 'visible', timeout=MEDIUM_TIMEOUT):
                        confirm_button = confirm_message_box_floor.child_window(title="Confirm",
                                                                                auto_id="btnCONFIRM",
                                                                                control_type="Button")
                        confirm_button.click_input()
                        write_info_to_file("确认提交操作完成")

                    # 仅在成功处理（未触发异常）时写入 PKID_list.txt
                    f.write(str(pkid) + '\n')
                    write_info_to_file(f"PKID {pkid} 处理完成，耗时: {time.time() - start_time:.2f}秒")


                except Exception as e:
                    write_error_to_file(f"处理 PKID {pkid} 时出错：{str(e)}\n{traceback.format_exc()}")
                    return

    except Exception as e:
        write_error_to_file(f"定位控件时出错：{str(e)}\n{traceback.format_exc()}")

def start_process():
    # 每次点击开始时删除旧文件
    delete_old_files()

    # 禁用开始按钮，防止重复点击
    confirm_button.config(state=tk.DISABLED)
    write_info_to_file("------------------- 程序启动 -------------------")

    def run_task():
        try:
            pkid_list = read_pkid_from_excel()
            write_info_to_file(f"成功读取 Excel 文件，获取 {len(pkid_list)} 个 PKID")
            auto_submit_pkid(pkid_list)
            write_info_to_file("所有 PKID 提交完成，程序正常结束")
        except Exception as e:
            write_error_to_file(f"程序主流程出错：{str(e)}\n{traceback.format_exc()}")
        finally:
            write_info_to_file("------------------- 程序结束 -------------------\n")
            # 恢复按钮状态（需在主线程中执行）
            root.after(0, lambda: confirm_button.config(state=tk.NORMAL))
            # 检测 error.txt 并弹出提示框
            if os.path.exists(ERROR_LOG_PATH):
                messagebox.showerror("运行结果", "程序运行失败，请在 error.txt 中查看错误说明")
            else:
                messagebox.showinfo("运行结果", "程序运行成功,请检查")

    # 创建并启动新线程
    thread = threading.Thread(target=run_task, daemon=True)
    thread.start()


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