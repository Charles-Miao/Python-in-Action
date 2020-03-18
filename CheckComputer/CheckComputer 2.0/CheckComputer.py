from activation import activation
from officescan import officescan
import tkinter as tk

if __name__ == "__main__":
    #check activation
    os_activation=activation()
    os_activation.close_dialog_box()
    if os_activation.is_activated()==1:
        check_activation_result="The computer has been activated"
    else:
        os_activation.activate()
        check_activation_result="The computer is not activated, it has tried to activate itself"
    
    #check officescan
    check_officescan=officescan()
    if check_officescan.get_officescan_server_ptn()==check_officescan.get_officescan_client_ptn():
        check_officescan.virus_pattern_identical=1
        check_officescan_result="The computer virus pattern is the same with the server"
    elif check_officescan.network_connection==0:
        check_officescan_result="The computer virus pattern cannot be compared with the server because the network cannot connect"
    elif check_officescan.install_officescan==0:
        check_officescan_result="The computer virus pattern cannot be compared with the server because the officescan is not installed"
    else:
        check_officescan_result="The computer virus pattern is different from the server"

    #show the result
    #check_activation_result="12356789101112131415161718192021"
    #check_officescan_result="45665449895465113231654564561332"
    window=tk.Tk()
    window.title("The results of checking activation and officescan")
    window.geometry('210x210')
    tk.Label(window, text="Check activation result:"+"\n"+check_activation_result+"\n"+"\n"+"Check officescan result:"+"\n"+check_officescan_result, bg='white', font=('Arial', 12),width = 210,height = 210,wraplength = 200,justify = 'left').pack()
    window.mainloop()