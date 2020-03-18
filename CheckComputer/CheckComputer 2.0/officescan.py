import configparser
import re
import os
import psutil

class officescan:
    def __init__(self):
        self.virus_pattern_identical=0
        self.install_officescan=0
        self.network_connection=0


    def get_officescan_client_ptn(self):
        if os.path.exists(r'C:\Program Files (x86)\Trend Micro\OfficeScan Client\updinfo.ini'):
            officescan_client_path=r'C:\Program Files (x86)\Trend Micro\OfficeScan Client\updinfo.ini'
            self.install_officescan=1
        elif os.path.exists(r'C:\Program Files\Trend Micro\OfficeScan Client\updinfo.ini'):
            officescan_client_path=r'C:\Program Files\Trend Micro\OfficeScan Client\updinfo.ini'
            self.install_officescan=1
        try:
            config=configparser.ConfigParser()
            config.read(officescan_client_path)
        except:
            return("officescan is not installed")
        else:
            return(int(config.get('INI_UPDATE_SECTION','Ptnfile_Version')))
        

    def get_officescan_server_ptn(self):
        os.system(r"net use w: /d /y")
        try:
            errorcode=os.system(r"net use w: \\172.168.168.100\ofcscan /user:admin btco")
            if errorcode==0:
                self.network_connection=1
            config=configparser.ConfigParser(strict=False,allow_no_value=True)
            config.read(r'W:\ofcscan.ini')
            ptn=config.get('INI_PROGRAM_VERSION_SECTION','NonCrcPtnVersion')
        except:
            return("cannot connect to the server")
        else:
            os.system(r"net use w: /d /y")
            return(int(re.split(r'[.]',ptn)[0]+re.split(r'[.]',ptn)[1]+re.split(r'[.]',ptn)[2]))


	
if __name__ == '__main__':
    check_officescan=officescan()
    if check_officescan.get_officescan_server_ptn()==check_officescan.get_officescan_client_ptn():
        check_officescan.virus_pattern_identical=1
        print("the computer virus pattern is the same with the server")
    elif int(check_officescan.get_officescan_server_ptn())==int(check_officescan.get_officescan_client_ptn())+200:
        check_officescan.virus_pattern_identical=1
        print("the computer virus pattern is the same with the server")
    elif check_officescan.network_connection==0:
        print("the computer virus pattern cannot be compared with the server because the network cannot connect")
    elif check_officescan.install_officescan==0:
        print("the computer virus pattern cannot be compared with the server because the officescan is not installed") 
    else:
        print("the computer virus pattern is different from the server")