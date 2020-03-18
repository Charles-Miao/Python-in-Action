import autoit
import win32gui
import win32con
import time
import os

class activation:
    def __init__(self):
        self.activation=0

    #determine whether the system is activated
    def is_activated(self):
        #call system command
        os.popen("slmgr /dli")
        self.wait_dialog_box()
        #determine if it is licensed
        if autoit.win_exists("Windows Script Host",text="已授权") or autoit.win_exists("Windows Script Host",text="已取得授權") or autoit.win_exists("Windows Script Host",text="Licensed"):
            self.activation=1
        self.close_dialog_box()
        #return the result
        return(self.activation)

    #activate the os
    def activate(self):
        #call system command
        os.popen("slmgr /skms 10.37.31.86:1688")        
        self.wait_dialog_box()
        self.close_dialog_box()
        #call system command
        os.popen("slmgr /ato")
        self.wait_dialog_box()
        self.close_dialog_box()

    #close all the dialog box
    def close_dialog_box(self):
       while win32gui.FindWindow(None, "Windows Script Host")>0:
           #time.sleep(0.21)
           win32gui.SendMessage(win32gui.FindWindow(None, "Windows Script Host"),win32con.WM_CLOSE)

    #wait for the dialog box to appear
    def wait_dialog_box(self):
        time.sleep(1)
        count=1
        while win32gui.FindWindow(None, "Windows Script Host")==0:
            time.sleep(1)
            if count>21:
                break
            count=count+1


if __name__ == "__main__":
    os_activation=activation()
    os_activation.close_dialog_box()
    if os_activation.is_activated()==1:
        print("this computer has been activated")
    else:
        os_activation.activate()
        print("this computer is not activated, it has tried to activate itself")