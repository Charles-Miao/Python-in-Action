import configparser
import time
import subprocess
import socket
from datetime import datetime

# 服务器连接信息
SERVER_ADDRESS = r'\\10.197.193.15'
USERNAME = 'ht\esop'
PASSWORD = 'Js@ict2024'


# 连接服务器共享
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
        print(f"服务器连接失败: {e.stderr}")
        exit(1)


config_file = "config.ini"
server_config = f'{SERVER_ADDRESS}\ht共享盘\ESOP\测试SOP\onekey\server_config.ini'


# 从本地config.ini文件中读取computer_name
def get_computer_name():
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
        for section in config.sections():
            for key in config[section]:
                return key
    except Exception as e:
        print(f"读取本地配置文件获取computer_name出错: {e}")
    return None


computer_name = get_computer_name()
if computer_name is None:
    print("无法从本地配置文件中获取computer_name，程序可能无法正常工作。")
    exit(1)  # 强制退出，避免无效循环


# 读取服务器配置值（新增：明确处理默认值）
def read_server_config():
    config = configparser.ConfigParser()
    try:
        config.read(server_config)
        for section in config.sections():
            if computer_name in config[section]:
                return config.get(section, computer_name, fallback='0')  # 新增fallback默认值
    except Exception as e:
        print(f"读取服务器配置文件出错: {e}")
    return '0'  # 异常时默认返回0


# 同步本地配置（核心修改部分）
def sync_local_with_server():
    server_num = read_server_config()
    if server_num != '0':  # 仅当服务器值非0时同步到本地
        update_local_config(server_num)
        print(f"服务器配置值为 {server_num}，已同步到本地")
    else:
        print("服务器配置值为0，无需同步本地")


# 更新本地config.ini文件
def update_local_config(num):
    config = configparser.ConfigParser()
    config.read(config_file)
    for section in config.sections():
        if computer_name in config[section]:
            config.set(section, computer_name, num)
            break
    with open(config_file, 'w') as configfile:
        config.write(configfile)


# 更新服务器上的server_config.ini文件
def update_server_config(num):
    config = configparser.ConfigParser()
    config.read(server_config)
    for section in config.sections():
        if computer_name in config[section]:
            config.set(section, computer_name, num)
            break
    with open(server_config, 'w') as configfile:
        config.write(configfile)


# 执行命令（仅当本地配置值与服务器同步后执行）
def execute_command(num):
    update_local_config('0')
    update_server_config('0')
    # print("命令执行完成，状态已重置为0")

    if num == '0':
        print("无操作")
        return

    print(f"执行命令: {num}")
    try:
        if num == '1':
            subprocess.run(['shutdown', '/s', '/t', '10'], check=True)
        elif num == '2':
            subprocess.run(['shutdown', '/r', '/t', '10'], check=True)
        elif num == '3':
            # 创建 STARTUPINFO 对象
            startupinfo = subprocess.STARTUPINFO()
            # 启用窗口显示控制
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            # 显式设置窗口为隐藏状态
            startupinfo.wShowWindow = subprocess.SW_HIDE
            subprocess.run(['update.bat'], check=True,startupinfo=startupinfo)

    except Exception as e:
        print(f"命令执行出错: {e}")



if __name__ == '__main__':
    connect_to_server()
    while True:
        # 1. 同步本地配置（仅当服务器值非0时更新）
        sync_local_with_server()

        # 2. 读取最新的本地配置值
        local_num = read_server_config()  # 这里直接复用服务器读取函数，因为本地和服务器已同步

        if local_num != '0':
            print(f"检测到有效命令: {local_num}，开始执行")
            execute_command(local_num)
        else:
            print("当前无有效命令（服务器值为0）")

        time.sleep(10)  # 主循环间隔