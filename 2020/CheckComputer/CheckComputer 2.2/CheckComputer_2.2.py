import os
import win32api
import win32con
import win32gui_struct
import win32gui
import tkinter as tk
from activation import activation
from officescan import officescan


Main = None

class SysTrayIcon(object):
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]
    FIRST_ID = 1314
    def __init__(s,
                 icon,
                 hover_text,
                 menu_options,
                 on_quit=None,
                 default_menu_index=None,
                 window_class_name=None,):
        s.icon = icon
        s.hover_text = hover_text
        s.on_quit = on_quit

        menu_options = menu_options + (('Exit', None, s.QUIT),)
        s._next_action_id = s.FIRST_ID
        s.menu_actions_by_id = set()
        s.menu_options = s._add_ids_to_menu_options(list(menu_options))
        s.menu_actions_by_id = dict(s.menu_actions_by_id)
        del s._next_action_id

        s.default_menu_index = (default_menu_index or 0)
        s.window_class_name = window_class_name or "SysTrayIconPy"

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): s.refresh_icon,
                       win32con.WM_DESTROY: s.destroy,
                       win32con.WM_COMMAND: s.command,
                       win32con.WM_USER+20 : s.notify,}
        # 注册窗口类。
        window_class = win32gui.WNDCLASS()
        window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = s.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map #也可以指定wndproc.
        s.classAtom = win32gui.RegisterClass(window_class)

    def show_icon(s):
        # 创建窗口。
        hinst = win32gui.GetModuleHandle(None)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        s.hwnd = win32gui.CreateWindow(s.classAtom,
                                          s.window_class_name,
                                          style,
                                          0,
                                          0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0,
                                          0,
                                          hinst,
                                          None)
        win32gui.UpdateWindow(s.hwnd)
        s.notify_id = None
        s.refresh_icon()
        
        win32gui.PumpMessages()

    def show_menu(s):
        menu = win32gui.CreatePopupMenu()
        s.create_menu(menu, s.menu_options)
        #win32gui.SetMenuDefaultItem(menu, 1000, 0)
        
        pos = win32gui.GetCursorPos()
        # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
        win32gui.SetForegroundWindow(s.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                s.hwnd,
                                None)
        win32gui.PostMessage(s.hwnd, win32con.WM_NULL, 0, 0)

    def destroy(s, hwnd, msg, wparam, lparam):
        if s.on_quit: s.on_quit(s) #运行传递的on_quit
        nid = (s.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0) # 退出托盘图标

    def notify(s, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONDBLCLK: # 双击左键
            pass #s.execute_menu_option(s.default_menu_index + s.FIRST_ID)
        elif lparam == win32con.WM_RBUTTONUP: # 单击右键
            s.show_menu()
        elif lparam == win32con.WM_LBUTTONUP: # 单击左键
            nid = (s.hwnd, 0)
            win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
            win32gui.PostQuitMessage(0) # 退出托盘图标
            if Main: Main.root.deiconify()
        return True
        """ 可能的鼠标事件：
        WM_MOUSEMOVE
        WM_LBUTTONDOWN
        WM_LBUTTONUP
        WM_LBUTTONDBLCLK
        WM_RBUTTONDOWN
        WM_RBUTTONUP
        WM_RBUTTONDBLCLK
        WM_MBUTTONDOWN
        WM_MBUTTONUP
        WM_MBUTTONDBLCLK"""

    def _add_ids_to_menu_options(s, menu_options):
        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in s.SPECIAL_ACTIONS:
                s.menu_actions_by_id.add((s._next_action_id, option_action))
                result.append(menu_option + (s._next_action_id,))
            else:
                result.append((option_text,
                               option_icon,
                               s._add_ids_to_menu_options(option_action),
                               s._next_action_id))
            s._next_action_id += 1
        return result
        
    def refresh_icon(s, **data):
        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(s.icon): # 尝试找到自定义图标
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst,
                                       s.icon,
                                       win32con.IMAGE_ICON,
                                       0,
                                       0,
                                       icon_flags)
        else: # 找不到图标文件 - 使用默认值
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if s.notify_id: message = win32gui.NIM_MODIFY
        else: message = win32gui.NIM_ADD
        s.notify_id = (s.hwnd,
                          0,
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                          win32con.WM_USER+20,
                          hicon,
                          s.hover_text)
        win32gui.Shell_NotifyIcon(message, s.notify_id)

    def create_menu(s, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_icon:
                option_icon = s.prep_menu_icon(option_icon)
            
            if option_id in s.menu_actions_by_id:                
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui.CreatePopupMenu()
                s.create_menu(submenu, option_action)
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(s, icon):
        # 首先加载图标。
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        # 填满背景。
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        # "GetSysColorBrush返回缓存的画笔而不是分配新的画笔。"
        #  - 暗示没有DeleteObject
        # 画出图标
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)
        
        return hbm

    def command(s, hwnd, msg, wparam, lparam):
        id = win32gui.LOWORD(wparam)
        s.execute_menu_option(id)
        
    def execute_menu_option(s, id):
        menu_action = s.menu_actions_by_id[id]      
        if menu_action == s.QUIT:
            win32gui.DestroyWindow(s.hwnd)
        else:
            menu_action(s)

class _Main:
    def __init__(s, activation, officesan, connection, install, activation_result, officescan_result):
        s.activation=activation
        s.officescan=officesan
        s.connection=connection
        s.install=install
        s.activation_result=activation_result
        s.officescan_result=officescan_result

    def main(s):
        
        s.root = tk.Tk()

        icons = 'icon.ico'
        hover_text = "Check Computer" #悬浮于图标上方时的提示
        menu_options = ()
        s.sysTrayIcon = SysTrayIcon(icons, hover_text, menu_options, on_quit = s.exit, default_menu_index = 1)
        
        #title
        s.root.title("The results of checking activation and officescan")
        #show title
        frame0 = tk.Frame(s.root) 
        frame0.grid(row=0, column=0,columnspan=4) 
        tk.Label(frame0, text="The results of checking activation and officescan"+"\n",font=('Arial', 13)).pack() 
        #show activation_result
        if s.activation==1:
            activation_result=["OK","green"]
        else:
            activation_result=["Fail","yellow"]

        frame1 = tk.Frame(s.root) 
        frame1.grid(row=1, column=0, sticky='w') 
        tk.Label(frame1, text="Activation Check Result:",width=25).pack(side='left') 
        tk.Label(frame1, text=activation_result[0],bg=activation_result[1],width=8).pack(side='left')
        #show officescan_result
        if s.officescan==1:
            officescan_result=["OK","green"]
        else:
            officescan_result=["Fail","yellow"]

        frame2 = tk.Frame(s.root) 
        frame2.grid(row=1, column=1, sticky='w') 
        tk.Label(frame2, text="OfficeScan Check Result:",width=25).pack(side='left')
        tk.Label(frame2, text=officescan_result[0],bg=officescan_result[1],width=8).pack(side='left') 
        #show network_result
        if s.connection==1:
            network_result=["OK","green"]
        else:
            network_result=["Fail","yellow"]

        frame3 = tk.Frame(s.root) 
        frame3.grid(row=2, column=0, sticky='w') 
        tk.Label(frame3, text="Network Connection Status:",width=25).pack(side='left') 
        tk.Label(frame3, text=network_result[0],bg=network_result[1],width=8).pack(side='left') 
        #show install_result
        if s.install==1:
            install_result=["OK","green"]
        else:
            install_result=["Fail","yellow"]

        frame4 = tk.Frame(s.root) 
        frame4.grid(row=2, column=1, sticky='w') 
        tk.Label(frame4, text="OfficeScan Install Status:",width=25).pack(side='left')
        tk.Label(frame4, text=install_result[0],bg=install_result[1],width=8).pack(side='left')
        #show remark
        frame5 = tk.Frame(s.root) 
        frame5.grid(row=3, column=0,columnspan=4,sticky='w') 
        tk.Label(frame5, text="\n").pack(side='left')

        frame6 = tk.Frame(s.root) 
        frame6.grid(row=4, column=0,columnspan=4, sticky='w') 
        tk.Label(frame6, text="Remark:").pack(side='left')

        frame7 = tk.Frame(s.root) 
        frame7.grid(row=5, column=0,columnspan=4, sticky='w') 
        tk.Label(frame7, text=s.activation_result).pack(side='left')

        frame8 = tk.Frame(s.root) 
        frame8.grid(row=6, column=0,columnspan=4, sticky='w') 
        tk.Label(frame8, text=s.officescan_result).pack(side='left')

        s.root.bind("<Unmap>", lambda event: s.Unmap() if s.root.state() == 'iconic' else False)
        s.root.protocol('WM_DELETE_WINDOW', s.exit)
        s.root.resizable(0,0)
        s.root.mainloop()

    def Unmap(s):
        s.root.withdraw()
        s.sysTrayIcon.show_icon()

    def exit(s, _sysTrayIcon = None):
        s.root.destroy()
        print ('exit...')

if __name__ == '__main__':
    #check activation
    os_activation=activation()
    os_activation.close_dialog_box()
    os_activation.is_activated()
    if os_activation.activation==1:
        check_activation_result="The computer has been activated"
    else:
        os_activation.activate()
        check_activation_result="The computer is not activated, it has tried to activate itself."
    
    #check officescan
    check_officescan=officescan()
    server_ptn=check_officescan.get_officescan_server_ptn()
    client_ptn=check_officescan.get_officescan_client_ptn()
    if server_ptn==client_ptn or server_ptn==client_ptn+200 or server_ptn==client_ptn+400 or server_ptn+200==client_ptn or server_ptn+400==client_ptn:
        check_officescan.virus_pattern_identical=1
        check_officescan_result="The computer virus pattern is similar to the server."
    elif check_officescan.network_connection==0:
        check_officescan_result="The computer virus pattern cannot be compared with the server because the network cannot connect."
    elif check_officescan.install_officescan==0:
        check_officescan_result="The computer virus pattern cannot be compared with the server because the officescan is not installed."
    else:
        check_officescan_result="The computer virus pattern is not similar to the server."

    #show UI
    if os_activation.activation==1 and check_officescan.virus_pattern_identical==1:
        pass
    else:
        Main = _Main(os_activation.activation,check_officescan.virus_pattern_identical,check_officescan.network_connection,check_officescan.install_officescan,check_activation_result,check_officescan_result)
        Main.main()
