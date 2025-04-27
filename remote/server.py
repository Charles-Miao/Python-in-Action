import tkinter as tk
from tkinter import messagebox
import configparser
import subprocess

# 服务器连接信息（服务端若在本地服务器可省略，若需访问共享配置则添加）
SERVER_ADDRESS = r'\\10.197.193.15'
USERNAME = 'ht\esop'
PASSWORD = 'Js@ict2024'

# 连接服务器共享（服务端若在本地运行可跳过，根据实际环境调整）
def connect_to_server():
    try:
        subprocess.run(
            ['net', 'use', SERVER_ADDRESS, PASSWORD, '/user:' + USERNAME],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("服务器连接成功")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("连接失败", f"服务器连接失败: {e.stderr}")
        root.destroy()  # 连接失败则关闭程序

config_file = f'{SERVER_ADDRESS}\ht共享盘\ESOP\测试SOP\onekey\server_config.ini'
config = configparser.ConfigParser()
config.read(config_file)

# 重置配置文件中的值
for section in config.sections():
    for key in config[section]:
        if config[section][key] != '0':
            config.set(section, key, '0')
with open(config_file, 'w') as configfile:
    config.write(configfile)

# 创建主窗口
root = tk.Tk()
root.title("远程控制ESOP电脑")
root.geometry("1000x600")

canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.config(yscrollcommand=scrollbar.set)

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor=tk.NW)

all_computers = {}
all_checkbox_vars = {}
for section in config.sections():
    computers = []
    checkbox_vars = []
    for key in config[section]:
        computers.append(key)
        var = tk.IntVar()
        checkbox_vars.append(var)
    all_computers[section] = computers
    all_checkbox_vars[section] = checkbox_vars

# 增加执行前的检查逻辑
def execute_command():
    # 检查是否选择了控制命令
    selected_command = command_var.get()
    if selected_command == "无操作":
        messagebox.showwarning("操作提示", "请先选择要执行的控制命令（关机/重启/更新/远程连接）")
        return

    # 检查是否选择了至少一台电脑
    has_selected = False
    for section in all_checkbox_vars:
        checkbox_vars = all_checkbox_vars[section]
        for var in checkbox_vars:
            if var.get() == 1:
                has_selected = True
                break
        if has_selected:
            break

    if not has_selected:
        messagebox.showwarning("操作提示", "请先选择至少一台需要控制的电脑")
        return


    for section in all_computers:
        selected_computers = []
        checkbox_vars = all_checkbox_vars[section]
        computers = all_computers[section]
        for i, var in enumerate(checkbox_vars):
            if var.get() == 1:
                selected_computers.append(computers[i])

        command = command_var.get()
        num = 0
        if command == "关机":
            num = 1
        elif command == "重启":
            num = 2
        elif command == "更新":
            num = 3
        elif command == "远程连接":
            num = 4

        for computer in selected_computers:
            config.set(section, computer, str(num))

    with open(config_file, 'w') as configfile:
        config.write(configfile)

    messagebox.showinfo("提示", "执行成功")


def select_all_line(section):
    checkbox_vars = all_checkbox_vars[section]
    for var in checkbox_vars:
        var.set(1)

def deselect_all_line(section):
    checkbox_vars = all_checkbox_vars[section]
    for var in checkbox_vars:
        var.set(0)

# 命令选择区域（增加远程连接选项）
frame_right = tk.Frame(root)
frame_right.pack(side=tk.RIGHT, fill=tk.Y)

command_var = tk.StringVar()
command_var.set("无操作")

shutdown_button = tk.Radiobutton(frame_right, text="关机", variable=command_var, value="关机")
shutdown_button.pack(anchor=tk.W)

restart_button = tk.Radiobutton(frame_right, text="重启", variable=command_var, value="重启")
restart_button.pack(anchor=tk.W)

update_button = tk.Radiobutton(frame_right, text="更新客户端", variable=command_var, value="更新")
update_button.pack(anchor=tk.W, pady=(10, 0))

# remote_button = tk.Radiobutton(frame_right, text="远程连接", variable=command_var, value="远程连接")
# remote_button.pack(anchor=tk.W)

execute_button = tk.Button(frame_right, text="执行命令", command=execute_command)
execute_button.pack(anchor=tk.W, pady=10)

# 显示电脑列表（保留原有布局代码）
column = 0
for section, computers in all_computers.items():
    line_frame = tk.Frame(frame)
    line_frame.grid(row=0, column=column, padx=10, sticky=tk.N)
    tk.Label(line_frame, text=section).pack(anchor=tk.W)
    checkbox_vars = all_checkbox_vars[section]
    for i, computer in enumerate(computers):
        checkbox = tk.Checkbutton(line_frame, text=computer, variable=checkbox_vars[i])
        checkbox.pack(anchor=tk.W)

    select_all_button = tk.Button(line_frame, text="全选", command=lambda s=section: select_all_line(s))
    select_all_button.pack(side=tk.LEFT, anchor=tk.W)
    deselect_all_button = tk.Button(line_frame, text="取消全选", command=lambda s=section: deselect_all_line(s))
    deselect_all_button.pack(side=tk.LEFT, anchor=tk.W)
    column += 1

frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

if __name__ == '__main__':
    connect_to_server()
    root.mainloop()