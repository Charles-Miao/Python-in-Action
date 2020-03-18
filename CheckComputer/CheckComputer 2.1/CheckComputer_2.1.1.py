import tkinter as tk
from activation import activation
from officescan import officescan
from infi.systray import SysTrayIcon
import time

class MainUI:
    def __init__(self, activation, officesan, connection, install, activation_result, officescan_result,window):
        self.activation=activation
        self.officescan=officesan
        self.connection=connection
        self.install=install
        self.activation_result=activation_result
        self.officescan_result=officescan_result
        self.window=window


    #show the result
    # check_activation_result="The computer is not activated, it has tried to activate itself."
    # check_officescan_result="The computer virus pattern cannot be compared with the server because the officescan is not installed."
    def showUI(self):
        
        #title
        self.window.title("The results of checking activation and officescan")
        #show title
        frame0 = tk.Frame(self.window) 
        frame0.grid(row=0, column=0,columnspan=4) 
        tk.Label(frame0, text="The results of checking activation and officescan"+"\n",font=('Arial', 13)).pack() 
        #show activation_result
        if self.activation==1:
            activation_result=["OK","green"]
        else:
            activation_result=["Fail","yellow"]

        frame1 = tk.Frame(self.window) 
        frame1.grid(row=1, column=0, sticky='w') 
        tk.Label(frame1, text="Activation Check Result:",width=25).pack(side='left') 
        tk.Label(frame1, text=activation_result[0],bg=activation_result[1],width=8).pack(side='left')
        #show officescan_result
        if self.officescan==1:
            officescan_result=["OK","green"]
        else:
            officescan_result=["Fail","yellow"]

        frame2 = tk.Frame(self.window) 
        frame2.grid(row=1, column=1, sticky='w') 
        tk.Label(frame2, text="OfficeScan Check Result:",width=25).pack(side='left')
        tk.Label(frame2, text=officescan_result[0],bg=officescan_result[1],width=8).pack(side='left') 
        #show network_result
        if self.connection==1:
            network_result=["OK","green"]
        else:
            network_result=["Fail","yellow"]

        frame3 = tk.Frame(self.window) 
        frame3.grid(row=2, column=0, sticky='w') 
        tk.Label(frame3, text="Network Connection Status:",width=25).pack(side='left') 
        tk.Label(frame3, text=network_result[0],bg=network_result[1],width=8).pack(side='left') 
        #show install_result
        if self.install==1:
            install_result=["OK","green"]
        else:
            install_result=["Fail","yellow"]

        frame4 = tk.Frame(self.window) 
        frame4.grid(row=2, column=1, sticky='w') 
        tk.Label(frame4, text="OfficeScan Install Status:",width=25).pack(side='left')
        tk.Label(frame4, text=install_result[0],bg=install_result[1],width=8).pack(side='left')
        #show remark
        frame5 = tk.Frame(self.window) 
        frame5.grid(row=3, column=0,columnspan=4,sticky='w') 
        tk.Label(frame5, text="\n").pack(side='left')

        frame6 = tk.Frame(self.window) 
        frame6.grid(row=4, column=0,columnspan=4, sticky='w') 
        tk.Label(frame6, text="Remark:").pack(side='left')

        frame7 = tk.Frame(self.window) 
        frame7.grid(row=5, column=0,columnspan=4, sticky='w') 
        tk.Label(frame7, text=self.activation_result).pack(side='left')

        frame8 = tk.Frame(self.window) 
        frame8.grid(row=6, column=0,columnspan=4, sticky='w') 
        tk.Label(frame8, text=self.officescan_result).pack(side='left')
        

if __name__ == "__main__":
    
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

    #show_UI
    def show(systray):
        window=tk.Tk()
        UI = MainUI(os_activation.activation,check_officescan.virus_pattern_identical,check_officescan.network_connection,check_officescan.install_officescan,check_activation_result,check_officescan_result,window)
        UI.showUI()
        window.mainloop()

    if os_activation.activation==1 and check_officescan.virus_pattern_identical==1:
        pass
    else:   
        menu_options = (("Check Computer", None, show),)
        systray = SysTrayIcon("icon.ico", "Check Computer", menu_options)
        systray.start()